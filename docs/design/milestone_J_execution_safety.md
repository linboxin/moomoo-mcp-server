# Design Doc: Milestone J - Execution & Safety

## 1. Goal
Implement 3 critical tools for "closing the loop" on trading, safety, and efficiency:
1.  **Execution Gap**: `get_deals` to see actual trade execution prices.
2.  **Safety Gap**: `get_margin_ratio` (or enhanced balance) to monitor liquidation risk.
3.  **Efficiency**: `get_market_snapshot` for low-latency batch quotes.

## 2. API Design

### 2.1. `get_deals`
Retrieves list of executed deals for the day (or recent period).
- **Function**: `get_deals(symbol: Optional[str] = None)`
- **Output**: List of dictionaries:
  ```json
  [
    {"deal_id": "123", "symbol": "HK.00700", "side": "BUY", "price": 100.50, "qty": 100, "status": "Filled", "time": "..."}
  ]
  ```
- **Underlying**: `trade_ctx.deal_list_query()`

### 2.2. `get_margin_ratio`
Retrieves account risk details.
- **Function**: `get_margin_ratio()`
- **Output**: Dictionary with risk metrics.
  ```json
  {
    "margin_call_margin": 1000.0,
    "maintenance_margin": 5000.0,
    "risk_level": "Safe", # derived
    "margin_ratio": 0.0 # if available directly or calculated
  }
  ```
- **Underlying**: `trade_ctx.accinfo_query()` or `funds_query()`. `accinfo_query` typically has more potential for detailed risk status in some markets, but `funds` has `cash`, `market_val`, and often risk ratios. We will inspect `funds` more closely or `accinfo`. (Update: Futu's `accinfo_query` is often for account list, `funds` is for details. Let's check `get_funds` return fields for `risk_status` or similar).

### 2.3. `get_market_snapshot`
Batch fetch for efficiency.
- **Function**: `get_market_snapshot(symbols: List[str])`
- **Output**: List of snapshot data.
  ```json
  [
    {"symbol": "HK.00700", "price": 100.0, "last_updated": "..."},
    {"symbol": "US.AAPL", "price": 150.0, ...}
  ]
  ```
- **Underlying**: `quote_ctx.get_market_snapshot(symbol_list)`.

## 3. Implementation Steps
1.  Analyze `get_funds` response in `client.py` to see if it already contains margin info. If not, investigate `accinfo_query`.
2.  Implement `get_deals` in `client.py` and `trading/get_deals.py`.
3.  Implement `get_market_snapshot` in `market_data/get_market_snapshot.py`.
4.  Implement `get_margin_ratio` (wrapping appropriate client method).

## 4. Risks
- **Snapshot Limits**: `get_market_snapshot` has a limit (e.g., 400 symbols). Tool should handle chunks if list is huge (unlikely for agent usage, but good practice).
- **Margin Data**: Different markets (HK/US) might have different field names for margin. We need to normalize.

## 5. Verification
- `test_execution_safety.py`:
    - Place order (paper).
    - Call `get_deals` to see it.
    - Call `get_margin_ratio`.
    - Call `get_market_snapshot(["HK.00700", "US.AAPL"])`.
