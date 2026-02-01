class MooMcpError(Exception):
    """Base exception for moomoo-mcp-server."""
    pass

class OpenDConnectionError(MooMcpError):
    """Raised when connection to OpenD fails."""
    pass

class QuoteError(MooMcpError):
    """Raised when fetching a quote fails."""
    pass

def map_futu_error(err: Exception) -> MooMcpError:
    """Map futu-api exceptions to our local error types."""
    return MooMcpError(str(err))
