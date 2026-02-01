from moomoo_mcp.opend.client import get_client
import sys

def main():
    print("Initializing MoomooClient...")
    try:
        client = get_client()
        print("Connecting to OpenD...")
        client.connect()
        print("Connected!")
        
        symbol = "00700" # Test normalization (should become HK.00700)
        print(f"Fetching quote for {symbol}...")
        quote = client.get_quote(symbol)
        print("Quote received:")
        print(quote)
        
        client.close()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
