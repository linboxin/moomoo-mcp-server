# Milestone D: Account Tools Design

## 1. Overview
**Goal**: Expose account information (positions, balance) via MCP tools.
**Scope**:
- Enable `OpenTradeContext` in `MoomooClient`.
- Implement `unlock_trade` logic.
- Tools: `account.get_positions`, `account.get_balance`.

## 2. Architecture & Components
### Modified Components
- `src/moomoo_mcp/opend/client.py`:
  - Re-enable `OpenTradeContext`.
  - Add `unlock_trade()` method using `config.pwd`.
  - Add `get_details()` and `get_position_list()`.

### New Components
- `src/moomoo_mcp/account/get_positions.py`
- `src/moomoo_mcp/account/get_balance.py`

## 3. API & Data Models
### Tool: `account.get_balance`
**Input**:
- None (or optional `currency` filter)

**Output**:
```json
{
  "total_assets": 10000.0,
  "cash": 5000.0,
  "market_value": 5000.0,
  "buying_power": 20000.0,
  "currency": "USD"
}
```

### Tool: `account.get_positions`
**Input**:
- None (or optional `filter_empty` bool)

**Output**:
List of:
```json
{
  "symbol": "US.AAPL",
  "qty": 10,
  "cost_price": 145.0,
  "market_value": 1500.0,
  "pl_val": 50.0,
  "pl_ratio": 3.4
}
```

## 4. Implementation Details
- **Unlock Logic**: On `connect()`, if `config.pwd` is set, calls `unlock_trade(config.pwd)`.
- **Context**: Need to determine if we use `OpenUSTradeContext`, `OpenHKTradeContext`, etc.
  - *Challenge*: Futu separates trade contexts by market (US, HK, CN).
  - *Decision*: The user only has **HK Quote Rights** and likely HK Trade rights.
  - *Refinement*: We will support `OpenHKTradeContext` primarily for this MVP.
  - **Strategy**: Instantiate `OpenHKTradeContext` triggered by `TRADING_MARKET=HK` (or default).
  - We will add `TRADING_MARKET` to config (default "HK").

## 5. Risk & Safety
- **Read-Only**: These tools are read-only but require "Unlock" which is a sensitive operation.
- **Privacy**: Balance info is sensitive.

## 6. Testing Plan
- **Verification**: `examples/scripts/account_snapshot.py`.
