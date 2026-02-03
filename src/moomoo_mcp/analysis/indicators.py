import pandas as pd
import ta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    """
    Computes technical indicators on market data using 'ta' library.
    """
    
    @staticmethod
    def compute(df: pd.DataFrame, indicators: List[str]) -> Dict[str, Any]:
        """
        Computes requested indicators and returns the latest values.
        
        Args:
            df: DataFrame containing 'close', 'high', 'low', 'volume' columns.
            indicators: List of indicator strings (e.g. ["RSI", "SMA_20"])
            
        Returns:
            Dict of indicator names and their latest values.
        """
        if df.empty:
            return {}
            
        # Ensure column names match what 'ta' expects (it expects lowercase usually, but let's standardize)
        # Futu DF usually has 'close', 'high', etc.
        # ta lib works on Series.
        
        results = {}
        
        try:
            close = df['close']
            high = df['high']
            low = df['low']
            volume = df['volume']
            
            for ind in indicators:
                ind_upper = ind.upper()
                val = None
                
                try:
                    # Generic Moving Averages
                    if ind_upper.startswith("SMA_"):
                        # Format: SMA_20
                        period = int(ind_upper.split("_")[1])
                        val = ta.trend.SMAIndicator(close=close, window=period).sma_indicator().iloc[-1]
                        
                    elif ind_upper.startswith("EMA_"):
                        # Format: EMA_50
                        period = int(ind_upper.split("_")[1])
                        val = ta.trend.EMAIndicator(close=close, window=period).ema_indicator().iloc[-1]
                        
                    elif ind_upper.startswith("WMA_"):
                        period = int(ind_upper.split("_")[1])
                        val = ta.trend.WMAIndicator(close=close, window=period).wma().iloc[-1]

                    # Momentum
                    elif ind_upper.startswith("RSI"):
                        # Format: RSI or RSI_14
                        period = 14
                        if "_" in ind_upper:
                            period = int(ind_upper.split("_")[1])
                        val = ta.momentum.RSIIndicator(close=close, window=period).rsi().iloc[-1]
                        
                    elif ind_upper == "MACD":
                        macd = ta.trend.MACD(close=close)
                        val = {
                            "MACD_LINE": macd.macd().iloc[-1],
                            "MACD_SIGNAL": macd.macd_signal().iloc[-1],
                            "MACD_HIST": macd.macd_diff().iloc[-1]
                        }

                    # Volatility
                    elif ind_upper == "BOLL" or ind_upper == "BBANDS":
                        boll = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
                        val = {
                            "BOLL_UPPER": boll.bollinger_hband().iloc[-1],
                            "BOLL_MID": boll.bollinger_mavg().iloc[-1],
                            "BOLL_LOWER": boll.bollinger_lband().iloc[-1]
                        }
                    
                    elif ind_upper == "ATR":
                         val = ta.volatility.AverageTrueRange(high=high, low=low, close=close).average_true_range().iloc[-1]

                    # Volume
                    elif ind_upper.startswith("VOL_SMA_"):
                         period = int(ind_upper.split("_")[2])
                         val = ta.trend.SMAIndicator(close=volume, window=period).sma_indicator().iloc[-1]

                    if val is not None:
                        # Round floats for cleanliness
                        if isinstance(val, float):
                             results[ind] = round(val, 3)
                        elif isinstance(val, dict):
                             results[ind] = {k: round(v, 3) for k, v in val.items()}
                        else:
                             results[ind] = val
                    else:
                        results[ind] = "Unknown Indicator"

                except Exception as e:
                    logger.warning(f"Failed to calc {ind}: {e}")
                    results[ind] = f"Error ({e})"
                    
        except Exception as e:
             logger.error(f"Error in technical analysis: {e}")
             return {"error": str(e)}

        return results
