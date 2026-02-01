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
    # This is a placeholder; futu usually returns RetType values or raises exceptions
    # We will refine this as we observe actual futu errors.
    return MooMcpError(str(err))
