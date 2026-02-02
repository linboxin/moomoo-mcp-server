from mcp.server.fastmcp import FastMCP
import logging
from .market_data.get_quote import get_quote
from .market_data.get_kline import get_kline
from .account.get_positions import get_positions
from .account.get_balance import get_balance
from .account.get_orders import get_orders
from .trading.buy_stock import buy_stock
from .trading.sell_stock import sell_stock

# Initialize FastMCP
mcp = FastMCP("moomoo-mcp-server")

# Basic logging setup (will be improved in logging.py)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp.add_tool(get_quote)
mcp.add_tool(get_kline)
mcp.add_tool(get_positions)
mcp.add_tool(get_balance)
mcp.add_tool(get_orders)
mcp.add_tool(buy_stock)
mcp.add_tool(sell_stock)

@mcp.tool()
def health_ping() -> str:
    """Returns 'pong' to verify server is running."""
    return "pong"

def main():
    """Entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main()
