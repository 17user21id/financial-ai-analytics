# Makefile for AI-Powered Financial Data Processing System

# Configuration
PYTHON := python3
PIP := pip3
VENV := venv
VENV_BIN := $(VENV)/bin
VENV_PYTHON := $(VENV_BIN)/python
VENV_PIP := $(VENV_BIN)/pip

# Project directories
SRC_DIR := src
TEST_DIR := test
LOGS_DIR := logs
RESOURCES_DIR := resources

# Database
DB_PATH := financial_data.db
DB_TEST_PATH := test_financial_data.db

# API Configuration
API_HOST := 0.0.0.0
API_PORT := 8000
API_URL := http://$(API_HOST):$(API_PORT)

# Environment
ENVIRONMENT ?= DEV
LOG_LEVEL ?= INFO

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

.PHONY: help install setup clean test run dev prod lint format format-check docs

# Default target
help: ## Show this help message
	@echo "$(BLUE)AI-Powered Financial Data Processing System$(NC)"
	@echo "$(BLUE)============================================$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Quick Start:$(NC)"
	@echo "  $(YELLOW)make setup$(NC)     - Complete setup (install dependencies, init database)"
	@echo "  $(YELLOW)make dev$(NC)        - Start development server"
	@echo "  $(YELLOW)make test$(NC)       - Run all tests"
	@echo ""

# Installation and Setup
install: ## Install Python dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	$(VENV_PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

setup: ## Complete project setup (install dependencies, init database)
	@echo "$(BLUE)Setting up AI-Powered Financial Data Processing System...$(NC)"
	@echo ""
	@echo "$(YELLOW)1. Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✓ Virtual environment created$(NC)"
	@echo ""
	@echo "$(YELLOW)2. Installing dependencies...$(NC)"
	$(MAKE) install
	@echo ""
	@echo "$(YELLOW)3. Initializing database...$(NC)"
	$(VENV_PYTHON) -m src.handler.data_sync_handler
	@echo "$(GREEN)✓ Database initialized$(NC)"
	@echo ""
	@echo "$(YELLOW)4. Running initial tests...$(NC)"
	$(MAKE) test-quick
	@echo ""
	@echo "$(GREEN)✓ Setup completed successfully!$(NC)"
	@echo ""
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  $(YELLOW)make dev$(NC)        - Start development server"
	@echo "  $(YELLOW)make docs$(NC)       - View API documentation"
	@echo "  $(YELLOW)make test$(NC)       - Run comprehensive tests"

# Development
dev: ## Start development server with auto-reload
	@echo "$(BLUE)Starting development server...$(NC)"
	@echo "$(YELLOW)Server will be available at: $(API_URL)$(NC)"
	@echo "$(YELLOW)API Documentation: $(API_URL)/docs$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	@echo ""
	ENVIRONMENT=$(ENVIRONMENT) LOG_LEVEL=$(LOG_LEVEL) $(VENV_PYTHON) -m src.api.main

run: ## Start production server
	@echo "$(BLUE)Starting production server...$(NC)"
	@echo "$(YELLOW)Server will be available at: $(API_URL)$(NC)"
	@echo ""
	ENVIRONMENT=PROD LOG_LEVEL=WARNING $(VENV_PYTHON) -m src.api.main

prod: run ## Alias for production server

# Testing
test: ## Run all tests with coverage
	@echo "$(BLUE)Running comprehensive test suite...$(NC)"
	$(VENV_PYTHON) -m pytest $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-quick: ## Run quick tests (no coverage)
	@echo "$(BLUE)Running quick tests...$(NC)"
	$(VENV_PYTHON) -m pytest $(TEST_DIR)/ -v
	@echo "$(GREEN)✓ Quick tests completed$(NC)"

test-ai: ## Run AI-specific tests
	@echo "$(BLUE)Running AI-specific tests...$(NC)"
	$(VENV_PYTHON) -m pytest $(TEST_DIR)/test_context_refactored.py -v
	@echo "$(GREEN)✓ AI tests completed$(NC)"

test-data: ## Run data integration tests
	@echo "$(BLUE)Running data integration tests...$(NC)"
	$(VENV_PYTHON) -m pytest $(TEST_DIR)/test_data_integration.py -v
	@echo "$(GREEN)✓ Data tests completed$(NC)"

# Database Operations
db-init: ## Initialize database with sample data
	@echo "$(BLUE)Initializing database...$(NC)"
	$(VENV_PYTHON) -m src.handler.data_sync_handler
	@echo "$(GREEN)✓ Database initialized$(NC)"

db-reset: ## Reset database (WARNING: This will delete all data)
	@echo "$(RED)WARNING: This will delete all data in the database!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "$(BLUE)Resetting database...$(NC)"
	rm -f $(DB_PATH)
	$(MAKE) db-init
	@echo "$(GREEN)✓ Database reset completed$(NC)"

db-backup: ## Create database backup
	@echo "$(BLUE)Creating database backup...$(NC)"
	@mkdir -p backups
	cp $(DB_PATH) backups/financial_data_$(shell date +%Y%m%d_%H%M%S).db
	@echo "$(GREEN)✓ Database backup created$(NC)"

# Code Quality
lint: ## Run code linting
	@echo "$(BLUE)Running code linting...$(NC)"
	$(VENV_PYTHON) -m flake8 $(SRC_DIR)/ $(TEST_DIR)/ --max-line-length=100 --ignore=E203,W503
	@echo "$(GREEN)✓ Linting completed$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	$(VENV_PYTHON) -m black $(SRC_DIR)/ $(TEST_DIR)/ --line-length=88
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting with black
	@echo "$(BLUE)Checking code formatting...$(NC)"
	$(VENV_PYTHON) -m black $(SRC_DIR)/ $(TEST_DIR)/ --line-length=88 --check
	@echo "$(GREEN)✓ Code formatting check completed$(NC)"

type-check: ## Run type checking with mypy
	@echo "$(BLUE)Running type checking...$(NC)"
	$(VENV_PYTHON) -m mypy $(SRC_DIR)/ --ignore-missing-imports
	@echo "$(GREEN)✓ Type checking completed$(NC)"

# Documentation
docs: ## Open API documentation in browser
	@echo "$(BLUE)Opening API documentation...$(NC)"
	@echo "$(YELLOW)Swagger UI: $(API_URL)/docs$(NC)"
	@echo "$(YELLOW)ReDoc: $(API_URL)/redoc$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop the server$(NC)"
	@echo ""
	@echo "$(BLUE)Starting server for documentation...$(NC)"
	ENVIRONMENT=$(ENVIRONMENT) $(VENV_PYTHON) -m src.api.main

docs-build: ## Build documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	@echo "$(GREEN)✓ Documentation files are already built in the repository$(NC)"

# API Testing
api-test: ## Test API endpoints
	@echo "$(BLUE)Testing API endpoints...$(NC)"
	@echo "$(YELLOW)Testing health endpoint...$(NC)"
	curl -s $(API_URL)/api/health/ | $(VENV_PYTHON) -m json.tool
	@echo ""
	@echo "$(YELLOW)Testing root endpoint...$(NC)"
	curl -s $(API_URL)/ | $(VENV_PYTHON) -m json.tool
	@echo ""
	@echo "$(GREEN)✓ API tests completed$(NC)"

api-test-ai: ## Test AI query endpoint
	@echo "$(BLUE)Testing AI query endpoint...$(NC)"
	@echo "$(YELLOW)Sending test query...$(NC)"
	curl -X POST "$(API_URL)/api/ai/query" \
		-H "Content-Type: application/json" \
		-d '{"query": "What is the total revenue?", "chat_id": "test_chat", "user_id": "test_user"}' \
		| $(VENV_PYTHON) -m json.tool
	@echo ""
	@echo "$(GREEN)✓ AI query test completed$(NC)"

# Logging and Monitoring
logs: ## Show recent logs
	@echo "$(BLUE)Recent application logs:$(NC)"
	@if [ -d "$(LOGS_DIR)" ]; then \
		find $(LOGS_DIR) -name "*.log" -type f -exec tail -20 {} \; -print; \
	else \
		echo "$(YELLOW)No logs directory found$(NC)"; \
	fi

logs-clear: ## Clear all log files
	@echo "$(BLUE)Clearing log files...$(NC)"
	rm -rf $(LOGS_DIR)/*
	@echo "$(GREEN)✓ Logs cleared$(NC)"

logs-tail: ## Tail logs in real-time
	@echo "$(BLUE)Tailing logs in real-time...$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(NC)"
	@if [ -d "$(LOGS_DIR)" ]; then \
		tail -f $(LOGS_DIR)/*.log; \
	else \
		echo "$(YELLOW)No logs directory found$(NC)"; \
	fi

# Performance Testing
perf-test: ## Run performance tests
	@echo "$(BLUE)Running performance tests...$(NC)"
	@echo "$(YELLOW)Testing API response times...$(NC)"
	@for i in {1..10}; do \
		echo "Request $$i:"; \
		time curl -s $(API_URL)/api/health/ > /dev/null; \
	done
	@echo "$(GREEN)✓ Performance tests completed$(NC)"

load-test: ## Run load tests (requires server to be running)
	@echo "$(BLUE)Running load tests...$(NC)"
	@echo "$(YELLOW)Testing concurrent requests...$(NC)"
	@for i in {1..5}; do \
		curl -s $(API_URL)/api/health/ > /dev/null & \
	done; \
	wait
	@echo "$(GREEN)✓ Load tests completed$(NC)"

# Cleanup
clean: ## Clean up temporary files and caches
	@echo "$(BLUE)Cleaning up temporary files...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	@echo "$(GREEN)✓ Cleanup completed$(NC)"

clean-all: clean ## Clean everything including virtual environment
	@echo "$(BLUE)Cleaning everything...$(NC)"
	rm -rf $(VENV)
	rm -f $(DB_PATH)
	rm -rf $(LOGS_DIR)
	rm -rf backups
	@echo "$(GREEN)✓ Complete cleanup completed$(NC)"

# Environment Management
env-check: ## Check environment configuration
	@echo "$(BLUE)Checking environment configuration...$(NC)"
	@echo "$(YELLOW)Python version:$(NC)"
	$(PYTHON) --version
	@echo "$(YELLOW)Pip version:$(NC)"
	$(PIP) --version
	@echo "$(YELLOW)Virtual environment:$(NC)"
	@if [ -d "$(VENV)" ]; then \
		echo "$(GREEN)✓ Virtual environment exists$(NC)"; \
	else \
		echo "$(RED)✗ Virtual environment not found$(NC)"; \
	fi
	@echo "$(YELLOW)Database file:$(NC)"
	@if [ -f "$(DB_PATH)" ]; then \
		echo "$(GREEN)✓ Database file exists$(NC)"; \
	else \
		echo "$(RED)✗ Database file not found$(NC)"; \
	fi
	@echo "$(YELLOW)Environment variables:$(NC)"
	@echo "ENVIRONMENT: $(ENVIRONMENT)"
	@echo "LOG_LEVEL: $(LOG_LEVEL)"
	@echo "API_HOST: $(API_HOST)"
	@echo "API_PORT: $(API_PORT)"

# Development Utilities
dev-install: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	$(VENV_PIP) install pytest pytest-cov flake8 black mypy
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

dev-tools: ## Install all development tools
	@echo "$(BLUE)Installing development tools...$(NC)"
	$(MAKE) dev-install
	$(VENV_PIP) install jupyter ipython
	@echo "$(GREEN)✓ Development tools installed$(NC)"

# Quick Commands
start: dev ## Alias for development server
stop: ## Stop any running processes
	@echo "$(BLUE)Stopping all processes...$(NC)"
	pkill -f "src.api.main" || true
	@echo "$(GREEN)✓ Processes stopped$(NC)"

restart: stop start ## Restart development server

status: ## Show system status
	@echo "$(BLUE)System Status:$(NC)"
	@echo "$(YELLOW)Virtual Environment:$(NC)"
	@if [ -d "$(VENV)" ]; then \
		echo "$(GREEN)✓ Active$(NC)"; \
	else \
		echo "$(RED)✗ Not found$(NC)"; \
	fi
	@echo "$(YELLOW)Database:$(NC)"
	@if [ -f "$(DB_PATH)" ]; then \
		echo "$(GREEN)✓ Exists ($(shell du -h $(DB_PATH) | cut -f1))$(NC)"; \
	else \
		echo "$(RED)✗ Not found$(NC)"; \
	fi
	@echo "$(YELLOW)API Server:$(NC)"
	@if curl -s $(API_URL)/api/health/ > /dev/null 2>&1; then \
		echo "$(GREEN)✓ Running$(NC)"; \
	else \
		echo "$(RED)✗ Not running$(NC)"; \
	fi

# Version Information
version: ## Show version information
	@echo "$(BLUE)AI-Powered Financial Data Processing System$(NC)"
	@echo "$(BLUE)Version: 1.0.0$(NC)"
	@echo "$(BLUE)Python: $(shell $(PYTHON) --version)$(NC)"
	@echo "$(BLUE)Environment: $(ENVIRONMENT)$(NC)"
	@echo "$(BLUE)API URL: $(API_URL)$(NC)"

# Help for specific categories
help-dev: ## Show development-related commands
	@echo "$(BLUE)Development Commands:$(NC)"
	@echo "  $(YELLOW)make dev$(NC)           - Start development server"
	@echo "  $(YELLOW)make test$(NC)          - Run all tests"
	@echo "  $(YELLOW)make lint$(NC)          - Run code linting"
	@echo "  $(YELLOW)make format$(NC)        - Format code"
	@echo "  $(YELLOW)make docs$(NC)          - Open API documentation"

help-test: ## Show testing-related commands
	@echo "$(BLUE)Testing Commands:$(NC)"
	@echo "  $(YELLOW)make test$(NC)          - Run all tests with coverage"
	@echo "  $(YELLOW)make test-quick$(NC)    - Run quick tests"
	@echo "  $(YELLOW)make test-ai$(NC)        - Run AI-specific tests"
	@echo "  $(YELLOW)make api-test$(NC)      - Test API endpoints"

# Default target when no target is specified
.DEFAULT_GOAL := help
