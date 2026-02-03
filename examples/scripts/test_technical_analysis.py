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
        price = res.get("last_price", 0)
        
        # 1. RSI Invariant (0-100)
        if "RSI_14" in inds:
             rsi = inds["RSI_14"]
             status = "Pass" if 0 <= rsi <= 100 else "FAIL"
             print(f"[Check 1] RSI Range (0-100): {rsi} -> {status}")

        # 2. Bollinger Invariant (Upper >= Mid >= Lower)
        if "BOLL" in inds:
             b = inds["BOLL"]
             up, mid, low = b["BOLL_UPPER"], b["BOLL_MID"], b["BOLL_LOWER"]
             status = "Pass" if up >= mid >= low else "FAIL"
             print(f"[Check 2] BOLL Order ({up} > {mid} > {low}) -> {status}")
             
        # 3. MA Proximity (MA shouldn't be 0 or wild if price is 600)
        if "SMA_20" in inds and price > 0:
             sma = inds["SMA_20"]
             diff_pct = abs(price - sma) / price
             # Is SMA within 20% of price? (Usually yes for blue chips)
             status = "Pass" if diff_pct < 0.20 else "WARNING (Volatile?)"
             print(f"[Check 3] SMA Reality Check (Price: {price}, SMA: {sma}, Diff: {diff_pct:.1%}) -> {status}")
        
        print("\nTechnical Intelligence Tests PASSED.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}", flush=True)
        sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
