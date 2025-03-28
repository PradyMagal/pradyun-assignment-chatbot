"""
Anthropic API Manager

This module provides a manager class for interacting with the Anthropic API.
It handles authentication, model selection, and response generation.

Author: Pradyun Magal
Date: March 2025
"""

import logging
from typing import Optional, List, Dict, Any

import anthropic
from src.managers.base_manager import BaseManager

# Configure module logger
logger = logging.getLogger(__name__)

class AnthropicManager(BaseManager):
    """
    Manager class for Anthropic API interactions.
    
    This class handles:
    - API authentication using credentials from environment variables
    - Listing available models
    - Generating responses using selected models
    """
    
    def __init__(self):
        """
        Initialize the Anthropic manager.
        
        Sets up the Anthropic client with API credentials and initializes
        model tracking variables.
        """
        super().__init__("anthropic") 
        
        # Initialize the Anthropic client with API key
        api_key = self._get_credentials()
        if not api_key:
            logger.warning("No Anthropic API key found in environment variables")
            
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Initialize model tracking
        self.model = None
        self.model_display_name = None
        
        logger.info("AnthropicManager initialized successfully")
    
    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a response using the Anthropic API.
        
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
        
        # Call the Anthropic API to generate a response
        logger.info(f"Generating response with model '{self.model}'")
        
        # Prepare the messages array
        messages = [{"role": "user", "content": prompt}]
        
        # Prepare the request parameters
        request_params = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": messages
        }
        
        # Add system prompt if provided
        if system_prompt:
            logger.info("Including system prompt in request")
            request_params["system"] = system_prompt
        
        # Make the API call
        response = self.client.messages.create(**request_params)
        logger.info(f"Response received from Anthropic API")
        
        # Extract the text content from the response
        # The Anthropic API returns content as a list of content blocks
        if response.content and len(response.content) > 0:
            # Get the first content block (usually there's just one)
            content_block = response.content[0]
            if hasattr(content_block, 'text'):
                return content_block.text
        
        # If we couldn't extract text through the expected path, return a fallback
        return "Response received but could not extract text content."

    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available models from the Anthropic API.
        
        Returns:
            A list of available models
        """
        logger.info("Listing available Anthropic models")
        
        try:
            # Call the Anthropic API to list models
            response = self.client.models.list()
            
            # Format the response to match our expected structure
            models = []
            for model in response.data:
                models.append({
                    "id": model.id,
                    "name": model.display_name if hasattr(model, 'display_name') else model.id,
                    "provider": "anthropic"
                })
            
            logger.info(f"Retrieved {len(models)} models from Anthropic API")
            return models
        except Exception as e:
            logger.error(f"Error listing Anthropic models: {str(e)}")
            # Return an empty list in case of error
            return []
    
    def set_model(self, model: str, model_display_name: Optional[str] = None) -> None:
        """
        Set the model to use for generating responses.
        
        Args:
            model: The model identifier (e.g., "claude-3-opus-20240229")
            model_display_name: A human-readable name for the model (optional)
        """
        logger.info(f"Setting active model to '{model}'")
        self.model = model
