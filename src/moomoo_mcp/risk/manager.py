import logging
from ..config import config

logger = logging.getLogger(__name__)

class RiskError(Exception):
    """Raised when a risk check fails."""
    pass

class RiskManager:
    """
    Validates orders against defined risk policies.
    """
    
    @staticmethod
    def check_order(symbol: str, quantity: int, price: float):
        """
        Validates an order before submission.
        Raises RiskError if validation fails.
        """
        # 1. Check Max Order Value
        estimated_value = quantity * price
        if estimated_value > config.max_order_value:
            msg = (f"Risk Reject: Order value {estimated_value:.2f} exceeds limit "
                   f"{config.max_order_value:.2f} for {symbol}")
            logger.warning(msg)
            raise RiskError(msg)
            
        logger.info(f"Risk Pass: Order {symbol} {quantity}@{price} ({estimated_value:.2f})")
        return True
