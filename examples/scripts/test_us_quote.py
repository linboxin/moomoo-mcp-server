from moomoo_mcp.market_data.get_quote import get_quote
from moomoo_mcp.opend.client import get_client
import sys

def main():
    print("Testing US Quote...", flush=True)
    try:
        # Quote uses OpenQuoteContext (shared), so this should work if connected.
        # But this confirms connection is healthy after switch.
        symbol = "US.AAPL"
        print(f"Fetching quote for {symbol}...")
        quote = get_quote(symbol)
        print(f"Quote: {quote.get('last_price')} (Success)", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
        if "Connection failed" in str(e):
             print("(Expected failure if OpenD is not running)")
        else:
             sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
