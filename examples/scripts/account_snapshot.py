from moomoo_mcp.account.get_positions import get_positions
from moomoo_mcp.account.get_balance import get_balance
import sys

def main():
    print("Fetching Account Snapshot...")
    try:
        print("\n--- Balance ---")
        balance = get_balance()
        # Print key fields
        print(f"Total Assets: {balance.get('total_assets')}")
        print(f"Cash: {balance.get('cash')}")
        print(f"Market Value: {balance.get('market_val')}")
        
        print("\n--- Positions ---")
        positions = get_positions()
        if not positions:
            print("No positions found.")
        else:
            for p in positions:
                print(f"{p.get('code')} | Qty: {p.get('qty')} | Cost: {p.get('cost_price')} | MktVal: {p.get('market_val')}")
                
        print("\nDone.")
    except Exception as e:
        print(f"Error: {e}")
        # Expected if OpenD is not running or trade unlock fails
        if "Connection failed" in str(e) or "WSAECONNREFUSED" in str(e):
             print("(Expected failure if OpenD is not running)")
        else:
             sys.exit(1)
    finally:
        from moomoo_mcp.opend.client import get_client
        get_client().close()

if __name__ == "__main__":
    main()
