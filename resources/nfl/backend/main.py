"""
FastAPI Backend Server for NFL AI Coach
Serves predictions from all 5 PyTorch models via REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import torch
import numpy as np
from pathlib import Path
import joblib

from models import create_model
from live_game_api import NFLLiveDataAPI

# Paths
MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

# Initialize FastAPI app
app = FastAPI(
    title="NFL AI Coach API",
    description="Data-driven decision support for football coaching",
    version="1.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Global model storage
MODELS = {}
SCALERS = {}
ENCODERS = {}


# ==================== Pydantic Models for Request/Response ====================

class GameState(BaseModel):
    """Current game situation"""
    home_team: str = Field(..., example="KC")
    away_team: str = Field(..., example="SF")
    possession: str = Field(..., example="KC")
    quarter: int = Field(..., ge=1, le=5, example=2)  # 5 for OT
    time_remaining: int = Field(..., description="Seconds remaining in game", example=1800)
    down: int = Field(..., ge=1, le=4, example=2)
    distance: int = Field(..., ge=1, le=99, example=10)
    yard_line: int = Field(..., ge=1, le=99, description="Yards from opponent goal", example=50)
    home_score: int = Field(..., ge=0, example=14)
    away_score: int = Field(..., ge=0, example=17)
    home_timeouts: int = Field(..., ge=0, le=3, example=3)
    away_timeouts: int = Field(..., ge=0, le=3, example=2)


class OffensivePlayResponse(BaseModel):
    """Response for offensive play-calling"""
    recommended_play: str
    probabilities: Dict[str, float]
    expected_epa: float
    confidence: float


class DefensiveResponse(BaseModel):
    """Response for defensive coordinator"""
    predicted_play_type: str
    pass_probability: float
    run_probability: float
    recommended_defense: str


class FourthDownResponse(BaseModel):
    """Response for 4th down decision"""
    recommendation: str
    go_for_it_prob: Optional[float]
    field_goal_prob: Optional[float]
    expected_values: Dict[str, float]


class WinProbabilityResponse(BaseModel):
    """Response for win probability"""
    possession_team_win_prob: float
    opponent_win_prob: float
    leverage: str


class PersonnelResponse(BaseModel):
    """Response for personnel optimizer"""
    recommended_personnel: str
    probabilities: Dict[str, float]
    reasoning: str


# ==================== Startup: Load Models ====================

@app.on_event("startup")
async def load_models():
    """Load all models, scalers, and encoders on startup"""
    global MODELS, SCALERS, ENCODERS

    print("Loading models...")

    try:
        # Load scalers
        scalers_file = DATA_DIR / "scalers.pkl"
        if scalers_file.exists():
            SCALERS = joblib.load(scalers_file)
            print(f"Loaded scalers: {list(SCALERS.keys())}")
        else:
            print("Warning: Scalers not found. Train models first.")
            return

        # Load encoders
        encoders_file = DATA_DIR / "encoders.pkl"
        if encoders_file.exists():
            ENCODERS = joblib.load(encoders_file)
            print(f"Loaded encoders: {list(ENCODERS.keys())}")

        # Load offensive model
        X_shape = SCALERS['offensive'].mean_.shape[0]
        le_off = joblib.load(MODEL_DIR / 'offensive_label_encoder.pkl')
        off_model = create_model('offensive', input_dim=X_shape, num_classes=len(le_off.classes_))
        off_model.load_state_dict(torch.load(MODEL_DIR / 'offensive_model.pt', map_location=device))
        off_model.to(device)
        off_model.eval()
        MODELS['offensive'] = (off_model, le_off)
        print("Loaded offensive model")

        # Load defensive model
        X_shape = SCALERS['defensive'].mean_.shape[0]
        def_model = create_model('defensive', input_dim=X_shape)
        def_model.load_state_dict(torch.load(MODEL_DIR / 'defensive_model.pt', map_location=device))
        def_model.to(device)
        def_model.eval()
        MODELS['defensive'] = def_model
        print("Loaded defensive model")

        # Load 4th down model
        X_shape = SCALERS['fourth_down'].mean_.shape[0]
        fourth_model = create_model('fourth_down', input_dim=X_shape)
        fourth_model.load_state_dict(torch.load(MODEL_DIR / 'fourth_down_model.pt', map_location=device))
        fourth_model.to(device)
        fourth_model.eval()
        MODELS['fourth_down'] = fourth_model
        print("Loaded 4th down model")

        # Load win probability model
        X_shape = SCALERS['win_prob'].mean_.shape[0]
        wp_model = create_model('win_prob', input_dim=X_shape)
        wp_model.load_state_dict(torch.load(MODEL_DIR / 'win_prob_model.pt', map_location=device))
        wp_model.to(device)
        wp_model.eval()
        MODELS['win_prob'] = wp_model
        print("Loaded win probability model")

        # Load personnel model
        X_shape = SCALERS['personnel'].mean_.shape[0]
        le_pers = joblib.load(MODEL_DIR / 'personnel_label_encoder.pkl')
        pers_model = create_model('personnel', input_dim=X_shape, num_personnel_groups=len(le_pers.classes_))
        pers_model.load_state_dict(torch.load(MODEL_DIR / 'personnel_model.pt', map_location=device))
        pers_model.to(device)
        pers_model.eval()
        MODELS['personnel'] = (pers_model, le_pers)
        print("Loaded personnel model")

        print(f"All models loaded successfully on {device}!")

    except Exception as e:
        print(f"Error loading models: {e}")
        print("You may need to train the models first by running: python backend/train.py")


# ==================== Helper Functions ====================

def game_state_to_features(state: GameState, model_type: str) -> np.ndarray:
    """Convert GameState to feature array for a specific model"""

    # Calculate derived features
    score_diff = state.home_score - state.away_score
    if state.possession == state.away_team:
        score_diff = -score_diff

    posteam_timeouts = state.home_timeouts if state.possession == state.home_team else state.away_timeouts
    defteam_timeouts = state.away_timeouts if state.possession == state.home_team else state.home_timeouts

    red_zone = 1 if state.yard_line <= 20 else 0
    goal_to_go = 1 if state.yard_line <= 10 else 0
    two_min_drill = 1 if (state.time_remaining <= 120 and state.quarter in [2, 4]) else 0

    # Calculate half_seconds_remaining (for 1st/3rd quarter, full half remaining)
    if state.quarter == 1:
        half_seconds_remaining = state.time_remaining
    elif state.quarter == 2:
        half_seconds_remaining = state.time_remaining
    elif state.quarter == 3:
        half_seconds_remaining = state.time_remaining
    elif state.quarter == 4:
        half_seconds_remaining = state.time_remaining
    else:  # OT
        half_seconds_remaining = state.time_remaining

    # Base features (common across models)
    base_features = {
        'down': state.down,
        'ydstogo': state.distance,
        'yardline_100': state.yard_line,
        'score_differential': score_diff,
        'qtr': state.quarter,
        'game_seconds_remaining': state.time_remaining,
        'half_seconds_remaining': half_seconds_remaining,
        'red_zone': red_zone,
        'goal_to_go': goal_to_go,
        'two_min_drill': two_min_drill,
        'posteam_timeouts_remaining': posteam_timeouts,
        'defteam_timeouts_remaining': defteam_timeouts,
        'team_encoded': 0,  # Default team encoding (would need actual team lookup)
        'team_pass_rate': 0.55,  # Default league average
        'team_avg_epa': 0.0  # Default
    }

    # Model-specific feature selection
    if model_type == 'offensive':
        features = ['down', 'ydstogo', 'yardline_100', 'score_differential', 'qtr',
                    'game_seconds_remaining', 'half_seconds_remaining', 'red_zone',
                    'goal_to_go', 'two_min_drill', 'posteam_timeouts_remaining', 'team_encoded']
    elif model_type == 'defensive':
        features = ['down', 'ydstogo', 'yardline_100', 'score_differential', 'qtr',
                    'game_seconds_remaining', 'team_pass_rate', 'team_avg_epa',
                    'red_zone', 'goal_to_go', 'two_min_drill']
    elif model_type == 'fourth_down':
        features = ['ydstogo', 'yardline_100', 'score_differential', 'qtr',
                    'game_seconds_remaining', 'posteam_timeouts_remaining']
    elif model_type == 'win_prob':
        features = ['score_differential', 'qtr', 'game_seconds_remaining', 'yardline_100',
                    'down', 'ydstogo', 'posteam_timeouts_remaining', 'defteam_timeouts_remaining']
    elif model_type == 'personnel':
        features = ['down', 'ydstogo', 'yardline_100', 'score_differential', 'red_zone', 'goal_to_go']
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    feature_array = np.array([[base_features[f] for f in features]])
    return feature_array


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NFL AI Coach API",
        "status": "running",
        "models_loaded": len(MODELS),
        "available_models": list(MODELS.keys())
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models": list(MODELS.keys()),
        "device": str(device)
    }


@app.post("/predict/offensive", response_model=OffensivePlayResponse)
async def predict_offensive_play(state: GameState):
    """Get offensive play recommendation"""
    if 'offensive' not in MODELS:
        raise HTTPException(status_code=503, detail="Model not loaded. Train models first.")

    try:
        # Prepare features
        features = game_state_to_features(state, 'offensive')
        features_scaled = SCALERS['offensive'].transform(features)

        # Predict
        model, label_encoder = MODELS['offensive']
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled).to(device)
            probs = model.predict_proba(features_tensor).cpu().numpy()[0]

        # Get play recommendations
        play_types = label_encoder.classes_
        probabilities = {play: float(prob) for play, prob in zip(play_types, probs)}

        recommended_idx = np.argmax(probs)
        recommended_play = play_types[recommended_idx]
        confidence = float(probs[recommended_idx])

        return OffensivePlayResponse(
            recommended_play=recommended_play,
            probabilities=probabilities,
            expected_epa=0.5 * confidence,  # Simplified EPA calculation
            confidence=confidence
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/defensive", response_model=DefensiveResponse)
async def predict_defensive_play(state: GameState):
    """Get defensive coordinator recommendation"""
    if 'defensive' not in MODELS:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        features = game_state_to_features(state, 'defensive')
        features_scaled = SCALERS['defensive'].transform(features)

        model = MODELS['defensive']
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled).to(device)
            pass_prob = float(model.predict_proba(features_tensor).cpu().numpy()[0][0])

        run_prob = 1.0 - pass_prob
        predicted_play = "pass" if pass_prob > 0.5 else "run"

        # Simple defensive recommendation
        if pass_prob > 0.65:
            recommended_defense = "Nickel / Prevent"
        elif pass_prob < 0.35:
            recommended_defense = "Base / Run Defend"
        else:
            recommended_defense = "Balanced Base Defense"

        return DefensiveResponse(
            predicted_play_type=predicted_play,
            pass_probability=pass_prob,
            run_probability=run_prob,
            recommended_defense=recommended_defense
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/fourth-down", response_model=FourthDownResponse)
async def predict_fourth_down(state: GameState):
    """Get 4th down decision recommendation"""
    if state.down != 4:
        raise HTTPException(status_code=400, detail="This endpoint is for 4th down situations only")

    if 'fourth_down' not in MODELS:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        features = game_state_to_features(state, 'fourth_down')
        features_scaled = SCALERS['fourth_down'].transform(features)

        model = MODELS['fourth_down']
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled).to(device)
            predictions = model.predict(features_tensor)

        conv_prob = float(predictions['conversion_prob'].cpu().numpy()[0][0])
        fg_prob = float(predictions['fg_success_prob'].cpu().numpy()[0][0])

        # Decision logic
        expected_values = {
            'go_for_it': conv_prob * 3.0,  # Simplified: assume TD value
            'field_goal': fg_prob * 3.0 if state.yard_line < 35 else 0.0,
            'punt': 1.5  # Expected field position value
        }

        recommendation = max(expected_values, key=expected_values.get)

        return FourthDownResponse(
            recommendation=recommendation,
            go_for_it_prob=conv_prob,
            field_goal_prob=fg_prob if state.yard_line < 35 else None,
            expected_values=expected_values
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/win-probability", response_model=WinProbabilityResponse)
async def predict_win_probability(state: GameState):
    """Get win probability"""
    if 'win_prob' not in MODELS:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        features = game_state_to_features(state, 'win_prob')
        features_scaled = SCALERS['win_prob'].transform(features)

        model = MODELS['win_prob']
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled).to(device)
            win_prob = float(model.predict_proba(features_tensor).cpu().numpy()[0][0])

        # Determine leverage (how important this play is)
        if 0.45 <= win_prob <= 0.55:
            leverage = "High"
        elif 0.35 <= win_prob <= 0.65:
            leverage = "Medium"
        else:
            leverage = "Low"

        return WinProbabilityResponse(
            possession_team_win_prob=win_prob * 100,
            opponent_win_prob=(1 - win_prob) * 100,
            leverage=leverage
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/personnel", response_model=PersonnelResponse)
async def predict_personnel(state: GameState):
    """Get personnel grouping recommendation"""
    if 'personnel' not in MODELS:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        features = game_state_to_features(state, 'personnel')
        features_scaled = SCALERS['personnel'].transform(features)

        model, label_encoder = MODELS['personnel']
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled).to(device)
            probs = model.predict_proba(features_tensor).cpu().numpy()[0]

        personnel_groups = label_encoder.classes_
        probabilities = {group: float(prob) for group, prob in zip(personnel_groups, probs)}

        recommended_idx = np.argmax(probs)
        recommended_personnel = personnel_groups[recommended_idx]

        # Simple reasoning
        reasoning = f"Best for {state.down} & {state.distance} at yard line {state.yard_line}"

        return PersonnelResponse(
            recommended_personnel=recommended_personnel,
            probabilities=probabilities,
            reasoning=reasoning
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/all")
async def predict_all(state: GameState):
    """Get all predictions at once"""
    try:
        results = {}

        if 'offensive' in MODELS:
            results['offensive'] = await predict_offensive_play(state)

        if 'defensive' in MODELS:
            results['defensive'] = await predict_defensive_play(state)

        if state.down == 4 and 'fourth_down' in MODELS:
            results['fourth_down'] = await predict_fourth_down(state)

        if 'win_prob' in MODELS:
            results['win_probability'] = await predict_win_probability(state)

        if 'personnel' in MODELS:
            results['personnel'] = await predict_personnel(state)

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/live-games")
async def get_live_games():
    """Get all live NFL games from ESPN API"""
    try:
        api = NFLLiveDataAPI()
        games = api.get_live_games()
        return {"games": games, "count": len(games)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live games: {str(e)}")


@app.get("/game/{game_id}")
async def get_game_state(game_id: str):
    """Get detailed game state for a specific game from ESPN API"""
    try:
        api = NFLLiveDataAPI()
        game_state = api.get_game_details(game_id)

        if game_state is None:
            raise HTTPException(status_code=404, detail="Game not found or data unavailable")

        return game_state
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching game details: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
