"""
Base Manager for AI Model Providers

This module defines an abstract base class for AI model provider managers.
It provides a common interface for interacting with different AI model APIs.

Author: Pradyun Magal
Date: March 2025
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BaseManager(ABC):
    """
    Abstract base class for AI model provider managers.
    
    This class defines the common interface that all AI model provider
    managers must implement, ensuring consistent behavior across
    different providers.
    """
    
    def __init__(self, provider: str):
        """
        Initialize the base manager.
        
        Args:
            provider: The name of the AI model provider (e.g., "openai", "anthropic")
        """
        self.provider = provider
        self.model = None
        self.model_display_name = None
    
    def __str__(self) -> str:
        """Return a string representation of the manager."""
        return f"BaseManager(provider={self.provider})"
    
    def _get_credentials(self) -> Optional[str]:
        """
        Get API credentials for the provider from environment variables.
        
        Returns:
            The API key for the provider, or None if not found
        """
        if self.provider == "openai":
            return os.getenv("OPEN_AI_KEY")
        elif self.provider == "anthropic":
            return os.getenv("ANTHROPIC_KEY")
        return None

    @abstractmethod
    def generate_response(self, prompt: str) -> Any:
        """
        Generate a response using the selected model.
        
        Args:
            prompt: The user's input prompt
            
        Returns:
            The generated response (format may vary by provider)
            
        Raises:
            ValueError: If no model has been set
        """
        pass

    @abstractmethod
    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available models from the provider.
        
        Returns:
            A list of available models
        """
        pass

    @abstractmethod
    def set_model(self, model: str, model_display_name: Optional[str] = None) -> None:
        """
        Set the model to use for generating responses.
        
        Args:
            model: The model identifier
            model_display_name: A human-readable name for the model (optional)
        """
        pass

    def get_model_display_name(self) -> Optional[str]:
        """
        Get the display name of the currently selected model.
        
        Returns:
            The display name of the model, or None if no model is selected
        """
        return self.model_display_name
