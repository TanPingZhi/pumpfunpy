class PumpFunError(Exception):
    """Base exception for pumpfunpy errors."""


class APIRequestError(PumpFunError):
    """Raised when an HTTP request fails."""


class WebSocketError(PumpFunError):
    """Raised for WebSocket connection or protocol errors."""
