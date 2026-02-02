import logging
import threading
from typing import Optional, Dict, List, Any
from futu import (
    OpenQuoteContext,
    OpenHKTradeContext,
    RET_OK,
    RET_ERROR,
    SysConfig,
    KLType,
    AuType,
    SubType,
    TrdEnv,
    TrdSide,
    OrderType,
)
from ..config import config
from ..utils.symbols import normalize_symbol
from .errors import OpenDConnectionError, QuoteError
from ..risk.manager import RiskManager, RiskError

logger = logging.getLogger(__name__)

class MoomooClient:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._quote_ctx: Optional[OpenQuoteContext] = None
        self._trade_ctx: Optional[OpenHKTradeContext] = None
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

        print("Entering client.connect()...", flush=True)
        logger.info(f"Connecting to OpenD at {config.host}:{config.port}...")
        try:
            # Initialize Quote Context
            print("Initializing Quote Context...", flush=True)
            self._quote_ctx = OpenQuoteContext(host=config.host, port=config.port)
            
            # Initialize HK Trade Context (since we are focused on HK)
            print("Initializing Trade Context...", flush=True)
            self._trade_ctx = OpenHKTradeContext(host=config.host, port=config.port)

            # Simple test call
            print("Checking Global State...", flush=True)
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
            print("Connection Established!", flush=True)
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
        print(f"Calling accinfo_query with env={trd_env}...", flush=True)
        ret, data = self._trade_ctx.accinfo_query(trd_env=trd_env)
        print(f"accinfo_query returned ret={ret}", flush=True)
        
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

    def place_order(self, symbol: str, quantity: int, price: float, side: TrdSide) -> Dict[str, Any]:
        """
        Places an order after passing risk checks.
        """
        self.connect()
        if not self._trade_ctx:
             raise OpenDConnectionError("Trade context is null")

        symbol = normalize_symbol(symbol)
        
        # 1. Risk Check (Raises RiskError if fails)
        RiskManager.check_order(symbol, quantity, price)

        # 2. Place Order
        trd_env = self._get_trd_env()
        logger.info(f"Placing order: {side} {quantity} {symbol} @ {price} (Env: {trd_env})")
        
        ret, data = self._trade_ctx.place_order(
            price=price,
            qty=quantity,
            code=symbol,
            trd_side=side,
            trd_env=trd_env,
            order_type=OrderType.NORMAL, # Limit Order
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
