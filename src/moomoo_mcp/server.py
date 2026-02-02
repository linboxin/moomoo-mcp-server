from mcp.server.fastmcp import FastMCP
import logging
from .market_data.get_quote import get_quote
from .market_data.get_kline import get_kline
from .market_data.get_option_chain import get_option_chain
from .market_data.get_financials import get_financials
from .market_data.get_order_book import get_order_book
from .account.get_positions import get_positions
from .account.get_balance import get_balance
from .account.get_orders import get_orders
from .account.get_max_buyable import get_max_buyable
from .trading.buy_stock import buy_stock
from .trading.sell_stock import sell_stock
from .trading.cancel_order import cancel_order
from .trading.modify_order import modify_order
from .trading.get_deals import get_deals
from .account.get_margin_ratio import get_margin_ratio
from .market_data.get_market_snapshot import get_market_snapshot
from .system.run_diagnostics import run_diagnostics

# Initialize FastMCP
mcp = FastMCP("moomoo-mcp-server")

# Basic logging setup (will be improved in logging.py)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp.add_tool(get_quote)
mcp.add_tool(get_kline)
mcp.add_tool(get_option_chain)
mcp.add_tool(get_financials)
mcp.add_tool(get_order_book)
mcp.add_tool(get_positions)
mcp.add_tool(get_balance)
mcp.add_tool(get_orders)
mcp.add_tool(get_max_buyable)
mcp.add_tool(buy_stock)
mcp.add_tool(sell_stock)
mcp.add_tool(cancel_order)
mcp.add_tool(modify_order)
mcp.add_tool(get_deals)
mcp.add_tool(get_margin_ratio)
mcp.add_tool(get_market_snapshot)
mcp.add_tool(run_diagnostics)

@mcp.tool()
def health_ping() -> str:
    """Returns 'pong' to verify server is running."""
    return "pong"

def main():
    """Entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main()
