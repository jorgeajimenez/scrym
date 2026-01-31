#!/bin/bash

echo "🏈 NFL AI Coach - Setup Verification"
echo "===================================="
echo ""

# Check backend files
echo "✓ Backend Directory:"
echo "  - data_loader.py: $([ -f backend/data_loader.py ] && echo '✓' || echo '✗')"
echo "  - feature_engineering.py: $([ -f backend/feature_engineering.py ] && echo '✓' || echo '✗')"
echo "  - models.py: $([ -f backend/models.py ] && echo '✓' || echo '✗')"
echo "  - train.py: $([ -f backend/train.py ] && echo '✓' || echo '✗')"
echo "  - main.py: $([ -f backend/main.py ] && echo '✓' || echo '✗')"
echo ""

# Check frontend files
echo "✓ Frontend Directory:"
echo "  - package.json: $([ -f frontend/package.json ] && echo '✓' || echo '✗')"
echo "  - app/page.tsx: $([ -f frontend/app/page.tsx ] && echo '✓' || echo '✗')"
echo "  - components: $([ -d frontend/components ] && echo '✓' || echo '✗')"
echo "  - node_modules: $([ -d frontend/node_modules ] && echo '✓ (installed)' || echo '✗ (run npm install)')"
echo ""

# Check if models are trained
echo "⚠️  Trained Models:"
if [ -f "models/offensive_model.pt" ]; then
    echo "  - ✓ Models are trained and ready!"
else
    echo "  - ✗ Models NOT trained yet"
    echo "    Run: cd backend && python train.py"
fi
echo ""

echo "===================================="
echo ""
echo "Next Steps:"
echo "1. Train models (if not done): cd backend && python train.py"
echo "2. Start backend: ./start_backend.sh"
echo "3. Start frontend: ./start_frontend.sh"
echo "4. Open: http://localhost:3001"
echo ""
