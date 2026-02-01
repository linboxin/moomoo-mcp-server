import logging
import threading
from typing import Optional, Dict, List, Any
from futu import (
    OpenQuoteContext,
    RET_OK,
    RET_ERROR,
    SysConfig,
)
from ..config import config
from .errors import OpenDConnectionError, QuoteError

logger = logging.getLogger(__name__)

class MoomooClient:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._quote_ctx: Optional[OpenQuoteContext] = None
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
            # Sync start required? usually yes.
            # OpenQuoteContext connects on init usually or we can check status?
            # Actually futu-api connects on __init__.
            
            # Simple test call
            ret, _ = self._quote_ctx.get_global_state()
            if ret != RET_OK:
                raise OpenDConnectionError("Failed to get global state after connect.")

            self._connected = True
            logger.info("Connected to OpenD (Quote Context).")
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

        # Futu expects symbol like "US.AAPL"
        ret, data = self._quote_ctx.get_stock_quote([symbol])
        if ret == RET_OK:
            # data is a DataFrame
            # Convert to dict
            record = data.to_dict(orient="records")[0]
            # Normalize keys if needed? For now return raw python data
            return record
        else:
            logger.error(f"Error fetching quote for {symbol}: {data}")
            raise QuoteError(f"OpenD Error: {data}")

    def close(self):
        if self._quote_ctx:
            self._quote_ctx.close()
        self._connected = False
        logger.info("Disconnected from OpenD.")

# Global client accessor
def get_client() -> MoomooClient:
    return MoomooClient.get_instance()
