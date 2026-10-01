#!/bin/bash
# Simple launcher - assumes venv is already set up

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Run './start.sh' first to set up the environment."
    exit 1
fi

source venv/bin/activate
python app.py
