# Milestone G: Advanced Features Design

## 1. Overview
This milestone extends the trading capabilities to support **Market Orders** and **Options Trading**. It builds upon the Risk Management (Milestone E) and Basic Trading (Milestone F) layers.

## 2. Market Orders
### Requirement
Allow the agent to execute trades immediately at the best available price (`OrderType.MARKET`).

### Design
- **Client**: Update `place_order` to accept `order_type`.
- **Risk Management**:
  - *Problem*: Market orders have no fixed `price`.
  - *Solution*: `place_order` must fetch the *Real-time Quote* (`get_quote`) to estimate the `estimated_value` (`qty * current_price`) before passing it to `RiskManager`.
- **Tools**: `buy_stock` and `sell_stock` will accept an optional `order_type` argument.

## 3. Options Data
### Requirement
Allow the agent to query Option Chains (Calls/Puts) for a given stock and expiration.

### Design
- **Client**: Add `get_option_chain(symbol, start_date, end_date)`.
  - Uses `OpenQuoteContext.request_history_kline`? No, specific `get_option_chain` API or `get_option_chain` in futu.
  - *Futu API*: `OpenQuoteContext.get_option_chain(stock_code, begin_time, end_time, data_filter=None)`.
- **Tool**: `get_option_chain(symbol, filter_date)`.
  - Returns simplified list: `code`, `name`, `strike_price`, `option_type` (Call/Put), `maturity_time`.

## 4. API Changes
### `moomoo_mcp.opend.client.MoomooClient`
```python
def place_order(self, symbol, quantity, price, side, order_type=OrderType.NORMAL):
    if order_type == OrderType.MARKET:
        current_price = self.get_quote(symbol)['last_price']
        RiskManager.check_order(symbol, quantity, current_price)
    else:
        RiskManager.check_order(symbol, quantity, price)
    # ...
```

### `moomoo_mcp.trading.buy_stock`
```python
def buy_stock(symbol, quantity, price=0.0, order_type="LIMIT"):
    # ...
```
