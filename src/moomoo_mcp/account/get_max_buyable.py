from typing import Any
from ..opend.client import get_client

def get_max_buyable(symbol: str, price: float = 0.0) -> str:
    """
    Calculate the maximum number of shares you can buy.
    If 0, attempts to explain why (e.g. insufficient cash for lot size).
    
    Args:
        symbol: Stock symbol (e.g., "HK.00700")
        price: The price you intend to buy at.
    """
    client = get_client()
    data = client.get_max_buyable(symbol, price)
    qty = int(data.get("max_buy_qty", 0))
    
    if qty > 0:
        return str(qty)
        
    # If 0, investigate why
    reason = "Unknown"
    try:
        # 1. Get Lot Size & Price
        quote = client.get_market_snapshot([symbol]) # returns list of dicts or dict
        # client.get_market_snapshot returns dict per row in get_financials, but here client returns raw from ctx usually? 
        # Wait, get_financials implemented wrapper. Client.get_market_snapshot isn't wrapped in client.py yet?
        # Ah, in get_financials I called `client._quote_ctx.get_market_snapshot`.
        # client.py has `get_financials` but not specific `get_market_snapshot` wrapper except inside get_financials.
        # But I can access `get_financials` which returns `total_market_val`. 
        # I should probably expose `get_lot_size` or uses `get_quote`?
        # `get_quote` returns `lot_size`? Let's check `get_quote` implementation.
        # It calls `get_stock_quote`. `StockQuote` object usually has `lot_size`.
        
        qt = client.get_quote(symbol)
        lot_size = qt.get("lot_size", 0)
        curr_price = qt.get("last_price", 0.0)
        if price <= 0: price = curr_price
        
        # 2. Get Balance
        bal = client.get_balance()
        power = bal.get("power", 0.0)
        cash = bal.get("cash", 0.0)
        
        cost_per_lot = price * lot_size
        
        if lot_size == 0:
             reason = "Invalid Lot Size (0)"
        elif power < cost_per_lot:
             reason = f"Insufficient Buying Power for min lot size of {lot_size}. Cost: {cost_per_lot:.2f} | Power: {power:.2f}"
        else:
             reason = f"Power ({power}) >= Cost ({cost_per_lot}), but Max is 0. Possible position limit or suspended?"
             
    except Exception as e:
        reason = f"Could not determine reason ({e})"
        
    return f"Max Qty: 0 (Reason: {reason})"
