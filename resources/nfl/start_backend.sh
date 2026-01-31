#!/bin/bash

echo "🏈 Starting NFL AI Coach Backend..."
echo ""

# Check if models exist
if [ ! -f "models/offensive_model.pt" ]; then
    echo "⚠️  Models not found! You need to train them first."
    echo ""
    echo "Run these commands:"
    echo "  cd backend"
    echo "  python train.py"
    echo ""
    exit 1
fi

echo "✓ Models found"
echo "✓ Starting FastAPI server on http://localhost:8000"
echo ""

cd backend
python main.py
