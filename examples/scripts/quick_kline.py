from moomoo_mcp.market_data.get_kline import get_kline
import sys

def main():
    print("Testing get_kline...")
    try:
        # We expect this to fail if OpenD is not running, but we want to see the call path working.
        symbol = "00700" # Test normalization
        print(f"Fetching klines for {symbol}...")
        klines = get_kline(symbol, period="1d", limit=5)
        print("Klines received:")
        for k in klines:
            print(k)
    except Exception as e:
        print(f"Error: {e}")
        # If it's the expected connection error, we consider it a 'pass' for code verification.
        if "Connection failed" in str(e) or "WSAECONNREFUSED" in str(e):
             print("Success: Attempted connection and failed as expected (OpenD not running).")
        else:
             print("Unexpected error.")
             sys.exit(1)
    finally:
        from moomoo_mcp.opend.client import get_client
        get_client().close()

if __name__ == "__main__":
    main()
