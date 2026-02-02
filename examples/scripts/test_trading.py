from moomoo_mcp.trading.buy_stock import buy_stock
from moomoo_mcp.opend.client import get_client
import sys

import logging

# Suppress INFO logs to see errors clearly
logging.basicConfig(level=logging.ERROR)

def main():
    print("Testing Trading Tools (Paper Env)...")
    try:
        # Adjust config for test
        from moomoo_mcp.config import config
        config.max_order_value = 1000000.0
        
        # Test Buy Order
        # Tencent (00700) lot size is 100
        symbol = "HK.00700"
        qty = 100
        price = 400.0 
        
        print(f"Placing Buy Order: {qty} {symbol} @ {price}", flush=True)
        result = buy_stock(symbol, qty, price)
        print("buy_stock returned", flush=True)
        
        print("\nOrder Result:", flush=True)
        print(result, flush=True)
        
        if result.get('order_id'):
            print("\nSUCCESS: Order placed successfully.")
        else:
            print("\nFAIL: No order ID returned.")
            
    except Exception as e:
        with open("error.txt", "w") as f:
            f.write(f"CRITICAL ERROR: {e}")
        
        if "Connection failed" in str(e) or "WSAECONNREFUSED" in str(e):
             print("(Expected failure if OpenD is not running)")
        else:
             sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
