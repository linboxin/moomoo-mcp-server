# Moomoo MCP Server

An MCP (Model Context Protocol) server that connects to **Moomoo OpenD** to provide market data and trading capabilities to LLMs (like Claude, Gemini, etc.).

## Features

### Market Data
- **Real-time Quotes**: Fetch live snapshots (price, volume, turnover) for stocks.
- **Historical K-Lines**: Retrieve candlestick data (Daily, 1m, 5m, etc.) for technical analysis.
- **Auto-Subscription**: Automatically handles Moomoo's subscription limits so you don't have to manually manage them.
- **Symbol Normalization**: Smartly handles symbols like `00700` (auto-converts to `HK.00700` based on default market).

### Account & Assets
- **Positions**: View your current stock holdings, quantities, and P/L.
- **Balance**: Check account cash, market value, and purchasing power.
- **Paper Trading Ready**: Automatically detects your environment configuration and switches to `Simulate` mode for safety.

### Trading & Risk
- **Trading**: Place **Market** and **Limit** orders for Stocks.
- **Option Chains**: Inspect available option contracts for any stock.
- **Order Management**: Modify or Cancel open orders.
- **Deal Execution**: View actual fill prices/fees with `get_deals`.
- **Pro Tools**: View **Level 2 Order Book** (Depth) and check **Fundamentals** (PE, PB).
- **Technical Analysis**: Calculate **RSI, MACD, Bollinger Bands, MA** instantly with `get_technical_indicators`.
- **Risk Management**: Check `margin_ratio` to prevent liquidation and `max_order_value` for safety.
- **High-Speed Data**: Use `get_market_snapshot` for low-latency batch quotes (1ms efficiency).

## Installation

1. **Prerequisites**
   - Install [Moomoo OpenD](https://www.moomoo.com/download/opend) and have it running.
   - Python 3.10+

2. **Clone & Install**
   ```bash
   git clone <repo-url>
   cd moomoo-mcp-server
   pip install -e .
   ```

3. **Configuration**
   Create a `.env` file in the root directory (see `.env.example`):
   ```ini
   # Moomoo OpenD Connection
   OPEND_HOST=127.0.0.1
   OPEND_PORT=11111
   OPEND_PWD=              # Leave empty if no unlock password set in OpenD
   
   # Trading Environment
   MOOMOO_ENV=paper        # 'paper' or 'live'
   MOOMOO_DEFAULT_MARKET=HK # Default market prefix (HK, US, CN)
   ```

## Available Tools

| Tool | Description | Arguments |
| :--- | :--- | :--- |
| `get_quote` | Real-time price snapshot | `symbol` (e.g., "HK.00700") |
| `get_kline` | Historical candlesticks | `symbol`, `period` (default "1d"), `limit` |
| `get_option_chain` | List options contracts | `symbol`, `start`, `end` |
| `get_positions` | Current stock holdings | *None* |
| `get_balance` | Account funds details | *None* |
| `get_orders` | List active/filled orders | `symbol` (optional) |
| `cancel_order` | Cancel an open order | `order_id` |
| `modify_order` | Change Price/Qty of order | `order_id`, `price`, `quantity` |
| `buy_stock` | Place Buy Order (Limit/Market) | `symbol`, `quantity`, `price`, `order_type` |
| `sell_stock` | Place Sell Order (Limit/Market) | `symbol`, `quantity`, `price`, `order_type` |
| `get_order_book` | Level 2 Market Depth (Ladder) | `symbol` |
| `get_financials` | Key Ratios (PE, PB, Market Cap) | `symbol` |
| `get_max_buyable`| Calc max shares (with reason analysis) | `symbol`, `price` |
| `get_deals`      | View executed trade fills (Real-env only)| `symbol` (optional) |
| `get_margin_ratio`| Check account risk/margin status | *None* |
| `get_market_snapshot`| Batch fetch quotes (Fast) | `symbols` (List) |
| `get_technical_indicators`| Calc RSI, MACD, MA, etc. | `symbol`, `indicators` (List) |
| `run_diagnostics`| Execute self-test health check | `symbol` (optional) |

## Health Checks & Diagnostics

You can perform a full system self-test using the `run_diagnostics` tool. This checks:
*   OpenD Connection
*   Market Data Latency
*   Permission access to L2 Data
*   Account Retrieval

Can also be run via script:
```bash
python examples/scripts/test_diagnostics.py
```

## Verification

You can test the connection and tools using the provided scripts:
```bash
# Test Market Data
python examples/scripts/quick_quote.py
python examples/scripts/quick_kline.py

# Test Account Data
python examples/scripts/account_snapshot.py

# Test Trading & Options
python examples/scripts/test_advanced.py

# Test Pro Tools
python examples/scripts/test_pro_tools.py

# Test Execution & Safety (Deals, Margin, Snapshot)
python examples/scripts/test_execution_safety.py

# Test Technical Analysis (RSI, MACD, etc.)
python examples/scripts/test_technical_analysis.py
```

## Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

Please ensure you follow the existing code style and add tests for any new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Risk & Disclaimer
This software is for educational and research purposes. Validating in `paper` mode is highly recommended before any live usage.
