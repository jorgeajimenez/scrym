# NFL AI Coach - Quick Start Guide

## Current Status

✅ Backend code ready (FastAPI + PyTorch)
✅ Frontend code ready (Next.js + TypeScript)
✅ Frontend dependencies installed
⚠️ Models need to be trained (one-time setup)

## Step-by-Step Setup (First Time Only)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs FastAPI, PyTorch, nfl_data_py, and other backend libraries.

### 2. Train the AI Models

**Important:** This is a ONE-TIME step that takes 30-60 minutes.

```bash
cd backend
python train.py
```

**What this does:**
- Downloads NFL data (2018-2024 seasons) - ~5-10 min
- Engineers features from play-by-play data
- Trains 5 PyTorch neural networks
- Saves models to `models/` directory

**You'll see output like:**
```
Loading all NFL data...
Training offensive_model...
Epoch [10/50], Train Loss: 0.8234, Val Loss: 0.8456, Val Acc: 0.6234
...
Training complete!
All models saved to: models/
```

### 3. Start the Backend Server

Open a terminal and run:

```bash
./start_backend.sh
```

Or manually:
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Loading models...
All models loaded successfully on cpu!
```

**Keep this terminal open!** The backend needs to stay running.

### 4. Start the Frontend (New Terminal)

Open a **NEW** terminal window and run:

```bash
./start_frontend.sh
```

Or manually:
```bash
cd frontend
npm run dev
```

You should see:
```
✓ Ready in 2.1s
Local: http://localhost:3000
```

### 5. Open Your Browser

Go to: **http://localhost:3000**

You should see the NFL AI Coach dashboard!

## Using the Dashboard

1. **Left Sidebar** - Enter game situation:
   - Select teams (KC vs SF, etc.)
   - Enter scores
   - Set down, distance, field position
   - Enter quarter and time remaining

2. **Click "Get Predictions"** button

3. **View AI Recommendations** in tabs:
   - 🎯 **Offense** - What play to call
   - 🛡️ **Defense** - What opponent will do
   - 📊 **4th Down** - Go/punt/kick decision (only on 4th down)
   - 📈 **Win Prob** - Live win probability
   - 👥 **Personnel** - Optimal personnel package

## Example Scenario

Try this situation:
- **Teams:** KC (home) vs SF (away)
- **Possession:** KC
- **Score:** KC 14, SF 17
- **Quarter:** 4
- **Time:** 120 seconds (2:00)
- **Down:** 3rd
- **Distance:** 7 yards
- **Yard Line:** 45 yards from opponent goal

Click "Get Predictions" and see what the AI recommends!

## Troubleshooting

### "Model not loaded" Error

**Problem:** Backend can't find trained models
**Solution:** Run `cd backend && python train.py` first (one-time setup)

### Backend Won't Start

**Problem:** Port 8000 already in use
**Solution:** Kill existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

### Frontend Won't Start

**Problem:** Port 3000 already in use
**Solution:** Kill existing process:
```bash
lsof -ti:3000 | xargs kill -9
```

Or change port:
```bash
cd frontend
PORT=3001 npm run dev
```

### "Cannot connect to backend"

**Problem:** Frontend can't reach backend API
**Solution:**
1. Make sure backend is running (check terminal)
2. Visit http://localhost:8000/health in your browser
3. Should see: `{"status":"healthy","models":[...]}`

### Training Takes Forever

**Training on CPU:** 30-60 minutes (normal)
**Training on GPU:** 5-10 minutes

If you have a GPU:
```bash
# Check if PyTorch sees your GPU
python -c "import torch; print(torch.cuda.is_available())"
```

## Project Structure

```
nfl/
├── backend/               # FastAPI + PyTorch backend
│   ├── main.py           # API server
│   ├── models.py         # Neural network architectures
│   ├── train.py          # Model training script
│   └── ...
├── frontend/             # Next.js frontend ✅ EXISTS!
│   ├── app/
│   │   └── page.tsx      # Main dashboard
│   ├── components/       # React components
│   └── package.json
├── models/               # Saved models (created after training)
├── data/                 # Cached NFL data (created during training)
├── start_backend.sh      # Quick start script for backend
├── start_frontend.sh     # Quick start script for frontend
└── README.md             # Full documentation
```

## What to Run Daily

After the initial setup, you only need:

**Terminal 1:**
```bash
./start_backend.sh
```

**Terminal 2:**
```bash
./start_frontend.sh
```

**Browser:**
```
http://localhost:3000
```

That's it! 🏈

## Need Help?

Check the full README.md for:
- API documentation
- Model architecture details
- Advanced configuration
- Feature roadmap

---

**Summary:** The frontend EXISTS and is ready! You just need to train the models once, then run both servers.
