from typing import Optional, Any, Dict, Tuple, Union
from flask import jsonify, Response

CODE = 200
MESSAGE = "success"

class SuccResponse:
    def __init__(self, data: Optional[Any] = None, status_code: int = CODE):
        self.data = data
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.data}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary."""
        response = {
            "code": self.status_code,
            "message": MESSAGE
        }
        
        # Only include data if it's not None
        if self.data is not None:
            response["data"] = self.data
            
        return response
    
    def to_response(self) -> Response:
        """Convert to a Flask Response object with JSON content."""
        return jsonify(self.to_dict()), self.status_code
    
    def to_tuple(self) -> Tuple[Dict[str, Any], int]:
        """Return a tuple of (dict, status_code) that Flask can convert to a response."""
        return self.to_dict(), self.status_code

def create_success_response(data: Optional[Any] = None, status_code: int = CODE) -> SuccResponse:
    """Helper function to create a success response."""
    return SuccResponse(data, status_code)
