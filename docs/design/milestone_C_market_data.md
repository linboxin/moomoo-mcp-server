# Milestone C: Market Data Tools Design

## 1. Overview
**Goal**: Expose market data retrieval capabilities via MCP tools.
**Scope**:
- `market_data.get_quote`: Real-time snapshot.
- `market_data.get_kline`: Historical/recent candlesticks.
- Updates to `MoomooClient` to support klines.

## 2. Architecture & Components
### Modified Components
- `src/moomoo_mcp/opend/client.py`: Add `get_kline` method.
- `src/moomoo_mcp/server.py`: Register new tools.

### New Components
- `src/moomoo_mcp/market_data/get_quote.py`
- `src/moomoo_mcp/market_data/get_kline.py`
- `src/moomoo_mcp/utils/time.py` (Timeframe conversion helpers)

## 3. API & Data Models

### Tool: `market_data.get_quote`
**Input**:
- `symbol` (str): e.g., "US.AAPL", "HK.00700".

**Output**:
```json
{
  "symbol": "US.AAPL",
  "last_price": 150.0,
  "open": 148.0,
  "high": 151.0,
  "low": 147.0,
  "volume": 1000000,
  "turnover": 150000000,
  "timestamp": "2023-10-27 10:00:00"
}
```

### Tool: `market_data.get_kline`
**Input**:
- `symbol` (str)
- `period` (str): "1m", "5m", "15m", "30m", "60m", "1d", "1w", "1M" (Map to Futu `KLType`).
- `limit` (int): Default 100, Max 1000.

**Output**:
List of:
```json
{
  "time_key": "2023-10-27 10:00:00",
  "open": 150.0,
  "close": 150.5,
  "high": 151.0,
  "low": 149.9,
  "volume": 500
}
```

## 4. Implementation Details
- **Normalization**: OpenD returns Pandas DataFrames. valid columns must be extracted and converted to standard Python types (float, str) before returning.
- **Validation**: Check if `symbol` follows "MARKET.CODE" format (simple regex). Check `period` against allowed list.

## 5. Risk & Safety
- **Read-Only**: These tools do not modify account state.
- **Performance**: Large kline requests can be slow. Enforce `limit` <= 1000.

## 6. Testing Plan
- **Unit**: Mock `client.get_kline` returns.
- **Integration**: `examples/scripts/quick_kline.py`.
