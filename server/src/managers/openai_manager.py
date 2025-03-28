"""
OpenAI API Manager

This module provides a manager class for interacting with the OpenAI API.
It handles authentication, model selection, and response generation.

Author: Pradyun Magal
Date: March 2025
"""

import logging
from typing import Optional, List, Dict, Any

from openai import OpenAI
from src.managers.base_manager import BaseManager

# Configure module logger
logger = logging.getLogger(__name__)

class OpenAIManager(BaseManager):
    """
    Manager class for OpenAI API interactions.
    
    This class handles:
    - API authentication using credentials from environment variables
    - Listing available models
    - Generating responses using selected models
    """
    
    def __init__(self):
        """
        Initialize the OpenAI manager.
        
        Sets up the OpenAI client with API credentials and initializes
        model tracking variables.
        """
        super().__init__("openai")
        
        # Initialize the OpenAI client with API key
        api_key = self._get_credentials()
        if not api_key:
            logger.warning("No OpenAI API key found in environment variables")
            
        self.client = OpenAI(api_key=api_key)
        
        # Initialize model tracking
        self.model = None
        self.model_display_name = None
        
        logger.info("OpenAIManager initialized successfully")
    
    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a response using the OpenAI API.
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system instructions for the model
            
        Returns:
            The generated text response
            
        Raises:
            ValueError: If no model has been set
        """
        # Validate that a model has been selected
        if self.model is None:
            logger.error("Cannot generate response: Model is not set")
            raise ValueError("Model is not set")
            
        # Call the OpenAI API to generate a response
        logger.info(f"Generating response with model '{self.model}'")
        
        # Prepare the request parameters
        request_params = {
            "model": self.model,
            "input": prompt
        }
        
        # Add system prompt if provided
        if system_prompt:
            logger.info("Including system prompt in request")
            request_params["instructions"] = system_prompt
        
        # Make the API call
        response = self.client.responses.create(**request_params)
        logger.info(f"Response received from OpenAI API")
        
        # Extract and return the text content
        # The OpenAI API provides the response text in the output_text property
        return response.output_text

    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available models from the OpenAI API.
        
        Returns:
            The raw response from the OpenAI API containing model information
        """
        logger.info("Listing available OpenAI models")
        return self.client.models.list()
    
    def set_model(self, model: str, model_display_name: Optional[str] = None) -> None:
        """
        Set the model to use for generating responses.
        
        Args:
            model: The model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
            model_display_name: A human-readable name for the model (optional)
        """
        logger.info(f"Setting active model to '{model}'")
        self.model = model
        self.model_display_name = model_display_name
