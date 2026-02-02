try:
    print("Importing MoomooClient...")
    from moomoo_mcp.opend.client import MoomooClient
    print("MoomooClient imported.")
    
    print("Instantiating Client...")
    c = MoomooClient()
    print("Client instantiated.")
    
    print("Importing RiskManager...")
    from moomoo_mcp.risk.manager import RiskManager
    print("RiskManager imported.")
except Exception as e:
    print(f"Error: {e}")
