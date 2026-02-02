from typing import Any, Dict
from ..opend.client import get_client

def get_financials(symbol: str) -> Dict[str, Any]:
    """
    Get fundamental financial data (PE, PB, Market Cap).
    
    Args:
        symbol: Stock symbol.
    """
    client = get_client()
    data = client.get_financials(symbol)
    
    # Extract key fields
    return {
        "symbol": data.get("code"),
        "pe_ttm": data.get("pe_ttm"),
        "pe_lyr": data.get("pe_lyr"), # Last Year Ratio if available
        "pb_ratio": data.get("pb_ratio"),
        "total_market_val": data.get("total_market_val"),
        "last_price": data.get("last_price")
    }
