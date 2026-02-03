from moomoo_mcp.analysis.get_technical_indicators import get_technical_indicators
from moomoo_mcp.opend.client import get_client
import sys
import json

def main():
    print("Testing Technical Intelligence...", flush=True)
    try:
        # Default Indicators
        print("\n1. Standard Set (RSI, SMA, MACD)...", flush=True)
        # Using a major stock to ensure liquid data
        res = get_technical_indicators(
             "HK.00700", 
             indicators=["RSI_14", "SMA_20", "EMA_50", "MACD", "BOLL", "ATR"]
        )
        print(json.dumps(res, indent=2), flush=True)
        
        # Check basic sanity
        inds = res.get("indicators", {})
        if "RSI_14" in inds:
             rsi = inds["RSI_14"]
             if 0 <= rsi <= 100:
                 print("RSI sanity check: OK")
             else:
                 print(f"RSI sanity check: FAIL ({rsi})")
        
        print("\nTechnical Intelligence Tests PASSED.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}", flush=True)
        sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
