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
)
from ..config import config
from ..utils.symbols import normalize_symbol
from .errors import OpenDConnectionError, QuoteError

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

    def connect(self):
        """Connects to OpenD if not already connected."""
        if self._connected:
            return

        logger.info(f"Connecting to OpenD at {config.host}:{config.port}...")
        try:
            # Initialize Quote Context
            self._quote_ctx = OpenQuoteContext(host=config.host, port=config.port)
            
            # Initialize HK Trade Context (since we are focused on HK)
            self._trade_ctx = OpenHKTradeContext(host=config.host, port=config.port)

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
