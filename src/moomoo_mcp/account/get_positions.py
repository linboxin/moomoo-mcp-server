from typing import Any, Dict, List
from ..opend.client import get_client

def get_positions() -> List[Dict[str, Any]]:
    """
    Get current stock positions in the account.
    Returns list of holdings (symbol, qty, cost, market value).
    """
    client = get_client()
    return client.get_positions()
