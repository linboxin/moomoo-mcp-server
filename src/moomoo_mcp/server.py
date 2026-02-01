from mcp.server.fastmcp import FastMCP
import logging

# Initialize FastMCP
mcp = FastMCP("moomoo-mcp-server")

# Basic logging setup (will be improved in logging.py)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
def health_ping() -> str:
    """Returns 'pong' to verify server is running."""
    return "pong"

def main():
    """Entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main()
