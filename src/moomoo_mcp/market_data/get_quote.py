from typing import Any, Dict
from mcp.server.fastmcp import Context
from ..opend.client import get_client

def get_quote(symbol: str) -> Dict[str, Any]:
    """
    Get a real-time snapshot quote for a security.
    
    Args:
        symbol: Security code, e.g. "US.AAPL", "HK.00700".
    """
    client = get_client()
    data = client.get_quote(symbol)
    return data
