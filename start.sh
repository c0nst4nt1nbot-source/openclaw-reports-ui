#!/bin/bash
# OpenClaw Reports UI - Startup Script

cd "$(dirname "$0")"

echo "================================================"
echo "OpenClaw Reports UI"
echo "================================================"

# Check if port 8000 is in use
PORT_PID=$(lsof -ti :8000 2>/dev/null)
if [ ! -z "$PORT_PID" ]; then
    echo "⚠️  Port 8000 is in use (PID: $PORT_PID)"
    echo "Stopping existing process..."
    kill -9 $PORT_PID 2>/dev/null
    sleep 1
    echo "✓ Port cleared"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Make sure python3-venv is installed: sudo apt install python3-venv"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the application
echo "Starting dashboard..."
python app.py
