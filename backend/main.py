"""
FastAPI Server for 4th Down Bot Inference
Serves real-time recommendations, win probability, and simulation logic.
"""

import sys
from pathlib import Path
import random

# Add the backend directory to sys.path to allow imports from local modules
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import joblib
import numpy as np

# Import from the renamed file
from architectures import (
    FourthDownDecisionModel, WinProbabilityModel,
    OffensivePlayCallerModel, DefensiveCoordinatorModel, PersonnelOptimizerModel
)
from feature_engineering import NFLFeatureEngineer
from demo_scenarios import get_demo_scenarios, get_scenario_by_id
from formation_logic import get_offensive_formation, get_defensive_formation, generate_formation_payload
from gemini_coach import coach_ai

app = FastAPI(title="NFL AI Coach API")

# ... (Previous Middleware) ...

# Input Models
class AnalysisRequest(BaseModel):
    state: GameState
    recommendation: str
    team_abbr: str = "KC"

@app.post("/analyze/play")
async def analyze_play(req: AnalysisRequest):
    """
    Get a natural language summary from Gemini 1.5 Pro.
    """
    analysis = coach_ai.analyze_situation(req.state, req.recommendation, req.team_abbr)
    return {"analysis": analysis}

@app.post("/predict/formation")
def predict_formation(req: FormationRequest):
    play_type: str = "pass"
    personnel: str = "11"
    ydstogo: int = 10
    is_2min: int = 0
    is_defense: bool = False
    is_pass_likely: float = 0.5
    is_goal_line: bool = False

@app.post("/predict/formation")
def predict_formation(req: FormationRequest):
    """
    Returns visual coordinates for the suggested formation.
    """
    if req.is_defense:
        formation_name = get_defensive_formation(req.personnel, req.is_pass_likely, req.is_goal_line)
    else:
        formation_name = get_offensive_formation(req.play_type, req.personnel, req.ydstogo, req.is_2min)
        
    coords = generate_formation_payload(formation_name)
    
    return {
        "formation_name": formation_name,
        "players": coords
    }

# ... (Rest of the file remains unchanged)


# Paths relative to this file
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR.parent / "data" # Scalers are usually in root data/

# Global storage
models = {}
scalers = {}
encoders = {}
loading_error = None

# --- Data Models (Aligned with INTEGRATION_GUIDE.md) ---

class GameState(BaseModel):
    game_id: str = "sim_001"
    # Context
    qtr: int
    time_remaining: int # Game Clock
    play_clock: int = 40
    clock_running: bool = True
    score_home: int
    score_away: int
    possession: str = 'home'
    
    # Field State
    down: int
    ydstogo: int
    yardline_100: int
    
    # Context (For Model Features)
    score_differential: int # Calculated on Frontend or Backend, but passed here for consistency
    game_seconds_remaining: int # Total seconds (e.g. Q4 15:00 = 900)
    
    # Logic Flags
    red_zone: int = 0
    goal_to_go: int = 0
    two_min_drill: int = 0
    
    # Timeouts
    posteam_timeouts_remaining: int
    defteam_timeouts_remaining: int
    
    # Legacy/Derived fields for compatibility with existing models (optional defaults)
    half_seconds_remaining: int = 1800 

class SimulationRequest(BaseModel):
    current_state: GameState
    action_taken: str # "Pass", "Run", "Punt", "FG"

class SimulationResponse(BaseModel):
    new_state: GameState
    play_result: dict

# --- Startup ---

@app.on_event("startup")
def load_artifacts():
    global loading_error
    try:
        print(f"📂 Loading artifacts. Models: {MODEL_DIR}, Data: {DATA_DIR}")
        
        # Load Scalers & Encoders (Check both root and backend/data)
        scaler_path = DATA_DIR / "scalers.pkl"
        if not scaler_path.exists(): scaler_path = BASE_DIR / "data" / "scalers.pkl"
        
        encoder_path = DATA_DIR / "encoders.pkl"
        if not encoder_path.exists(): encoder_path = BASE_DIR / "data" / "encoders.pkl"

        if scaler_path.exists():
            scalers['all'] = joblib.load(scaler_path)
            print("✅ Scalers loaded")
        else:
            print(f"❌ scalers.pkl not found at {scaler_path}")
            
        if encoder_path.exists():
            encoders['all'] = joblib.load(encoder_path)
            print("✅ Encoders loaded")
        
        def load_net(name, cls, **kwargs):
            path = MODEL_DIR / f"{name}.pt"
            if path.exists():
                model = cls(**kwargs)
                model.load_state_dict(torch.load(path, map_location='cpu'))
                model.eval()
                models[name] = model
                print(f"✅ Loaded {name}")
            else:
                print(f"❌ {name}.pt not found at {path}")

        # Load Models
        load_net('fourth_down_model', FourthDownDecisionModel, input_dim=6)
        load_net('win_prob_model', WinProbabilityModel, input_dim=8)
        
        if 'offensive' in encoders.get('all', {}):
            n_classes = len(encoders['all']['offensive'].classes_)
            load_net('offensive_model', OffensivePlayCallerModel, input_dim=11, num_classes=n_classes)
            
        load_net('defensive_model', DefensiveCoordinatorModel, input_dim=9)
        
        if 'personnel' in encoders.get('all', {}):
            n_classes = len(encoders['all']['personnel'].classes_)
            load_net('personnel_model', PersonnelOptimizerModel, input_dim=6, num_classes=n_classes)
        
        print(f"🚀 API Ready. Loaded models: {list(models.keys())}")
        
    except Exception as e:
        import traceback
        loading_error = f"{str(e)}\n{traceback.format_exc()}"
        print(f"🔥 CRITICAL ERROR loading models:\n{loading_error}")

@app.get("/health")
def health():
    if loading_error:
        return {"status": "error", "detail": loading_error}
    return {"status": "ok", "models_loaded": list(models.keys())}

# --- Demo Endpoints ---

@app.get("/demo/scenarios")
def list_demo_scenarios():
    return get_demo_scenarios()

@app.get("/demo/load/{scenario_id}")
def load_demo_scenario(scenario_id: str):
    scenario = get_scenario_by_id(scenario_id)
    if not scenario: raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

# --- Prediction Endpoints ---

@app.post("/predict/fourth-down")
async def predict_fourth_down(state: GameState):
    if 'fourth_down_model' not in models: raise HTTPException(503, "Models not loaded")
    
    fd_features = np.array([[ 
        state.ydstogo, state.yardline_100, state.score_differential,
        state.qtr, state.game_seconds_remaining, state.posteam_timeouts_remaining
    ]])
    fd_scaled = torch.FloatTensor(scalers['all']['fourth_down'].transform(fd_features))
    
    with torch.no_grad():
        conv_prob, fg_prob, epa = models['fourth_down_model'](fd_scaled)
        
    wp_features = np.array([[ 
        state.score_differential, state.qtr, state.game_seconds_remaining,
        state.yardline_100, state.down, state.ydstogo,
        state.posteam_timeouts_remaining, state.defteam_timeouts_remaining
    ]])
    wp_scaled = torch.FloatTensor(scalers['all']['win_prob'].transform(wp_features))
    
    with torch.no_grad():
        win_prob = models['win_prob_model'](wp_scaled)
    
    return {
        "recommendation": "GO" if conv_prob.item() > 0.5 else "PUNT/KICK",
        "conversion_probability": round(conv_prob.item(), 4),
        "fg_probability": round(fg_prob.item(), 4),
        "expected_epa": round(epa.item(), 4),
        "win_probability": round(win_prob.item(), 4)
    }

@app.post("/predict/offensive")
async def predict_offensive(state: GameState):
    if 'offensive_model' not in models: raise HTTPException(503, "Offensive model not loaded")
    
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
    recommendation = max(result, key=result.get)

    # Get Personnel (Optional, could be separate call but efficient here)
    # Just default to "11" if not separately predicted
    personnel = "11" 
    
    # Get Formation Logic
    formation_data = formation_logic.get_offensive_formation(
        play_type=recommendation,
        personnel=personnel,
        ydstogo=state.ydstogo,
        is_2min=bool(state.two_min_drill)
    )

    return {
        "recommendation": recommendation, 
        "probabilities": result,
        "formation_suggested": formation_data['formation_name'],
        "formation_data": formation_data
    }

@app.post("/predict/defensive")
async def predict_defensive(state: GameState):
    if 'defensive_model' not in models: raise HTTPException(503, "Defensive model not loaded")
    
    feats = np.array([[ 
        state.down, state.ydstogo, state.yardline_100, state.score_differential,
        state.qtr, state.game_seconds_remaining, state.red_zone, state.goal_to_go, state.two_min_drill
    ]])
    
    scaled = torch.FloatTensor(scalers['all']['defensive'].transform(feats))
    with torch.no_grad():
        pass_prob = models['defensive_model'](scaled).item()
    
    # Get Defensive Formation
    formation_data = formation_logic.get_defensive_formation(
        off_personnel="11", # Default assumption if not provided
        pass_prob=pass_prob,
        is_goal_line=bool(state.goal_to_go)
    )

    return {
        "recommendation": "Pass Defense" if pass_prob > 0.5 else "Run Defense", 
        "pass_probability": round(pass_prob, 4),
        "formation_suggested": formation_data['formation_name'],
        "formation_data": formation_data
    }

@app.post("/predict/personnel")
async def predict_personnel(state: GameState):
    if 'personnel_model' not in models: raise HTTPException(503, "Personnel model not loaded")
    
    feats = np.array([[ 
        state.down, state.ydstogo, state.yardline_100, state.score_differential,
        state.red_zone, state.goal_to_go
    ]])
    scaled = torch.FloatTensor(scalers['all']['personnel'].transform(feats))
    
    with torch.no_grad():
        logits = models['personnel_model'](scaled)
        probs = torch.softmax(logits, dim=1).numpy()[0]
        
    classes = encoders['all']['personnel'].classes_
    result = {cls: float(prob) for cls, prob in zip(classes, probs)}
    
    return {"recommendation": max(result, key=result.get), "probabilities": result}

# --- Simulation Endpoint ---

@app.post("/simulate/step", response_model=SimulationResponse)
async def simulate_step(req: SimulationRequest):
    """
    Simulates the result of a single play and advances the clock/state.
    """
    state = req.current_state
    action = req.action_taken
    
    # 1. Determine Outcome (Simplified probabilistic logic for Demo)
    # Ideally this would use a 'Yards Gained Model'
    
    yards_gained = 0
    is_complete = False
    is_turnover = False
    description = ""
    clock_impact = "running"
    
    if action == "Pass":
        roll = random.random()
        if roll < 0.60: # 60% Completion
            is_complete = True
            yards_gained = random.choice([5, 8, 12, 20, 45]) # Weighted randoms preferred
            description = f"Pass complete for {yards_gained} yards."
        elif roll < 0.95: # Incomplete
            is_complete = False
            yards_gained = 0
            description = "Pass incomplete."
            clock_impact = "stopped"
        else: # Interception
            is_turnover = True
            description = "INTERCEPTED! Turnover."
            clock_impact = "stopped"
            
    elif action == "Run":
        yards_gained = random.choice([-2, 1, 3, 4, 4, 5, 8, 15])
        description = f"Run for {yards_gained} yards."
        clock_impact = "running"
        
    elif action == "Punt":
        yards_gained = 40
        description = "Punt 40 yards."
        clock_impact = "stopped" # Change of possession
        is_turnover = True # Effectively
        
    # 2. Update Field Position
    new_ydstogo = state.ydstogo - yards_gained
    new_yardline_100 = state.yardline_100 - yards_gained
    new_down = state.down + 1
    
    # Check 1st Down
    if new_ydstogo <= 0:
        new_down = 1
        new_ydstogo = 10
        description += " 1ST DOWN!"
    
    # Check Touchdown
    if new_yardline_100 <= 0:
        state.score_home += 7 # Assume home scores for demo simplicity
        description += " TOUCHDOWN!"
        new_yardline_100 = 75 # Touchback
        new_down = 1
        new_ydstogo = 10
        is_turnover = True # Kickoff next
    
    # Check Turnover on Downs
    if new_down > 4 and not is_turnover:
        is_turnover = True
        description += " Turnover on Downs."
        
    # 3. Update Clock
    time_elapsed = 6 if clock_impact == "stopped" else 40
    new_time_remaining = max(0, state.time_remaining - time_elapsed)
    new_game_seconds = max(0, state.game_seconds_remaining - time_elapsed)
    
    # 4. Construct New State
    new_state = state.copy(deep=True)
    new_state.time_remaining = new_time_remaining
    new_state.game_seconds_remaining = new_game_seconds
    new_state.clock_running = (clock_impact == "running")
    new_state.play_clock = 40 # Reset
    
    if is_turnover:
        # Flip Field logic omitted for brevity, just resetting downs for demo
        new_down = 1
        new_ydstogo = 10
        new_state.clock_running = False
        
    new_state.down = new_down
    new_state.ydstogo = new_ydstogo
    new_state.yardline_100 = new_yardline_100
    
    return {
        "new_state": new_state,
        "play_result": {
            "yards_gained": yards_gained,
            "description": description,
            "is_turnover": is_turnover,
            "clock_impact": clock_impact
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)