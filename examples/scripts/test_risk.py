from moomoo_mcp.risk.manager import RiskManager, RiskError
import sys

def main():
    print("Testing Risk Manager...")
    
    # Test 1: Small order (Should PASS)
    symbol = "HK.00700"
    qty = 1
    price = 400.0 # Value = 400
    print(f"\nTest 1: {qty} * {price} = {qty*price}")
    try:
        if RiskManager.check_order(symbol, qty, price):
             print("PASS (Expected)")
    except RiskError as e:
        print(f"FAIL (Unexpected): {e}")
        sys.exit(1)

    # Test 2: Large order (Should FAIL)
    qty = 100
    price = 400.0 # Value = 40,000 (Limit is 2000)
    print(f"\nTest 2: {qty} * {price} = {qty*price}")
    try:
        RiskManager.check_order(symbol, qty, price)
        print("FAIL (Unexpected success)")
        sys.exit(1)
    except RiskError as e:
        print(f"PASS (Expected Rejection): {e}")

    print("\nRisk Manager Tests Completed Successfully.")

if __name__ == "__main__":
    main()
