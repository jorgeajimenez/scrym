#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")"

echo "🚀 Starting NFL AI Coach Backend..."

# Check for virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️ Warning: No virtual environment found. Running with global python."
fi

# Start the server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
