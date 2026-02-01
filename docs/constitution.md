# Constitution & Engineering Rules

## 0. Process
- **SDD First**: For any non-trivial feature, create a design document in `docs/design/` using the template before writing code.


## 1. Core Philosophy
- **Safety First**: Never enable live trading by default. Always respect risk limits.
- **Simplicity**: Maintain a readable, structured codebase. Each tool should be small and focused.
- **Reliability**: Robust error handling and logging are mandatory.

## 2. Architecture Constraints
- **OpenD Isolation**: All OpenD specific logic must reside in `src/moomoo_mcp/opend/client.py`. No other module should talk to OpenD directly.
- **Risk Isolation**: Risk logic goes in `src/moomoo_mcp/risk/`. Do not scatter safety checks in trading modules.
- **Tool Structure**: Each tool exports a `register(mcp, client)` function or is decorated in `server.py` delegating to the module.

## 3. Tech Stack & Standards
- **Framework**: FastMCP for tool definitions.
- **Type Safety**: Type hints are mandatory.
- **Linting**: Ruff + Black standards.
- **Dependencies**: Use `pyproject.toml`.
- **Outputs**: Return JSON-serializable dictionaries. **NO** pandas DataFrames in tool outputs.

## 4. Safety & Risk Policies
- **Default Mode**: Paper trading (`MOOMOO_ENV=paper`).
- **Caps**: Respect `max_order_notional_usd`, `max_order_qty`, etc.
- **Guardrails**: `place_order` must call `preview_order` internally or verifying checks if not done.
- **Confirmation**: If `require_confirm_token` is true, enforce it.

## 5. Implementation Rules
- **Validation**: Always validate `symbol`, `market`, and `timeframe` inputs.
- **Logging**: Structured logs for every tool call (inputs, latency, success/error).
- **Secrets**: Never commit secrets or API keys. Use `.env`.

## 6. Testing
- **Unit Tests**: Risk logic must be unit tested (`tests/test_risk.py`).
- **Integration**: Use `examples/scripts/` for connectivity tests.
