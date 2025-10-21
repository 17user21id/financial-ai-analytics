#!/bin/bash

# AI-Powered Financial Data Processing System - Setup Script
# This script helps set up the project for development

set -e

echo "🚀 Setting up AI-Powered Financial Data Processing System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
        print_success "Found Python 3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        print_success "Found Python 3"
    else
        print_error "Python 3.11+ is required but not installed"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Setup configuration files
setup_config() {
    print_status "Setting up configuration files..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Database Configuration
DATABASE_PATH=financial_data.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
ENVIRONMENT=DEV

# Azure OpenAI Configuration (set these after creating your Azure OpenAI resource)
LLM_MODEL=your-deployment-name
LLM_TEMPERATURE=0.4
EOF
        print_success ".env file created"
    else
        print_status ".env file already exists"
    fi
    
    # Setup key_store.json if it doesn't exist
    if [ ! -f "resources/key_store.json" ]; then
        if [ -f "resources/key_store.json.example" ]; then
            cp resources/key_store.json.example resources/key_store.json
            print_success "key_store.json created from example"
            print_warning "Please update resources/key_store.json with your actual Azure OpenAI credentials"
        else
            print_error "key_store.json.example not found"
        fi
    else
        print_status "key_store.json already exists"
    fi
}

# Create logs directory
create_logs_dir() {
    print_status "Creating logs directory..."
    mkdir -p logs
    print_success "Logs directory created"
}

# Main setup function
main() {
    print_status "Starting setup process..."
    
    check_python
    create_venv
    install_dependencies
    setup_config
    create_logs_dir
    
    print_success "Setup completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Update resources/key_store.json with your Azure OpenAI credentials"
    echo "2. Run: source venv/bin/activate"
    echo "3. Run: python -m src.handler.data_sync_handler (to initialize database)"
    echo "4. Run: python -m src.api.main (to start the server)"
    echo ""
    print_status "API will be available at:"
    echo "- API Documentation: http://localhost:8000/docs"
    echo "- Health Check: http://localhost:8000/api/health/"
}

# Run main function
main "$@"
