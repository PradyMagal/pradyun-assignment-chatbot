# Makefile for Pradyun Chat Application

# Variables
PYTHON = python
PIP = pip
SERVER_DIR = server
CLIENT_DIR = client/chat-app

# Default target
.PHONY: all
all: install-server start-server

# Install server dependencies
.PHONY: install-server
install-server:
	@echo "Installing server dependencies..."
	cd $(SERVER_DIR) && $(PIP) install -e .

# Start the server
.PHONY: start-server
start-server:
	@echo "Starting server..."
	cd $(SERVER_DIR) && $(PYTHON) -m src.main

# Install client dependencies
.PHONY: install-client
install-client:
	@echo "Installing client dependencies..."
	cd $(CLIENT_DIR) && npm install

# Start the client
.PHONY: start-client
start-client:
	@echo "Starting client..."
	cd $(CLIENT_DIR) && npm run dev

# Build the client
.PHONY: build-client
build-client:
	@echo "Building client..."
	cd $(CLIENT_DIR) && npm run build

# Install all dependencies
.PHONY: install
install: install-server install-client

# Start both client and server
.PHONY: start
start:
	@echo "Starting client and server..."
	$(MAKE) start-server & $(MAKE) start-client

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
