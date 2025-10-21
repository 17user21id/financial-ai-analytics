#!/bin/bash

# Financial Data Processing System - Shutdown Script
# This script stops the running server gracefully

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_DIR/server.pid"

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

# Function to check if server is running
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

# Function to stop server gracefully
stop_server() {
    if check_server_running; then
        PID=$(cat "$PID_FILE")
        print_status "Stopping server (PID: $PID)..."
        
        # Try graceful shutdown first
        kill "$PID" 2>/dev/null || true
        
        # Wait for graceful shutdown
        for i in {1..10}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                print_success "Server stopped gracefully"
                rm -f "$PID_FILE"
                return 0
            fi
            sleep 1
        done
        
        # Force kill if still running
        print_warning "Server didn't stop gracefully, force killing..."
        kill -9 "$PID" 2>/dev/null || true
        sleep 1
        
        if ! ps -p "$PID" > /dev/null 2>&1; then
            print_success "Server force stopped"
            rm -f "$PID_FILE"
        else
            print_error "Failed to stop server"
            exit 1
        fi
    else
        print_warning "No server is currently running"
    fi
}

# Function to kill any remaining uvicorn processes
cleanup_uvicorn() {
    print_status "Cleaning up any remaining uvicorn processes..."
    pkill -f "uvicorn.*src.api.main:app" 2>/dev/null || true
    sleep 1
}

# Main execution
main() {
    print_status "=== Financial Data Processing System Shutdown ==="
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Stop server
    stop_server
    
    # Cleanup any remaining processes
    cleanup_uvicorn
    
    print_success "=== Shutdown Complete ==="
}

# Run main function
main "$@"
