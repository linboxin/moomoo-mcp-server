from futu import OpenQuoteContext, SysConfig
import sys

def main():
    print("Testing OpenD Connection...", flush=True)
    try:
        host = "127.0.0.1"
        port = 11111
        print(f"Connecting to {host}:{port}...", flush=True)
        ctx = OpenQuoteContext(host=host, port=port)
        print("Context Created.", flush=True)
        
        ret, data = ctx.get_global_state()
        print(f"Global State: {ret}", flush=True)
        
        ctx.close()
        print("Closed.", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)
    except BaseException as e:
        print(f"BaseException: {e}", flush=True)

if __name__ == "__main__":
    main()
