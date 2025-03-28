"""
Error Response Model

This module defines a class for creating error response objects,
makes code cleaner from main.py
"""
from time import perf_counter
from typing import Any, Dict, Tuple, Optional
from flask import jsonify, Response

class ErrorCodes:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

class ErrorMessages:
    BAD_REQUEST = "Bad Request"
    UNAUTHORIZED = "Unauthorized"
    NOT_FOUND = "Not Found"
    INTERNAL_SERVER_ERROR = "Internal Server Error"

class ErrorResponse:
    def __init__(self, code: int, message: str, details: Optional[Any] = None):
        self.timestamp = perf_counter()
        self.code = code
        self.message = message
        self.details = details

    def __str__(self) -> str:
        return f"{self.timestamp} - {self.code}: {self.message}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def get_code(self) -> int:
        return self.code

    def get_message(self) -> str:
        return self.message

    def get_timestamp(self) -> float:
        return self.timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the error response to a dictionary."""
        response = {
            "code": self.code,
            "message": self.message,
            "timestamp": self.timestamp
        }
        if self.details:
            response["details"] = self.details
        return response
    
    def to_response(self) -> Response:
        """Convert to a Flask Response object with JSON content."""
        return jsonify(self.to_dict()), self.code
    
    def to_tuple(self) -> Tuple[Dict[str, Any], int]:
        """Return a tuple of (dict, status_code) that Flask can convert to a response."""
        return self.to_dict(), self.code

def create_error_response(code: int, message: str, details: Optional[Any] = None) -> ErrorResponse:
    """Helper function to create an error response."""
    return ErrorResponse(code, message, details)

def bad_request(details: Optional[Any] = None) -> ErrorResponse:
    """Create a 400 Bad Request error response."""
    return create_error_response(ErrorCodes.BAD_REQUEST, ErrorMessages.BAD_REQUEST, details)

def unauthorized(details: Optional[Any] = None) -> ErrorResponse:
    """Create a 401 Unauthorized error response."""
    return create_error_response(ErrorCodes.UNAUTHORIZED, ErrorMessages.UNAUTHORIZED, details)

def not_found(details: Optional[Any] = None) -> ErrorResponse:
    """Create a 404 Not Found error response."""
    return create_error_response(ErrorCodes.NOT_FOUND, ErrorMessages.NOT_FOUND, details)

def internal_server_error(details: Optional[Any] = None) -> ErrorResponse:
    """Create a 500 Internal Server Error response."""
    return create_error_response(ErrorCodes.INTERNAL_SERVER_ERROR, ErrorMessages.INTERNAL_SERVER_ERROR, details)
