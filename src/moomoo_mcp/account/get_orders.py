from typing import Any, Dict, List, Optional
from ..opend.client import get_client

def get_orders(symbol: str = "") -> List[Dict[str, Any]]:
    """
    Get list of orders.
    Args:
        symbol: Optional symbol to filter by (e.g., "HK.00700")
    """
    client = get_client()
    # Fetch all orders (no status filter implies all)
    return client.get_orders(symbol=symbol)
