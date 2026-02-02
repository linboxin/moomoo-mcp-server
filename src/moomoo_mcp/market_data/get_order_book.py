from typing import Any, Dict
from ..opend.client import get_client

def get_order_book(symbol: str) -> str:
    """
    Get the Level 2 Order Book (Depth) as a visual ladder.
    Returns a formatted string for easy visualization.
    
    Args:
        symbol: Stock symbol.
    """
    client = get_client()
    data = client.get_order_book(symbol)
    
    # Format as Ladder
    output = []
    output.append(f"Order Book for {symbol}")
    output.append("🔴 ASKS (Sellers)")
    
    # Asks: usually sort ascending (lowest sell price first). 
    # Moomoo returns 'Ask' list. Typically index 0 is best ask (lowest price).
    # We want to show highest price at top? No, usually ladder shows:
    # High Ask
    # ...
    # Low Ask (Best Ask)
    # ---
    # High Bid (Best Bid)
    # ...
    # Low Bid
    
    # Extract data (DataFrames or lists) in client.py gave us raw structure.
    # Futu get_order_book returns dict with 'Ask': List of (price, volume, order_count), 'Bid': List...
    asks = data.get('Ask', [])
    bids = data.get('Bid', [])
    
    # Asks: Reverse them so highest price is top, lowest (best) is bottom of ASK section
    for ask in reversed(asks):
        price = ask[0]
        vol = ask[1]
        output.append(f"{price:>10.3f} x {vol:<6}")
        
    output.append("-" * 20)
    
    # Bids: Best bid (highest price) first (default order usually), then descending
    output.append("🟢 BIDS (Buyers)")
    for bid in bids:
        price = bid[0]
        vol = bid[1]
        output.append(f"{price:>10.3f} x {vol:<6}")
        
    return "\n".join(output)
