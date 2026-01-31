"""
FastAPI Server for 4th Down Bot Inference
Serves real-time recommendations and win probability.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import joblib
import numpy as np
from pathlib import Path

from models import FourthDownDecisionModel, WinProbabilityModel
from feature_engineering import NFLFeatureEngineer

app = FastAPI(title="NFL AI Coach API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

# Global model/scaler storage
models = {}
scalers = {}

class GameState(BaseModel):
    down: int
    ydstogo: int
    yardline_100: int
    score_differential: int
    qtr: int
    game_seconds_remaining: int
    posteam_timeouts_remaining: int
    defteam_timeouts_remaining: int

@app.on_event("startup")
def load_artifacts():
    try:
        # Load Scalers
        scalers['all'] = joblib.load(DATA_DIR / "scalers.pkl")
        
        # Load 4th Down Model
        fd_model = FourthDownDecisionModel(input_dim=6)
        fd_model.load_state_dict(torch.load(MODEL_DIR / "fourth_down_model.pt", map_location='cpu'))
        fd_model.eval()
        models['fourth_down'] = fd_model
        
        # Load Win Prob Model
        wp_model = WinProbabilityModel(input_dim=8)
        wp_model.load_state_dict(torch.load(MODEL_DIR / "win_prob_model.pt", map_location='cpu'))
        wp_model.eval()
        models['win_prob'] = wp_model
        
        print("✅ API Artifacts Loaded Successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not load models. Ensure training is complete. Error: {e}")

@app.post("/predict/fourth-down")
async def predict_fourth_down(state: GameState):
    if 'fourth_down' not in models:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # 1. 4th Down Decision
    fd_features = np.array([[
        state.ydstogo, state.yardline_100, state.score_differential,
        state.qtr, state.game_seconds_remaining, state.posteam_timeouts_remaining
    ]])
    fd_scaled = torch.FloatTensor(scalers['all']['fourth_down'].transform(fd_features))
    
    with torch.no_grad():
        conv_prob, fg_prob, epa = models['fourth_down'](fd_scaled)
    
    # 2. Win Probability
    wp_features = np.array([[
        state.score_differential, state.qtr, state.game_seconds_remaining,
        state.yardline_100, state.down, state.ydstogo,
        state.posteam_timeouts_remaining, state.defteam_timeouts_remaining
    ]])
    wp_scaled = torch.FloatTensor(scalers['all']['win_prob'].transform(wp_features))
    
    with torch.no_grad():
        win_prob = models['win_prob'](wp_scaled)
    
    return {
        "recommendation": "GO" if conv_prob.item() > 0.5 else "PUNT/KICK",
        "conversion_probability": round(conv_prob.item(), 4),
        "fg_probability": round(fg_prob.item(), 4),
        "expected_epa": round(epa.item(), 4),
        "win_probability": round(win_prob.item(), 4)
    }

@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": list(models.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
