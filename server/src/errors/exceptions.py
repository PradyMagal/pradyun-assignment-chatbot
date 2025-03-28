"""
Custom exceptions for the application.
"""

class BaseError(Exception):
    """Base class for all custom exceptions."""
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class ModelNotFoundError(BaseError):
    """Raised when a requested model is not found."""
    def __init__(self, model_id=""):
        message = f"Model not found"
        if model_id:
            message = f"Model '{model_id}' not found"
        super().__init__(message)


class ModelNotSetError(BaseError):
    """Raised when trying to generate a response without setting a model."""
    def __init__(self):
        super().__init__("Model not set")


class InvalidRequestError(BaseError):
    """Raised when the request is invalid."""
    def __init__(self, message="Invalid request"):
        super().__init__(message)


class APIError(BaseError):
    """Raised when there's an error with the external API."""
    def __init__(self, message="API error"):
        super().__init__(message)
