from typing import Any, List, Dict
from ..opend.client import get_client

def get_market_snapshot(symbols: List[str]) -> List[Dict[str, Any]]:
    """
    Efficiently fetch snapshot data for a list of stocks.
    Faster than get_quote for multiple symbols.
    
    Args:
        symbols: List of stock symbols (e.g. ["HK.00700", "US.AAPL"])
    """
    client = get_client()
    return client.get_market_snapshot(symbols)
