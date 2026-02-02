from typing import Any, List, Dict, Optional
from ..opend.client import get_client

def get_deals(symbol: str = "") -> List[Dict[str, Any]]:
    """
    Get list of executed deals (trades) for the current day.
    
    Args:
        symbol: Optional stock symbol to filter by (e.g., "HK.00700").
    """
    client = get_client()
    return client.get_deals(symbol=symbol)
