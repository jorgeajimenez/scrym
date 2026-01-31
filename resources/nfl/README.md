# NFL AI Coach - Data-Driven Decision Support System

A comprehensive AI-powered football coaching system that provides real-time, data-driven recommendations for offensive play-calling, defensive strategy, 4th down decisions, win probability, and personnel optimization.

## Features

1. **Offensive Play-Caller** - Recommends optimal play types (pass, run, play-action, screen, draw) with probabilities and expected EPA
2. **Defensive Coordinator** - Predicts opponent's next play and recommends defensive formation
3. **4th Down Decision Engine** - Analyzes go/punt/field goal options with expected value calculations
4. **Win Probability Calculator** - Real-time win probability based on game situation
5. **Personnel Optimizer** - Recommends optimal personnel packages (11, 12, 21, 13, etc.)

## Technology Stack

### Backend
- **FastAPI** - REST API server
- **PyTorch** - Neural network models
- **nfl_data_py** - NFL data from nflverse
- **Python 3.8+**

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - API client

## Project Structure

```
nfl/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── models.py               # PyTorch model architectures
│   ├── data_loader.py          # NFL data loading
│   ├── feature_engineering.py  # Feature pipeline
│   └── train.py                # Model training script
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main dashboard
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/             # React components
│   ├── lib/
│   │   └── api.ts              # API client
│   └── types/
│       └── index.ts            # TypeScript types
├── models/                     # Saved PyTorch models (.pt files)
├── data/                       # Cached NFL data
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup Instructions

### 1. Backend Setup

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Download and Prepare Data

This will download 7 seasons of NFL play-by-play data (2018-2024):

```bash
cd backend
python data_loader.py
```

This may take 10-20 minutes depending on your internet connection. The data will be cached locally.

#### Train the Models

Train all 5 PyTorch models:

```bash
python train.py
```

Training time: 30-60 minutes depending on your hardware (CPU vs GPU).

**What this does:**
- Trains 5 neural network models on historical NFL data
- Saves trained models to `models/` directory
- Creates scalers and encoders for feature normalization
- Displays training progress and validation accuracy

**Expected output:**
```
Training offensive_model... Accuracy: ~0.65
Training defensive_model... Accuracy: ~0.62
Training fourth_down_model... Val Loss: ~0.45
Training win_prob_model... Accuracy: ~0.70
Training personnel_model... Accuracy: ~0.58
```

#### Start the FastAPI Server

```bash
# From the backend directory
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**Test the API:**
```bash
curl http://localhost:8000/health
```

### 2. Frontend Setup

#### Install Node Dependencies

```bash
cd frontend
npm install
```

#### Start the Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

### Web Dashboard

1. Open `http://localhost:3000` in your browser
2. Input the current game situation in the left sidebar:
   - Teams
   - Score
   - Quarter & Time
   - Down & Distance
   - Field Position
   - Timeouts
3. Click "Get Predictions" to get AI recommendations
4. View results in the 5 tabs:
   - **Offense**: Play type recommendations
   - **Defense**: Opponent play prediction
   - **4th Down**: Go/punt/kick analysis (only on 4th down)
   - **Win Prob**: Real-time win probability
   - **Personnel**: Optimal personnel package

### API Endpoints

**Base URL:** `http://localhost:8000`

#### Health Check
```bash
GET /health
```

#### Offensive Play-Calling
```bash
POST /predict/offensive
Content-Type: application/json

{
  "home_team": "KC",
  "away_team": "SF",
  "possession": "KC",
  "quarter": 2,
  "time_remaining": 120,
  "down": 2,
  "distance": 10,
  "yard_line": 50,
  "home_score": 14,
  "away_score": 17,
  "home_timeouts": 3,
  "away_timeouts": 2
}
```

**Response:**
```json
{
  "recommended_play": "pass",
  "probabilities": {
    "pass": 0.72,
    "run": 0.15,
    "play_action": 0.08,
    "screen": 0.03,
    "draw": 0.02
  },
  "expected_epa": 0.36,
  "confidence": 0.72
}
```

#### All Predictions
```bash
POST /predict/all
```
Get all 5 predictions in a single request.

## Model Details

### 1. Offensive Play-Caller Model
- **Architecture:** 4-layer feedforward neural network
- **Input Features:** down, distance, field position, score, time, team tendencies (12 features)
- **Output:** 5-class probabilities (pass, run, play-action, screen, draw)
- **Training Data:** ~150K successful plays (EPA > 0) from 2018-2024

### 2. Defensive Coordinator Model
- **Architecture:** 4-layer binary classification network
- **Input Features:** situation, opponent tendencies, game script (11 features)
- **Output:** Pass/run probability
- **Training Data:** ~250K plays with team-specific patterns

### 3. 4th Down Decision Model
- **Architecture:** Multi-output regression network
- **Input Features:** distance, field position, score, time (6 features)
- **Outputs:** Conversion probability, FG success probability, expected EPA
- **Training Data:** ~15K 4th down plays

### 4. Win Probability Model
- **Architecture:** 5-layer deep neural network
- **Input Features:** score differential, time, field position, situation (8 features)
- **Output:** Binary win probability
- **Training Data:** ~250K plays with game outcomes

### 5. Personnel Optimizer Model
- **Architecture:** 4-layer multi-class network
- **Input Features:** situation, intended play type (6 features)
- **Output:** Personnel package probabilities (11, 12, 21, 13, 22, 10)
- **Training Data:** ~50K plays with personnel data (2022-2024)

## Development

### Running Tests

Test individual models:

```bash
cd backend
python models.py  # Test model architectures
python feature_engineering.py  # Test feature pipeline
```

### Re-training Models

To retrain with updated data:

```bash
cd backend
python data_loader.py  # Download latest data
python train.py        # Retrain all models
```

### Frontend Development

```bash
cd frontend
npm run dev     # Development server with hot reload
npm run build   # Production build
npm run start   # Production server
```

## Troubleshooting

### Backend Issues

**"Model not loaded" error:**
- Make sure you've run `python train.py` first
- Check that `models/` directory contains .pt files

**Data download fails:**
- Check internet connection
- nfl_data_py may have rate limits - wait and retry
- Data is cached locally, so you only need to download once

**Training is slow:**
- Expected on CPU (30-60 min)
- Use GPU for faster training (5-10 min)
- Reduce batch_size in train.py if running out of memory

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 8000
- Check `frontend/.env.local` has correct API_URL
- Verify CORS is enabled in backend (already configured)

**npm install fails:**
- Use Node.js 18+
- Try `npm cache clean --force` and reinstall

## Future Enhancements

### V1.1 (Quick Wins)
- [ ] Example scenarios dropdown
- [ ] Export recommendations to PDF
- [ ] Historical comparison ("Teams in this situation chose...")
- [ ] Model confidence intervals

### V2.0 (Major Features)
- [ ] Live game data integration (ESPN/NFL.com API)
- [ ] Player-specific recommendations based on roster
- [ ] Historical tracking of recommendations vs outcomes
- [ ] Mobile-responsive design
- [ ] Multi-game tracking for season-long analytics
- [ ] Advanced visualizations with Recharts
- [ ] 2-point conversion decision model
- [ ] Timeout usage optimizer

## Data Sources

- **nflverse** (via nfl_data_py): Play-by-play data, FTN charting, rosters
- All data is publicly available NFL statistics
- Data is cached locally to minimize downloads

## License

This is a personal project for educational and analytical purposes.

## Credits

Built with:
- nfl_data_py by nflverse
- PyTorch
- FastAPI
- Next.js
- Tailwind CSS

---

## Quick Start Summary

```bash
# 1. Install backend dependencies
pip install -r requirements.txt

# 2. Train models (may take 30-60 min)
cd backend
python train.py

# 3. Start backend server
python main.py

# 4. In a new terminal, install frontend dependencies
cd frontend
npm install

# 5. Start frontend
npm run dev

# 6. Open browser to http://localhost:3000
```

Enjoy your AI Football Coach! 🏈
