#!/bin/bash

echo "🏈 Starting NFL AI Coach Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Dependencies not installed!"
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo "✓ Dependencies installed"
echo "✓ Starting Next.js on http://localhost:3001"
echo ""

cd frontend
npm run dev
