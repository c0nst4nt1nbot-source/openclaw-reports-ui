#!/bin/bash
# OpenClaw Reports UI - Stop Script

echo "Stopping OpenClaw Reports UI..."

# Find and kill process on port 8000
PORT_PID=$(lsof -ti :8000 2>/dev/null)

if [ -z "$PORT_PID" ]; then
    echo "No process found on port 8000"
else
    echo "Found process $PORT_PID on port 8000"
    kill -9 $PORT_PID
    echo "✓ Server stopped"
fi
