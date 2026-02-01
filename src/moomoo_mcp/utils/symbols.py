from ..config import config

def normalize_symbol(symbol: str) -> str:
    """
    Ensures symbol has a market prefix.
    If missing, prepends the configured default market (e.g., "HK.").
    Example: "00700" -> "HK.00700"
    """
    if "." in symbol:
        return symbol.upper()
    
    return f"{config.default_market}.{symbol}".upper()
