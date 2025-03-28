"""
Main Flask Application

This module defines the Flask application and API endpoints for interacting with
AI models from OpenAI and Anthropic. It provides endpoints for listing available
models and generating responses using selected models.

Author: Pradyun Magal
Date: March 2025
"""

import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import BaseModel

# Import response models
from src.models.succ_response import create_success_response, SuccResponse
from src.models.err_response import (
    ErrorResponse, ErrorCodes, ErrorMessages,
    bad_request, unauthorized, not_found, internal_server_error
)

# Import AI model managers
from src.managers.openai_manager import OpenAIManager
from src.managers.anthropic_manager import AnthropicManager

# Configure logging with timestamp and log level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize AI model managers
openai_manager = OpenAIManager()
anthropic_manager = AnthropicManager()

# Map of provider names to their respective managers
model_managers = {
    "openai": openai_manager,
    "anthropic": anthropic_manager
}

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        JSON response with status information
    """
    logger.info("Health check requested")
    return create_success_response({"status": "OK"}).to_response()

@app.route('/test', methods=['GET'])
def test():
    """
    Simple test endpoint that returns a plain text response.
    Useful for testing if the server is working correctly.
    """
    logger.info("Test endpoint requested")
    return "Server is working correctly!"

@app.route('/api/check-keys', methods=['GET'])
def check_keys():
    """
    Check if API keys are loaded correctly.
    Returns masked versions of the keys for security.
    """
    logger.info("API key check requested")
    openai_key = openai_manager._get_credentials()
    anthropic_key = anthropic_manager._get_credentials()
    
    # Mask the keys for security
    openai_key_masked = f"{openai_key[:5]}...{openai_key[-5:]}" if openai_key else "Not set"
    anthropic_key_masked = f"{anthropic_key[:5]}...{anthropic_key[-5:]}" if anthropic_key else "Not set"
    
    return create_success_response({
        "openai_key": openai_key_masked,
        "anthropic_key": anthropic_key_masked
    }).to_response()

@app.route('/api/openai/models', methods=['GET'])
def list_openai_models():
    """
    Endpoint to list all available OpenAI models.
    
    Returns:
        JSON response with a list of available OpenAI models
    """
    logger.info("OpenAI model listing requested")
    try:
        # Get models from OpenAI
        models_response = openai_manager.list_models()
        
        # Extract model IDs and format the response
        models = []
        for model in models_response.data:
            models.append({
                "id": model.id,
                "name": model.id,
                "provider": "openai"
            })
        
        logger.info(f"Returning {len(models)} OpenAI models")
        return create_success_response(models).to_response()
    except Exception as e:
        logger.error(f"Error listing OpenAI models: {str(e)}")
        return internal_server_error().to_response()

@app.route('/api/anthropic/models', methods=['GET'])
def list_anthropic_models():
    """
    Endpoint to list all available Anthropic models.
    
    Returns:
        JSON response with a list of available Anthropic models
    """
    logger.info("Anthropic model listing requested")
    try:
        # Get models from Anthropic
        models = anthropic_manager.list_models()
        
        logger.info(f"Returning {len(models)} Anthropic models")
        return create_success_response(models).to_response()
    except Exception as e:
        logger.error(f"Error listing Anthropic models: {str(e)}")
        return internal_server_error().to_response()

@app.route('/api/openai/generate', methods=['POST'])
def generate_openai_response():
    """
    Endpoint to generate a response using a specified OpenAI model.
    
    Expected JSON body:
    {
        "model": "model-id",
        "prompt": "User prompt text",
        "system_prompt": "Optional system instructions" (optional)
    }
    
    Returns:
        JSON response with the generated text
    """
    logger.info("OpenAI response generation requested")
    try:
        # Get and validate request data
        data = request.json
        
        if not data:
            logger.warning("No request data provided")
            return bad_request().to_response()
        
        # Validate required fields
        required_fields = ["model", "prompt"]
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return bad_request().to_response()
        
        # Extract request parameters
        model_id = data["model"]
        prompt = data["prompt"]
        system_prompt = data.get("system_prompt", "")
        
        logger.info(f"Generating response using OpenAI model: {model_id}")
        if system_prompt:
            logger.info("System prompt provided")
        
        # Set the model and generate response
        openai_manager.set_model(model_id)
        response_text = openai_manager.generate_response(prompt, system_prompt)
        
        # Ensure the response is a string
        if not isinstance(response_text, str):
            response_text = str(response_text)
        
        # Return the successful response
        return create_success_response({
            "response": response_text,
            "model": model_id,
            "provider": "openai"
        }).to_response()
        
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return bad_request().to_response()
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return internal_server_error().to_response()

@app.route('/api/anthropic/generate', methods=['POST'])
def generate_anthropic_response():
    """
    Endpoint to generate a response using a specified Anthropic model.
    
    Expected JSON body:
    {
        "model": "model-id",
        "prompt": "User prompt text",
        "system_prompt": "Optional system instructions" (optional)
    }
    
    Returns:
        JSON response with the generated text
    """
    logger.info("Anthropic response generation requested")
    try:
        # Get and validate request data
        data = request.json
        
        if not data:
            logger.warning("No request data provided")
            return bad_request().to_response()
        
        # Validate required fields
        required_fields = ["model", "prompt"]
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return bad_request().to_response()
        
        # Extract request parameters
        model_id = data["model"]
        prompt = data["prompt"]
        system_prompt = data.get("system_prompt", "")
        
        logger.info(f"Generating response using Anthropic model: {model_id}")
        if system_prompt:
            logger.info("System prompt provided")
        
        # Set the model and generate response
        anthropic_manager.set_model(model_id)
        response_text = anthropic_manager.generate_response(prompt, system_prompt)
        
        # Ensure the response is a string
        if not isinstance(response_text, str):
            response_text = str(response_text)
        
        # Return the successful response
        return create_success_response({
            "response": response_text,
            "model": model_id,
            "provider": "anthropic"
        }).to_response()
        
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return bad_request().to_response()
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return internal_server_error().to_response()

# Global error handlers
@app.errorhandler(404)
def handle_not_found(e):
    """Handle 404 Not Found errors."""
    logger.warning(f"Not found: {request.path}")
    return not_found().to_response()

@app.errorhandler(500)
def handle_server_error(e):
    """Handle 500 Internal Server Error errors."""
    logger.error(f"Server error: {str(e)}")
    return internal_server_error().to_response()

# Run the application
if __name__ == '__main__':
    logger.info("Starting Flask application")
    # Disable the debugger pin for development
    import os
    os.environ['WERKZEUG_DEBUG_PIN'] = 'off'
    # Use port 8000 instead of 5000 (which is often used by AirPlay on macOS)
    app.run(debug=True, host='0.0.0.0', port=8000)
