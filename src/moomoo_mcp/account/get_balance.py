from typing import Any, Dict
from ..opend.client import get_client

def get_balance() -> Dict[str, Any]:
    """
    Get account balance information (cash, market value, max power).
    """
    client = get_client()
    return client.get_balance()
