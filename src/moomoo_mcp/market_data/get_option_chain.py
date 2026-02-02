from typing import Any, Dict, List
from ..opend.client import get_client

def get_option_chain(symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Get option chain for a stock.
    
    Args:
        symbol: Underlying stock symbol (e.g., "HK.00700")
        start_date: Start expiry date (YYYY-MM-DD)
        end_date: End expiry date (YYYY-MM-DD)
    """
    client = get_client()
    return client.get_option_chain(symbol, start_date, end_date)
