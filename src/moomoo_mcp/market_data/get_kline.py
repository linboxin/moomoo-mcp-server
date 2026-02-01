from typing import Any, Dict, List
from futu import KLType
from ..opend.client import get_client

# Map easy strings to Futu KLType
PERIOD_MAP = {
    "1m": KLType.K_1M,
    "3m": KLType.K_3M,
    "5m": KLType.K_5M,
    "15m": KLType.K_15M,
    "30m": KLType.K_30M,
    "60m": KLType.K_60M,
    "1d": KLType.K_DAY,
    "1w": KLType.K_WEEK,
    "1M": KLType.K_MON,
    "1y": KLType.K_YEAR,
}

def get_kline(symbol: str, period: str = "1d", limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get historical candlestick (k-line) data.
    
    Args:
        symbol: Security code, e.g. "US.AAPL".
        period: Timeframe. Allowed: 1m, 3m, 5m, 15m, 30m, 60m, 1d, 1w, 1M, 1y. Default: 1d.
        limit: Number of candles to return. Max 1000. Default 100.
    """
    # Validation
    if period not in PERIOD_MAP:
        raise ValueError(f"Invalid period: {period}. Allowed: {list(PERIOD_MAP.keys())}")
    
    ktype = PERIOD_MAP[period]
    
    # Cap limit
    if limit > 1000:
        limit = 1000
        
    client = get_client()
    data = client.get_kline(symbol, ktype=ktype, limit=limit)
    return data
