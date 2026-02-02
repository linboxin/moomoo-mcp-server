from moomoo_mcp.market_data.get_option_chain import get_option_chain
from moomoo_mcp.trading.buy_stock import buy_stock
from moomoo_mcp.opend.client import get_client
import sys
from datetime import datetime, timedelta

def main():
    print("Testing Advanced Features...", flush=True)
    try:
        # 1. Option Chain
        symbol = "HK.00700"
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        print(f"\n1. Fetching Option Chain for {symbol} ({start_date} to {end_date})...", flush=True)
        options = get_option_chain(symbol, start_date, end_date)
        
        if not options:
            print("No options found (or market closed/no data).", flush=True)
        else:
            print(f"Found {len(options)} options.", flush=True)
            # Print first 2
            for o in options[:2]:
                print(f"Option: {o}", flush=True)

        # 2. Market Order (Risk Check Test)
        # We won't actually toggle Market Order efficiently in Paper unless supported.
        # But we trace the call path.
        print(f"\n2. Placing MARKET Buy Order for {symbol}...", flush=True)
        
        # Note: We expect this might fail in Paper Environment if Market Orders aren't fully supported
        # or if the price is 0 and quote fails. But we want to test the execution path.
        try:
            res = buy_stock(symbol, 100, price=0.0, order_type="MARKET")
            print(f"Market Order Result: {res}", flush=True)
        except Exception as e:
            print(f"Market Order Failed (Expected Risk/Env Error): {e}", flush=True)

        print("\nAdvanced Tests Completed.", flush=True)
        
    except Exception as e:
        with open("advanced_error.txt", "w") as f:
            f.write(f"CRITICAL ERROR: {e}")
        print(f"Error: {e}", flush=True)
        if "Connection failed" in str(e) or "WSAECONNREFUSED" in str(e):
             print("(Expected failure if OpenD is not running)")
        else:
             sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
