#!/bin/bash

# Financial Data Processing System - Startup Script
# This script sets up the virtual environment, installs dependencies, and starts the server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
MAIN_MODULE="src.api.main:app"
HOST="0.0.0.0"
PORT="8000"
PID_FILE="$PROJECT_DIR/server.pid"
LOG_FILE="$PROJECT_DIR/logs/server.log"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

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

# Function to check if server is already running
check_server_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # Server is running
        else
            rm -f "$PID_FILE"  # Clean up stale PID file
            return 1  # Server is not running
        fi
    fi
    return 1  # No PID file, server not running
}

# Function to stop existing server
stop_existing_server() {
    if check_server_running; then
        print_warning "Server is already running (PID: $PID). Stopping it first..."
        kill "$PID" 2>/dev/null || true
        sleep 2
        
        # Force kill if still running
        if ps -p "$PID" > /dev/null 2>&1; then
            print_warning "Force killing server process..."
            kill -9 "$PID" 2>/dev/null || true
            sleep 1
        fi
        
        rm -f "$PID_FILE"
        print_success "Existing server stopped"
    fi
}

# Function to check Python installation
check_python() {
    # Try Python 3.11 first, then fall back to python3
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
        PYTHON_VERSION=$(python3.11 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    else
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    print_status "Found Python $PYTHON_VERSION (using $PYTHON_CMD)"
}

# Function to create virtual environment
create_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        print_success "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
}

# Function to activate virtual environment and install dependencies
setup_dependencies() {
    print_status "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    if [ -f "$REQUIREMENTS_FILE" ]; then
        print_status "Installing dependencies from requirements.txt..."
        pip install -r "$REQUIREMENTS_FILE"
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found!"
        exit 1
    fi
}

# Function to start the server
start_server() {
    print_status "Starting Financial Data Processing System server..."
    print_status "Host: $HOST"
    print_status "Port: $PORT"
    print_status "Log file: $LOG_FILE"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Start server in background
    nohup uvicorn "$MAIN_MODULE" \
        --host "$HOST" \
        --port "$PORT" \
        --reload \
        --log-level info \
        > "$LOG_FILE" 2>&1 &
    
    # Save PID
    echo $! > "$PID_FILE"
    
    # Wait a moment and check if server started successfully
    sleep 3
    if check_server_running; then
        print_success "Server started successfully!"
        print_status "Server PID: $(cat $PID_FILE)"
        print_status "API Documentation: http://$HOST:$PORT/docs"
        print_status "API Root: http://$HOST:$PORT/"
        print_status "To view logs: tail -f $LOG_FILE"
        print_status "To stop server: ./stop.sh"
    else
        print_error "Failed to start server. Check logs: $LOG_FILE"
        exit 1
    fi
}

# Main execution
main() {
    print_status "=== Financial Data Processing System Startup ==="
    print_status "Project directory: $PROJECT_DIR"
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Stop existing server if running
    stop_existing_server
    
    # Check Python installation
    check_python
    
    # Create virtual environment
    create_venv
    
    # Setup dependencies
    setup_dependencies
    
    # Start server
    start_server
    
    print_success "=== Startup Complete ==="
}

# Run main function
main "$@"
