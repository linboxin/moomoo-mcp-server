from moomoo_mcp.analysis.get_technical_indicators import get_technical_indicators
from moomoo_mcp.opend.client import get_client
import sys
import json

def main():
    print("=== Demo: Technical Analysis Flexibility ===\n")
    
    try:
        # Scenario 1: HK Short Term (Alibaba) on HOURLY chart
        print("1. HK.09988 (Hourly - 60m): Checking Short Term Trend...")
        res_hour = get_technical_indicators(
             "HK.09988", 
             indicators=["RSI_9", "EMA_20"], # Fast RSI (9) for intraday
             period="60m",
             limit=100
        )
        print(json.dumps(res_hour, indent=2))
        
        # Scenario 2: HK Giant (Tencent) on WEEKLY chart (Long Term Trend)
        print("\n2. HK.00700 (Weekly - 1w): Checking Long Term Trend...")
        res_week = get_technical_indicators(
             "HK.00700", 
             indicators=["SMA_200", "BOLL"], # Long term SMA
             period="1w",
             limit=300 # Need more data for SMA_200
        )
        print(json.dumps(res_week, indent=2))

        # Scenario 3: Crypto/Futures? (If supported by account, let's stick to stocks for safety but show config)
        print("\n3. Customizing Indicators (RSI_21 vs RSI_14)...")
        # Just showing that we can change the 'option' (parameter) of the indicator
        print("   You can request 'RSI_21', 'SMA_100', 'VOL_SMA_5' etc.")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
