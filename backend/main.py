"""
FastAPI Server for 4th Down Bot Inference
Serves real-time recommendations and win probability.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import torch
import joblib
import numpy as np
from pathlib import Path
import asyncio
from typing import List

from models import (
    FourthDownDecisionModel, WinProbabilityModel,
    OffensivePlayCallerModel, DefensiveCoordinatorModel, PersonnelOptimizerModel
)
from feature_engineering import NFLFeatureEngineer
from demo_scenarios import get_demo_scenarios, get_scenario_by_id
from websocket_manager import manager
from vision_agent import vision_service
from position_enrichment import extract_formation_features, calculate_coverage_gaps
from config import config

app = FastAPI(title="NFL AI Coach API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from mockups directory
MOCKUP_DIR = Path(__file__).parent.parent / "mockups"
app.mount("/static", StaticFiles(directory=str(MOCKUP_DIR)), name="static")

# Paths
MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

# Global model/scaler/encoder storage
models = {}
scalers = {}
encoders = {}

class GameState(BaseModel):
    down: int
    ydstogo: int
    yardline_100: int
    score_differential: int
    qtr: int
    game_seconds_remaining: int
    posteam_timeouts_remaining: int
    defteam_timeouts_remaining: int
    # Optional context for specific models
    half_seconds_remaining: int = 1800 # default
    red_zone: int = 0
    goal_to_go: int = 0
    two_min_drill: int = 0

@app.on_event("startup")
def load_artifacts():
    try:
        # Load Scalers & Encoders
        if (DATA_DIR / "scalers.pkl").exists():
            scalers['all'] = joblib.load(DATA_DIR / "scalers.pkl")
        if (DATA_DIR / "encoders.pkl").exists():
            encoders['all'] = joblib.load(DATA_DIR / "encoders.pkl")
        
        # Helper to load model safely
        def load_net(name, cls, **kwargs):
            path = MODEL_DIR / f"{name}.pt"
            if path.exists():
                model = cls(**kwargs)
                model.load_state_dict(torch.load(path, map_location='cpu'))
                model.eval()
                models[name] = model

        # Load Models
        load_net('fourth_down_model', FourthDownDecisionModel, input_dim=6)
        load_net('win_prob_model', WinProbabilityModel, input_dim=8)
        
        # Load new models if encoder classes exist to determine output dim
        if 'offensive' in encoders.get('all', {}):
            n_classes = len(encoders['all']['offensive'].classes_)
            load_net('offensive_model', OffensivePlayCallerModel, input_dim=11, num_classes=n_classes)
            
        load_net('defensive_model', DefensiveCoordinatorModel, input_dim=9)
        
        if 'personnel' in encoders.get('all', {}):
            n_classes = len(encoders['all']['personnel'].classes_)
            load_net('personnel_model', PersonnelOptimizerModel, input_dim=6, num_classes=n_classes)
        
        print(f"✅ API Artifacts Loaded: {list(models.keys())}")
    except Exception as e:
        print(f"⚠️ Warning: Model loading failed. Error: {e}")

@app.get("/demo/scenarios")
def list_demo_scenarios():
    """Return list of curated demo scenarios"""
    return get_demo_scenarios()

@app.get("/demo/load/{scenario_id}")
def load_demo_scenario(scenario_id: str):
    """Return the game state for a specific scenario"""
    scenario = get_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@app.post("/predict/offensive")
async def predict_offensive(state: GameState):
    if 'offensive_model' not in models: raise HTTPException(503, "Offensive model not loaded")
    
    # Input: [down, ydstogo, yardline_100, score_diff, qtr, game_sec, half_sec, rz, gtg, 2min, to_pos]
    feats = np.array([[
        state.down, state.ydstogo, state.yardline_100, state.score_differential,
        state.qtr, state.game_seconds_remaining, state.half_seconds_remaining,
        state.red_zone, state.goal_to_go, state.two_min_drill, state.posteam_timeouts_remaining
    ]])
    scaled = torch.FloatTensor(scalers['all']['offensive'].transform(feats))
    
    with torch.no_grad():
        logits = models['offensive_model'](scaled)
        probs = torch.softmax(logits, dim=1).numpy()[0]
    
    classes = encoders['all']['offensive'].classes_
    result = {cls: float(prob) for cls, prob in zip(classes, probs)}
    
    # Get top recommendation
    best_play = max(result, key=result.get)
    return {"recommendation": best_play, "probabilities": result}

@app.post("/predict/defensive")
async def predict_defensive(state: GameState):
    if 'defensive_model' not in models: raise HTTPException(503, "Defensive model not loaded")
    
    # Input: [down, ydstogo, yardline_100, score_diff, qtr, game_sec, rz, gtg, 2min]
    feats = np.array([[
        state.down, state.ydstogo, state.yardline_100, state.score_differential,
        state.qtr, state.game_seconds_remaining, 
        state.red_zone, state.goal_to_go, state.two_min_drill
    ]])
    scaled = torch.FloatTensor(scalers['all']['defensive'].transform(feats))
    
    with torch.no_grad():
        pass_prob = models['defensive_model'](scaled).item()
    
    return {
        "recommendation": "Pass Defense" if pass_prob > 0.5 else "Run Defense",
        "pass_probability": round(pass_prob, 4)
    }

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

@app.get("/")
def serve_frontend():
    """Serve the main frontend HTML"""
    return FileResponse(str(MOCKUP_DIR / "index.html"))

@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": list(models.keys())}

@app.get("/api/vision/status")
def vision_status():
    """Get Vision Agent status"""
    return {
        "mode": vision_service.mode,
        "connections": len(manager.active_connections),
        "fps": config.WS_FPS,
        "stream_api_key": config.STREAM_API_KEY
    }

@app.websocket("/ws/positions")
async def websocket_positions(websocket: WebSocket):
    """
    WebSocket endpoint for streaming player positions.
    Sends 30fps position updates to frontend canvas.
    """
    await manager.connect(websocket)

    try:
        # Start streaming task
        stream_task = asyncio.create_task(stream_positions_to_client(websocket))

        # Keep connection alive and handle client messages
        while True:
            try:
                data = await websocket.receive_text()
                # Handle commands if needed
                if data == "ping":
                    await manager.send_personal({"type": "pong"}, websocket)
            except WebSocketDisconnect:
                break

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)
        stream_task.cancel()

async def stream_positions_to_client(websocket: WebSocket):
    """Background task to stream position data to a specific client"""
    async for frame_data in vision_service.start_tracking_stream():
        try:
            await websocket.send_json({
                "type": "position_update",
                "data": frame_data
            })
        except Exception as e:
            print(f"Error streaming to client: {e}")
            break

@app.post("/predict/epa-live")
async def predict_epa_live(state: GameState, positions: List[dict]):
    """
    Enhanced EPA prediction using live player positions.
    Combines game state + Vision Agent data.
    """
    # Extract position features
    position_features = extract_formation_features(positions)

    # Calculate coverage gaps
    gaps = calculate_coverage_gaps(positions)

    return {
        "position_features": position_features,
        "coverage_gaps": gaps,
        "gap_count": len(gaps),
        "message": "Position-enhanced EPA coming soon (requires model retraining)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
