# Pradyun Chat Application

A web-based tool that enables users to interact with AI models from OpenAI and Anthropic.

## Features

- Support for all OpenAI models
- Support for all Anthropic models
- Real-time response generation
- Clean, minimal API design

## Project Structure

- `server/`: Python Flask backend
- `client/`: React frontend 

## Setup

### Prerequisites

- Python 3.13+
- Node.js and npm (for the client)
- OpenAI API key
- Anthropic API key

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
OPEN_AI_KEY=your_openai_api_key
ANTHROPIC_KEY=your_anthropic_api_key
```

### Installation

Use the provided Makefile to install dependencies:

```bash
# Install server dependencies
make install-server

# Install client dependencies (when client is implemented)
make install-client

# Install all dependencies
make install
```

## Running the Application
Do these in a separate terminal
```bash
# Start the server only
make start-server

# Start the client only (when client is implemented)
make start-client

```

## API Endpoints

### OpenAI

- **GET** `/api/openai/models`: List all available OpenAI models
- **POST** `/api/openai/generate`: Generate a response using an OpenAI model

Example request body for `/api/openai/generate`:
```json
{
  "model": "gpt-3.5-turbo",
  "prompt": "Write a short poem about artificial intelligence."
}
```

### Anthropic

- **GET** `/api/anthropic/models`: List all available Anthropic models
- **POST** `/api/anthropic/generate`: Generate a response using an Anthropic model

Example request body for `/api/anthropic/generate`:
```json
{
  "model": "claude-3-sonnet-20240229",
  "prompt": "Explain the concept of machine learning in simple terms."
}
```

### Health Check

- **GET** `/health`: Check if the API is running

## Response Format

All API responses follow this format:

```json
{
  "code": 200,
  "message": "success",
  "data": {
      {
      "code": 200,
      "data": {
          "status": "OK"
      },
      "message": "success"
  }
  }
}
```

For error responses:

```json
{
  "code": 400, // or other error code
  "message": "Bad Request", // or other error message
  "timestamp": 1234567890.123
}
```

## Development

### Clean Up

```bash
make clean
```

This will remove Python cache files and compiled bytecode.
