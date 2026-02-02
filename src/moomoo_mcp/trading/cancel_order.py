from typing import Any, Dict
from ..opend.client import get_client

def cancel_order(order_id: str) -> Dict[str, Any]:
    """
    Cancel an existing order.
    
    Args:
        order_id: The ID of the order to cancel.
    """
    client = get_client()
    return client.cancel_order(order_id)
