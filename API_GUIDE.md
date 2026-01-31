# 🔌 API Integration Guide

This document provides `curl` commands to test the FastAPI endpoints with single-line JSON data.

## 1. Starting the Server
Before running any commands, start the backend server:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 2. Test Endpoints

### 🏈 4th Down Decision (Head Coach)
**Scenario:** 4th & 1 on the Opponent 45. Tie game.
```bash
curl -X POST "http://localhost:8000/predict/fourth-down" -H "Content-Type: application/json" -d '{"down":4,"ydstogo":1,"yardline_100":45,"score_differential":0,"qtr":3,"game_seconds_remaining":900,"posteam_timeouts_remaining":3,"defteam_timeouts_remaining":3}'
```

### 📋 Offensive Play Call (Offensive Coord)
**Scenario:** 1st & 10 on Own 20. Down by 7.
```bash
curl -X POST "http://localhost:8000/predict/offensive" -H "Content-Type: application/json" -d '{"down":1,"ydstogo":10,"yardline_100":80,"score_differential":-7,"qtr":1,"game_seconds_remaining":3000,"posteam_timeouts_remaining":3,"defteam_timeouts_remaining":3,"half_seconds_remaining":1800,"red_zone":0,"goal_to_go":0,"two_min_drill":0}'
```

### 🛡️ Defensive Tendency (Defensive Coord)
**Scenario:** 3rd & 15. Likely Pass situation.
```bash
curl -X POST "http://localhost:8000/predict/defensive" -H "Content-Type: application/json" -d '{"down":3,"ydstogo":15,"yardline_100":60,"score_differential":0,"qtr":2,"game_seconds_remaining":1500,"posteam_timeouts_remaining":2,"defteam_timeouts_remaining":2,"red_zone":0,"goal_to_go":0,"two_min_drill":0}'
```

### 🏟️ Personnel Optimizer
**Scenario:** 1st & Goal. Heavy set recommendation.
```bash
curl -X POST "http://localhost:8000/predict/personnel" -H "Content-Type: application/json" -d '{"down":1,"ydstogo":2,"yardline_100":2,"score_differential":0,"qtr":4,"game_seconds_remaining":600,"posteam_timeouts_remaining":3,"defteam_timeouts_remaining":3,"red_zone":1,"goal_to_go":1}'
```

### ♟️ Formation Prediction
**Scenario:** Visualizing a "Pass" play with "11" personnel.
```bash
curl -X POST "http://localhost:8000/predict/formation" -H "Content-Type: application/json" -d '{"play_type":"pass","personnel":"11","ydstogo":10}'
```

### 🧠 Gemini Assistant Coach
**Scenario:** Get a natural language explanation for a decision. This endpoint synthesizes raw analytics with team roster context.
```bash
# Optional: Requires GEMINI_API_KEY environment variable.
curl -X POST "http://localhost:8000/analyze/play" -H "Content-Type: application/json" -d '{"state":{"down":4,"ydstogo":1,"yardline_100":45,"score_differential":0,"qtr":3,"game_seconds_remaining":900,"posteam_timeouts_remaining":3,"defteam_timeouts_remaining":3},"recommendation":"GO (High Confidence)","team_abbr":"KC"}'
```

---

## 3. Utility Endpoints

### 🏥 Health Check & Troubleshooting
Verify the API is up and models are loaded:
```bash
curl -X GET "http://localhost:8000/health"
```

**If Gemini is not working:**
Ensure you have installed the updated requirements: `pip install -r backend/requirements.txt` and exported your key: `export GEMINI_API_KEY="..."`. The API will gracefully return an error message if the key is missing rather than crashing.
...
### 🏥 Health Check & Troubleshooting
Verify the API is up and models are loaded:
```bash
curl -X GET "http://localhost:8000/health"
```

**If you see `{"status":"error"}`:**
The response will include a `detail` field with a full Python traceback explaining why the models failed to load (e.g., missing `.pt` files or path errors).