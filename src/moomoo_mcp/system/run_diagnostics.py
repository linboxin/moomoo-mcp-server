import time
import json
from typing import Dict, Any
from ..opend.client import get_client
from ..market_data.get_quote import get_quote
from ..market_data.get_kline import get_kline
from ..market_data.get_order_book import get_order_book
from ..account.get_balance import get_balance
from ..account.get_positions import get_positions
from ..config import config

def run_diagnostics(symbol: str = "HK.00700") -> str:
    """
    Runs a comprehensive self-test of the Moomoo MCP Server.
    Checks OpenD connection, market data latency, and account access.
    Returns a JSON report string.
    
    Args:
        symbol: The stock symbol to use for data tests.
    """
    client = get_client()
    results: Dict[str, Any] = {
        "ok": True,
        "environment": config.env,
        "results": {}
    }
    
    # helper for tracking task status
    def add_result(key: str, success: bool, **kwargs):
        results["results"][key] = {"ok": success, **kwargs}
        if not success:
            results["ok"] = False

    # 1. OpenD Connection
    try:
        t0 = time.time()
        client.connect() # Should be idempotent
        # Check connection status (maybe check global state again)
        # We assume if no exception, it worked.
        # Let's verify with a lightweight call
        ret, _ = client._quote_ctx.get_global_state()
        latency = (time.time() - t0) * 1000
        if ret == 0:
            add_result("opend", True, host=config.host, port=config.port, latency_ms=round(latency, 2))
        else:
            add_result("opend", False, error="get_global_state failed")
    except Exception as e:
        add_result("opend", False, error=str(e))
        return json.dumps(results, indent=2) # Stop early if connection fails

    # 2. Quote (Latency)
    try:
        t0 = time.time()
        quote = get_quote(symbol)
        latency = (time.time() - t0) * 1000
        if quote and "last_price" in quote:
            add_result("quote", True, latency_ms=round(latency, 2), price=quote["last_price"])
        else:
            add_result("quote", False, error="Empty response")
    except Exception as e:
        add_result("quote", False, error=str(e))

    # 3. KLine
    try:
        klines = get_kline(symbol, limit=5)
        if isinstance(klines, list):
             add_result("kline", True, count=len(klines))
        else:
             add_result("kline", False, error="Invalid format")
    except Exception as e:
        add_result("kline", False, error=str(e))

    # 4. Order Book (L2)
    try:
        # get_order_book returns formatted string in our wrapper tool, 
        # but to test we might want to check if it contains "ASKS" or throws error
        # Actually client.get_order_book returns dict. 
        # The tool `get_order_book` returns string ladder.
        # Let's use the tool logic to see if it works without error.
        ladder = get_order_book(symbol)
        if "ASKS" in ladder and "BIDS" in ladder:
             add_result("order_book", True, status="Readable")
        else:
             add_result("order_book", False, error="Unexpected format")
    except Exception as e:
        add_result("order_book", False, error=str(e))

    # 5. Balance
    try:
        bal = get_balance()
        if "cash" in bal:
             add_result("balance", True, cash=bal["cash"])
        else:
             add_result("balance", False, error="No cash field")
    except Exception as e:
        add_result("balance", False, error=str(e))

    # 6. Positions
    try:
        pos = get_positions()
        add_result("positions", True, count=len(pos))
    except Exception as e:
        add_result("positions", False, error=str(e))

    return json.dumps(results, indent=2)
