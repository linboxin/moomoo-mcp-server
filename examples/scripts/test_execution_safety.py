from moomoo_mcp.trading.get_deals import get_deals
from moomoo_mcp.account.get_margin_ratio import get_margin_ratio
from moomoo_mcp.market_data.get_market_snapshot import get_market_snapshot
from moomoo_mcp.opend.client import get_client
import sys
import json

def main():
    print("Testing Execution & Safety Tools...", flush=True)
    try:
        # 1. Market Snapshot
        print("\n1. Testing get_market_snapshot...", flush=True)
        snaps = get_market_snapshot(["HK.00700", "HK.09988"])
        print(f"Snapshot Count: {len(snaps)}")
        if len(snaps) > 0:
            print(f"Sample: {snaps[0].get('code')} Price: {snaps[0].get('last_price')}", flush=True)
        
        # 2. Margin Ratio
        print("\n2. Testing get_margin_ratio...", flush=True)
        margin = get_margin_ratio()
        print(f"Total Assets: {margin.get('total_assets')}")
        print(f"Power: {margin.get('power')}")
        if 'risk_status' in margin:
            print(f"Risk Status: {margin.get('risk_status')}")
            
        # 3. Deals
        print("\n3. Testing get_deals...", flush=True)
        try:
            deals = get_deals() # Defaults to all for today
            print(f"Deals Count: {len(deals)}")
            if len(deals) > 0:
                 print(f"Last Deal: {deals[0]}")
        except Exception as e:
            if "Simulated trade does not support" in str(e):
                 print(f"WARNING: get_deals skipped (Not supported in Simulation).")
            else:
                 raise e
             
        print("\nExecution & Safety Tests PASSED.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}", flush=True)
        sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
