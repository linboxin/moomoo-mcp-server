from typing import Any, Dict
from futu import TrdSide, OrderType
from ..opend.client import get_client

def buy_stock(symbol: str, quantity: int, price: float = 0.0, order_type: str = "LIMIT") -> Dict[str, Any]:
    """
    Place a BUY order.

    Args:
        symbol: Stock symbol (e.g., "HK.00700")
        quantity: Number of shares (e.g., 100)
        price: Price per share. Required for LIMIT orders. Ignored for MARKET orders.
        order_type: "LIMIT" or "MARKET" (Default: "LIMIT")
    """
    client = get_client()
    
    # Map string param to futu Enum
    trd_order_type = OrderType.NORMAL
    if order_type.upper() == "MARKET":
        trd_order_type = OrderType.MARKET
        
    return client.place_order(symbol, quantity, price, TrdSide.BUY, order_type=trd_order_type)
