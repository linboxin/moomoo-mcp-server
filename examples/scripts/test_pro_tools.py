from moomoo_mcp.market_data.get_financials import get_financials
from moomoo_mcp.market_data.get_order_book import get_order_book
from moomoo_mcp.account.get_max_buyable import get_max_buyable
from moomoo_mcp.trading.buy_stock import buy_stock
from moomoo_mcp.trading.modify_order import modify_order
from moomoo_mcp.trading.cancel_order import cancel_order
from moomoo_mcp.opend.client import get_client
import sys
import time

from moomoo_mcp.config import config

def main():
    # Override max order value for testing
    config.max_order_value = 1000000.0
    
    print("Testing Pro Tools...", flush=True)
    symbol = "HK.00700" 
    
    try:
        # 1. Financials
        print(f"\n1. Fetching Financials for {symbol}...", flush=True)
        fin = get_financials(symbol)
        print(f"PE TTM: {fin.get('pe_ttm')} | PB: {fin.get('pb_ratio')} | Market Cap: {fin.get('total_market_val')}", flush=True)
        
        # 2. Max Buyable
        print(f"\n2. Max Buyable for {symbol} @ $100...", flush=True)
        # Assuming we have some cash
        qty = get_max_buyable(symbol, price=100.0)
        print(f"Max Qty: {qty}", flush=True)
        
        # 3. Order Book Ladder
        print(f"\n3. Fetching Order Book for {symbol}...", flush=True)
        ladder = get_order_book(symbol)
        print("--- LADDER START ---")
        print(ladder)
        print("--- LADDER END ---", flush=True)
        
        # 4. Modification Flow (Buy Low -> Modify -> Cancel)
        print(f"\n4. Testing Order Management Flow...", flush=True)
        
        # A. Place Limit Buy well below market price to ensure it sits in book
        print("  A. Placing Limit Buy @ $100...", flush=True)
        order = buy_stock(symbol, 100, price=100.0, order_type="LIMIT")
        order_id = order.get("order_id")
        
        if not order_id:
             print("Failed to get order_id. Skipping modification test.", flush=True)
        else:
             print(f"  Order Placed. ID: {order_id}", flush=True)
             time.sleep(2) # Wait for processing
             
             # B. Modify Price
             print("  B. Modifying Price to $101...", flush=True)
             mod_res = modify_order(order_id, price=101.0, quantity=100)
             print(f"  Modify Result: {mod_res.get('order_id')}", flush=True) # Should handle checking status
             time.sleep(2)
             
             # C. Cancel
             print("  C. Canceling Order...", flush=True)
             cancel_res = cancel_order(order_id)
             print(f"  Cancel Result: {cancel_res.get('order_id')}", flush=True)

        print("\nPro Tools Tests Completed.", flush=True)
        
        
    except Exception as e:
        with open("pro_error.txt", "w") as f:
            f.write(f"CRITICAL ERROR: {e}")
        print(f"Error: {e}", flush=True)
        if "Connection failed" in str(e):
             print("(Expected failure if OpenD is not running)")
        else:
             sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
