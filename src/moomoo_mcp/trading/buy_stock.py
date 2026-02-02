from typing import Any, Dict
from futu import TrdSide
from ..opend.client import get_client

def buy_stock(symbol: str, quantity: int, price: float) -> Dict[str, Any]:
    """
    Place a LIMIT BUY order.
    
    Args:
        symbol: Stock symbol (e.g., "HK.00700")
        quantity: Number of shares (e.g., 100)
        price: Limit price per share (e.g., 400.0)
    """
    client = get_client()
    return client.place_order(symbol, quantity, price, TrdSide.BUY)
