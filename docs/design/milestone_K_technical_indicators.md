# Design Doc: Milestone K - Technical Intelligence

## 1. Goal
Provide the agent with "Technical Vision". Instead of just seeing the current price, the agent should see the *trend* and *momentum*.

## 2. New Tool: `get_technical_indicators`

### Function Signature
`get_technical_indicators(symbol: str, indicators: List[str] = ["RSI", "SMA_20", "EMA_50"], period: str = "1d", limit: int = 100)`

### Supported Indicators (Initial Set)
*   **MA**: Moving Averages (SMA, EMA). Syntax: `SMA_20`, `EMA_50`.
*   **RSI**: Relative Strength Index. Syntax: `RSI` (defaults to 14) or `RSI_14`.
*   **MACD**: Moving Average Convergence Divergence. Syntax: `MACD`.
*   **BOLL**: Bollinger Bands. Syntax: `BOLL`.
*   **VOL**: Volume MA. Syntax: `VOL_20`.

### Logic
1.  **Fetch Data**: Call internal `client.get_kline(symbol, period, limit)`.
2.  **Calculate**: Use `ta` library (or pandas logic) to calculate requested indicators on the DataFrame.
3.  **Return**: A dictionary containing the *latest* values for each indicator, plus a "signal" summary if possible (e.g. "RSI is Overbought").

### Example Output
```json
{
  "symbol": "HK.00700",
  "price": 350.2,
  "indicators": {
    "RSI_14": 72.5,
    "SMA_20": 340.1,
    "MACD": 1.2,
    "MACD_SIGNAL": 0.8
  },
  "timestamp": "2025-10-25 10:00:00"
}
```

## 3. Libraries
We will add `ta` (Technical Analysis Library) to `pyproject.toml` to handle the math robustly.

## 4. Risks
*   **Data Sufficiency**: Calculating `EMA_200` requires >200 bars. We must ensure `limit` is sufficient.
*   **Naming**: Indicator names need to be standardized (e.g., `SMA_20` vs `MA20`). We will use a parser.

## 5. Future Packaging
This module will be cleanly separated in `src/moomoo_mcp/analysis/`.
