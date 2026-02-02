from moomoo_mcp.account.get_orders import get_orders
from moomoo_mcp.opend.client import get_client
import sys

def main():
    print("Checking Orders...")
    try:
        # Check orders for Tencent (used in previous test)
        symbol = "HK.00700" 
        print(f"Fetching orders for {symbol}...")
        orders = get_orders(symbol)
        
        if not orders:
            print("No orders found.")
        else:
            print(f"Found {len(orders)} orders:")
            for o in orders:
                print(f"ID: {o.get('order_id')} | Status: {o.get('order_status')} | Side: {o.get('trd_side')} | Qty: {o.get('qty')} @ {o.get('price')}")
                
        print("Done.")
    except Exception as e:
        with open("orders_error.txt", "w") as f:
            f.write(f"CRITICAL ERROR: {e}")
        print(f"Error: {e}")
        # Expected if OpenD is not running
        if "Connection failed" in str(e) or "WSAECONNREFUSED" in str(e):
             print("(Expected failure if OpenD is not running)")
        else:
             sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
