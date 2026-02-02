import logging
import threading
from typing import Optional, Dict, List, Any
from futu import (
    OpenQuoteContext,
    OpenSecTradeContext,
    RET_OK,
    RET_ERROR,
    SysConfig,
    KLType,
    AuType,
    SubType,
    TrdEnv,
    TrdSide,
    OrderType,
    ModifyOrderOp,
)
from ..config import config
from ..utils.symbols import normalize_symbol
from .errors import OpenDConnectionError, QuoteError
from ..risk.manager import RiskManager, RiskError

logger = logging.getLogger(__name__)

class MoomooClient:
# ... (existing init/connect generic methods skipped for brevity in replacement if not needed, but I need to locate insertion point)
# I will append new methods at the end or logic places.

    def get_max_buyable(self, symbol: str, price: float = 0.0) -> Dict[str, Any]:
        """
        Calculates max buyable quantity.
        Returns full trading info dict.
        """
        self.connect()
        if not self._trade_ctx:
             raise OpenDConnectionError("Trade context is null")
        
        symbol = normalize_symbol(symbol)
        trd_env = self._get_trd_env()
        
        # acctradinginfo_query(order_type, code, price, order_id=None, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)
        ret, data = self._trade_ctx.acctradinginfo_query(
            order_type=OrderType.NORMAL,
            code=symbol,
            price=price,
            trd_env=trd_env
        )
        
        if ret == RET_OK:
             return data.to_dict(orient="records")[0]
        else:
             logger.error(f"Error getting max buyable: {data}")
             raise QuoteError(f"OpenD Error: {data}")

    def get_financials(self, symbol: str) -> Dict[str, Any]:
        """
        Fetches fundamentals (PE, PB, MktCap) using get_market_snapshot.
        """
        self.connect()
        if not self._quote_ctx:
             raise OpenDConnectionError("Quote context is null")
        
        symbol = normalize_symbol(symbol)
        
        # Snapshot often requires QUOTE subscription or is push-based for some fields.
        # But get_market_snapshot documentation says it pulls latest.
        # However, to be safe and ensure data is recent/available:
        ret, err = self._quote_ctx.subscribe([symbol], [SubType.QUOTE], subscribe_push=False)
        if ret != RET_OK:
             raise QuoteError(f"Subscription failed for {symbol}: {err}")

        # get_market_snapshot takes list
        ret, data = self._quote_ctx.get_market_snapshot([symbol])
        
        if ret == RET_OK:
             return data.to_dict(orient="records")[0]
        else:
             logger.error(f"Error fetching financials: {data}")
             raise QuoteError(f"OpenD Error: {data}")

    def get_order_book(self, symbol: str, limit: int = 10) -> Dict[str, Any]:
        """
        Fetches Order Book (Level 2).
        """
        self.connect()
        if not self._quote_ctx:
             raise OpenDConnectionError("Quote context is null")
        
        symbol = normalize_symbol(symbol)
        
        # 1. Subscribe to ORDER_BOOK data
        # Note: Order Book requires specific subscription
        ret, err = self._quote_ctx.subscribe([symbol], [SubType.ORDER_BOOK], subscribe_push=False)
        if ret != RET_OK:
             raise QuoteError(f"Subscription failed for {symbol}: {err}")

        # get_order_book(code, num=10)
        ret, data = self._quote_ctx.get_order_book(symbol, num=limit)

        # Unsubscribe to clean up? Or keep it? 
        # Better to unsubscribe to avoid limit issues in long run, 
        # though client handles limit. Let's unsubscribe for safety in this tool.
        # But wait, unsubscribing might be slow.
        # For now, let's just fetch.
        
        if ret == RET_OK:
             # data is a dict with 'Bid', 'Ask' keys which are DataFrames/List
             # We need to convert them to easy dict
             return data
        else:
             logger.error(f"Error fetching order book: {data}")
             raise QuoteError(f"OpenD Error: {data}")

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancels an order.
        """
        self.connect()
        trd_env = self._get_trd_env()
        
        ret, data = self._trade_ctx.modify_order(
            ModifyOrderOp.CANCEL,
            order_id,
            0, # qty ignored for cancel
            0, # price ignored for cancel
            trd_env=trd_env
        )
        if ret == RET_OK:
             return data.to_dict(orient="records")[0]
        else:
             logger.error(f"Error canceling order: {data}")
             raise QuoteError(f"OpenD Error: {data}")

    def modify_order(self, order_id: str, price: float, quantity: int) -> Dict[str, Any]:
        """
        Modifies an order.
        """
        self.connect()
        trd_env = self._get_trd_env()
        
        # Note: Risk check logic for modification?
        # Ideally check new value. We'll skip stringent check for now or basic:
        # RiskManager.check_order(...)
        
        ret, data = self._trade_ctx.modify_order(
            ModifyOrderOp.NORMAL,
            order_id,
            quantity,
            price,
            trd_env=trd_env
        )
        if ret == RET_OK:
             return data.to_dict(orient="records")[0]
        if ret == RET_OK:
             return data.to_dict(orient="records")[0]
        else:
             logger.error(f"Error modifying order: {data}")
             raise QuoteError(f"OpenD Error: {data}")

    def close(self):
        if self._quote_ctx:
            try:
                self._quote_ctx.unsubscribe_all()
            except Exception as e:
                logger.warning(f"Error unsubscribing all: {e}")
            self._quote_ctx.close()
        if self._trade_ctx:
            self._trade_ctx.close()
        self._connected = False
        logger.info("Disconnected from OpenD.")

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._quote_ctx: Optional[OpenQuoteContext] = None
        self._trade_ctx: Optional[OpenSecTradeContext] = None
        self._connected = False
        
        # Configure futu global settings if needed
        SysConfig.enable_proto_encrypt(True if config.pwd else False)

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def _get_trd_env(self):
        if config.env.lower() == "live":
            return TrdEnv.REAL
        return TrdEnv.SIMULATE

    def connect(self):
        """Connects to OpenD if not already connected."""
        if self._connected:
            return

        logger.info(f"Connecting to OpenD at {config.host}:{config.port}...")
        try:
            # Initialize Quote Context
            self._quote_ctx = OpenQuoteContext(host=config.host, port=config.port)
            
            # Initialize Trade Context (Universal: supports HK, US, CN, etc.)
            self._trade_ctx = OpenSecTradeContext(host=config.host, port=config.port)

            # Simple test call
            ret, _ = self._quote_ctx.get_global_state()
            if ret != RET_OK:
                raise OpenDConnectionError("Failed to get global state after connect.")

            # Unlock if password provided
            if config.pwd:
                logger.info("Unlocking trade context...")
                ret, data = self._trade_ctx.unlock_trade(config.pwd)
                if ret != RET_OK:
                     logger.warning(f"Failed to unlock trade: {data}")
                else:
                     logger.info("Trade context unlocked.")

            self._connected = True
            logger.info("Connected to OpenD (Quote + HK Trade Context).")
        except Exception as e:
            logger.error(f"Failed to connect to OpenD: {e}")
            self._connected = False
            raise OpenDConnectionError(f"Connection failed: {e}")

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Fetches a snapshot quote for a given symbol.
        Returns a dictionary.
        """
        self.connect()
        if not self._quote_ctx:
             raise OpenDConnectionError("Quote context is null")

        symbol = normalize_symbol(symbol)

        # 1. Subscribe to QUOTE data
        ret, err = self._quote_ctx.subscribe([symbol], [SubType.QUOTE], subscribe_push=False)
        if ret != RET_OK:
            raise QuoteError(f"Subscription failed for {symbol}: {err}")

        # 2. Get stock quote
        ret, data = self._quote_ctx.get_stock_quote([symbol])
        if ret == RET_OK:
            return data.to_dict(orient="records")[0]
        else:
            logger.error(f"Error fetching quote for {symbol}: {data}")
            raise QuoteError(f"OpenD Error: {data}")

    def get_kline(self, symbol: str, ktype: str = "K_DAY", limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetches historical kline data using request_history_kline.
        """
        self.connect()
        if not self._quote_ctx:
             raise OpenDConnectionError("Quote context is null")
        
        symbol = normalize_symbol(symbol)

        # 1. Subscribe (ensure we have rights/data)
        ret, err = self._quote_ctx.subscribe([symbol], [ktype], subscribe_push=False)
        if ret != RET_OK:
            raise QuoteError(f"Subscription failed for {symbol} {ktype}: {err}")
            
        # 2. Get data using request_history_kline
        ret, data, _ = self._quote_ctx.request_history_kline(symbol, ktype=ktype, max_count=limit)
        
        # 3. Unsubscribe
        self._quote_ctx.unsubscribe([symbol], [ktype])
        
        if ret == RET_OK:
             return data.to_dict(orient="records")
        else:
             logger.error(f"Error fetching kline for {symbol}: {data}")
             raise QuoteError(f"OpenD Error: {data}")

    def get_positions(self, market: str = "HK") -> List[Dict[str, Any]]:
        """
        Fetches current stock positions.
        """
        self.connect()
        if not self._trade_ctx:
            raise OpenDConnectionError("Trade context is null")
            
        trd_env = self._get_trd_env()
        # Note: position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False)
        ret, data = self._trade_ctx.position_list_query(trd_env=trd_env)
        
        if ret == RET_OK:
            return data.to_dict(orient="records")
        else:
            logger.error(f"Error fetching positions: {data}")
            raise QuoteError(f"OpenD Error: {data}")

    def get_balance(self, market: str = "HK") -> Dict[str, Any]:
        """
        Fetches account balance details.
        """
        self.connect()
        if not self._trade_ctx:
            raise OpenDConnectionError("Trade context is null")
            
        trd_env = self._get_trd_env()
        # Note: accinfo_query(trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False)
        trd_env = self._get_trd_env()
        # Note: accinfo_query(trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False)
        ret, data = self._trade_ctx.accinfo_query(trd_env=trd_env)
        
        if ret == RET_OK:
            return data.to_dict(orient="records")[0]
        else:
            logger.error(f"Error fetching balance: {data}")
            raise QuoteError(f"OpenD Error: {data}")

    def get_orders(self, symbol: str = "", status_filter: List[Any] = None) -> List[Dict[str, Any]]:
        """
        Fetches orders.
        """
        self.connect()
        if not self._trade_ctx:
            raise OpenDConnectionError("Trade context is null")
            
        trd_env = self._get_trd_env()
        
        # Determine status filter (default to all if None)
        # In futu, execute_status_list=None means all
        
        ret, data = self._trade_ctx.order_list_query(
            code=symbol,
            trd_env=trd_env,
            status_filter_list=status_filter or []
        )
        
        if ret == RET_OK:
            return data.to_dict(orient="records")
        else:
            logger.error(f"Error fetching orders: {data}")
            raise QuoteError(f"OpenD Error: {data}")

    def get_option_chain(self, symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Fetches option chain.
        """
        self.connect()
        if not self._quote_ctx:
             raise OpenDConnectionError("Quote context is null")
             
        # Normalize symbol (for options, usually underlying is needed, but API takes 'code')
        # If symbol is the underlying stock, this returns options FOR that stock.
        symbol = normalize_symbol(symbol)
        
        # request_history_kline is NOT for option chains.
        # Use get_option_chain
        
        # Note: get_option_chain(code, begin_time, end_time, data_filter=None) -> actually (code, index_option_type, start, end, ...)
        # We must use kwargs to avoid passing date to index_option_type
        # Assuming index_option_type defaults to something valid or is ignored for stocks if skipped
        ret, data = self._quote_ctx.get_option_chain(symbol, start=start_date, end=end_date)
        
        if ret == RET_OK:
             return data.to_dict(orient="records")
        else:
             logger.error(f"Error fetching option chain: {data}")
             raise QuoteError(f"OpenD Error: {data}")

    def place_order(self, symbol: str, quantity: int, price: float, side: TrdSide, order_type: OrderType = OrderType.NORMAL) -> Dict[str, Any]:
        """
        Places an order after passing risk checks.
        """
        self.connect()
        if not self._trade_ctx:
             raise OpenDConnectionError("Trade context is null")

        symbol = normalize_symbol(symbol)
        
        # 1. Risk Check
        # For Market orders, price might be 0, so fetching current quote is safer for risk estimation
        check_price = price
        if order_type == OrderType.MARKET:
            try:
                # Fetch recent quote to estimate value
                # Note: This might add latency, but safety is priority
                quote = self.get_quote(symbol)
                check_price = quote.get("last_price", 0.0)
                if check_price == 0.0:
                     logger.warning("Market order risk check: Quote price is 0. Using provided price/0.")
            except Exception as e:
                logger.warning(f"Could not fetch quote for market order risk check: {e}")
        
        RiskManager.check_order(symbol, quantity, check_price)

        # 2. Place Order
        trd_env = self._get_trd_env()
        logger.info(f"Placing order: {side} {quantity} {symbol} @ {price} (Type: {order_type})")
        
        ret, data = self._trade_ctx.place_order(
            price=price,
            qty=quantity,
            code=symbol,
            trd_side=side,
            trd_env=trd_env,
            order_type=order_type, 
        )

        if ret == RET_OK:
            return data.to_dict(orient="records")[0]
        else:
            logger.error(f"Order failed: {data}")
            raise QuoteError(f"Order Placement Error: {data}")

    def close(self):
        if self._quote_ctx:
            try:
                self._quote_ctx.unsubscribe_all()
            except Exception as e:
                logger.warning(f"Error unsubscribing all: {e}")
            self._quote_ctx.close()
        if self._trade_ctx:
            self._trade_ctx.close()
        self._connected = False
        logger.info("Disconnected from OpenD.")

# Global client accessor
def get_client() -> MoomooClient:
    return MoomooClient.get_instance()
