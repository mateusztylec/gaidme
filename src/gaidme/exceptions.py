class GAIDMEBaseException(Exception):
    """Base exception class for GAIDME application."""

class ConfigError(GAIDMEBaseException):
    """Raised when there's an issue with the configuration."""

class CommandNotAllowedError(GAIDMEBaseException):
    """Raised when a blacklisted command is attempted to be executed."""

class APIError(GAIDMEBaseException):
    """Raised when there's an issue with API communication."""

class InvalidAPIKeyError(APIError):
    """Raised when the API key is invalid."""

class APIVersionError(APIError):
    """Raised when the API version is not supported."""

class UsageLimitExceededError(APIError):
    """Raised when the usage limit is exceeded."""
