# Milestone B: OpenD Connectivity Design

## 1. Overview
**Goal**: Create a robust wrapper around the `futu-api` to manage connections to Moomoo OpenD.
**Scope**:
- `opend/client.py`: The single point of contact for OpenD.
- Support for `SysConfig` settings (host/port/pwd).
- Error mapping (OpenD error -> MCP error).

## 2. Architecture
- **MoomooClient Class**:
  - Manages `OpenQuoteContext` and `OpenTradeContext`.
  - Lazy initialization (connect on first use or server start).
  - Handles reconnection logic (if `futu-api` drops).
  - Thread-safety if needed (FastMCP uses threads for sync tools).

## 3. API & Data Models
### `opend.client.MoomooClient`
```python
class MoomooClient:
    def __init__(self, host: str, port: int, pwd: str = ""): ...

    def get_quote(self, symbol: str) -> dict: ...
    # Wrapper for quote_ctx.get_stock_quote()

    def get_kline(self, symbol: str, ktype: str, limit: int) -> list[dict]: ...
    # Wrapper for quote_ctx.get_cur_kline()
```

### Configuration
- `OPEND_HOST`, `OPEND_PORT` from env.

## 4. Implementation Details
- **Dependency**: `futu-api`.
- **Error Handling**: Catch `FutuError`, map to `McpError` with clear messages.
- **Logging**: Log every call to OpenD with latency.

## 5. Risk & Safety
- **Authentication**: `pwd` encryption is handled by OpenD, we pass it clearly (local trust).
- **Rate Limits**: `futu-api` has internal frequency limits; we should catch "Frequency limit" errors.

## 6. Testing Plan
- **Manual**: `examples/scripts/quick_quote.py`.
- **Unit**: Mock `OpenQuoteContext` to test wrapper logic without real OpenD.
