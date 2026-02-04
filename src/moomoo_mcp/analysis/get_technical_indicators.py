from typing import List, Dict, Any, Optional
import pandas as pd
from ..opend.client import get_client
from .indicators import TechnicalAnalysis
from ..utils.symbols import normalize_symbol

def get_technical_indicators(
    symbol: str, 
    indicators: List[str] = ["RSI_14", "SMA_20", "EMA_50", "MACD"], 
    period: str = "1d", 
    limit: int = 200
) -> Dict[str, Any]:
    """
    Calculates technical indicators for a stock.
    
    Args:
    Args:
        symbol: Stock symbol (e.g., "HK.00700", "US.AAPL").
        indicators: List of technical indicators to calculate. 
                    - Moving Averages: "SMA_20", "EMA_50", "WMA_100" (replace number with any period).
                    - Momentum: "RSI_14", "MACD".
                    - Volatility: "BOLL" (Bollinger Bands), "ATR".
                    - Volume: "VOL_SMA_20".
        period: Timeframe of the chart. Options: "1m", "5m", "15m", "30m", "60m" (Hourly), "1d" (Daily), "1w" (Weekly).
        limit: Number of bars to fetch (default 200). Increase this if calculating long-period MAs (e.g. use 300 for SMA_200).
    """
    client = get_client()
    symbol = normalize_symbol(symbol)
    
    # 1. Fetch Historical Data (K-Line)
    # Map '1d' string to K_DAY etc if needed, but get_kline wrapper handles basic strings?
    # Let's check client.get_kline signature. It expects "K_DAY", "K_1M" usually.
    # We should map friendly strings to client constants here for ease of use.
    
    ktype_map = {
        "1d": "K_DAY",
        "1w": "K_WEEK",
        "1m": "K_1M",
        "5m": "K_5M",
        "15m": "K_15M",
        "30m": "K_30M",
        "60m": "K_60M",
        "1h": "K_60M"
    }
    ktype = ktype_map.get(period.lower(), "K_DAY")
    
    # Fetch data as list of dicts
    klines = client.get_kline(symbol, ktype=ktype, limit=limit)
    
    if not klines:
        return {"error": "No K-Line data found", "symbol": symbol}
        
    # 2. Key Data to DataFrame
    df = pd.DataFrame(klines)
    
    # 3. Compute
    tech_data = TechnicalAnalysis.compute(df, indicators)
    
    # 4. Result
    return {
        "symbol": symbol,
        "period": period,
        "last_price": klines[-1].get('close'),
        "timestamp": klines[-1].get('time_key'),
        "indicators": tech_data
    }
