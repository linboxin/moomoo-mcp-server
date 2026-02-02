# Milestone H: Pro Tools Design

## 1. Overview
This milestone introduces "Pro" features for advanced agentic trading: modifying/canceling orders, viewing Level 2 market depth, calculating purchasing power, and checking fundamentals.

## 2. Order Management
### `cancel_order` & `modify_order`
- **Correction**: Allowing the agent to fix mistakes or adjust to market movements.
- **Client API**: 
  - `modify_order(modify_order_op, order_id, ...)`
  - `ModifyOrderOp.CANCEL` for cancellation.
  - `ModifyOrderOp.NORMAL` for changing price/qty.

## 3. Market Depth (Level 2)
### `get_order_book`
- **Insight**: View bid/ask spread and depth.
- **Client API**: `get_order_book(code)`.

## 4. Calculations
### `get_max_buyable`
- **Planning**: Determine affordablity before placing order.
- **Client API**: `acctradinginfo_query` gives `max_buy_price`, `max_sell_short`, etc. Or `trd_get_max_trd_qty` (helper).

## 5. Fundamentals
### `get_financials`
- **Analysis**: PE Ratio, EPS, Market Cap.
- **Client API**: `get_stock_basicinfo` provides real-time snapshot of fundamentals (PE_TTM, PB, etc.).

## 6. Risk Considerations
- `modify_order` must pass `RiskManager` checks if quantity/price increases exposure? 
  - *Strategy*: For now, apply risk check if `price * qty` increases.

## API Signatures
```python
def cancel_order(order_id: str) -> Dict
def modify_order(order_id: str, price: float, quantity: int) -> Dict
def get_order_book(symbol: str) -> Dict # Returns {bids: [], asks: []}
def get_max_buyable(symbol: str, price: float) -> int
def get_financials(symbol: str) -> Dict
```
