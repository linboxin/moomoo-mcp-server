from moomoo_mcp.system.run_diagnostics import run_diagnostics
from moomoo_mcp.opend.client import get_client
import sys
import json

def main():
    print("Running Diagnostics...", flush=True)
    try:
        # Run self-test
        report_json = run_diagnostics("HK.00700")
        
        # Pretty print
        report = json.loads(report_json)
        print(json.dumps(report, indent=2), flush=True)
        
        if not report.get("ok"):
             print("\nDiagnostics reported failures.")
             # sys.exit(1) # Optional: fail script if diagnostics fail
        else:
             print("\nDiagnostics PASSED.")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}", flush=True)
        sys.exit(1)
    finally:
        get_client().close()

if __name__ == "__main__":
    main()
