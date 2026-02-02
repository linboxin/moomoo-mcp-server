from typing import Any, Dict
from ..opend.client import get_client

def modify_order(order_id: str, price: float, quantity: int) -> Dict[str, Any]:
    """
    Modify the price and quantity of an existing order.
    
    Args:
        order_id: The ID of the order to modify.
        price: New limit price.
        quantity: New quantity.
    """
    client = get_client()
    return client.modify_order(order_id, price, quantity)
