# 🏗 NFL AI Coach: System Architecture

This document outlines the technical architecture for the "Playbook" system, derived from the core architectural patterns.

## 1. Data Layer
The foundation of the system is the retrieval and caching of historical NFL data.

*   **Primary Source:** `nflfastR` / `nfl_data_py` (Play-by-Play Data 2018-2024).
*   **Secondary Sources:**
    *   FTN Charting Data (2022-2024) for advanced metrics.
    *   Roster Data (2022-2024) for player matching.
    *   *Future:* ESPN Live API for real-time game state.
*   **Storage Strategy:** Local Parquet files cached in `data/`.
    *   `pbp_2018_2024.parquet` (~128MB)
    *   `ftn_2022_2024.parquet` (~2MB)

## 2. Data Processing Pipeline
Raw data is transformed into model-ready tensors through a strict pipeline.

*   **`NFLDataLoader`**: Abstraction layer for fetching/caching data.
*   **`NFLFeatureEngineer`**: Logic for extracting situational features.
*   **Feature Scaling**: `StandardScaler` applied to continuous variables (saved as `scalers.pkl`).
*   **Encoding**: `LabelEncoder` for categorical inputs (teams, personnel).

## 3. Intelligence Layer (PyTorch Models)
The brain of the system consists of specialized neural networks. **For the 4th Down Bot, we focus on Models 3 & 4.**

### Model 3: 4th Down Decision Engine
*   **Goal:** Optimize 4th down strategy (Go, Punt, FG).
*   **Input:** 6 Features (Down, Distance, Yardline, Score Diff, Time, Timeouts).
*   **Architecture:**
    *   `FC(64) + BN + ReLU + Dropout`
    *   `FC(32) + BN + ReLU`
    *   **3 Output Heads:**
        1.  Conversion Probability (Sigmoid)
        2.  FG Success Probability (Sigmoid)
        3.  Expected EPA (Linear)

### Model 4: Win Probability Calculator
*   **Goal:** Contextualize decisions with game-winning chances.
*   **Input:** 8 Features (Score Diff, Time, Field Pos, Down, Distance, Timeouts x2).
*   **Architecture:** Deep 5-Layer Network.
    *   `128 -> 64 -> 32 -> 16 -> 1`
*   **Output:** Single probability (0-1) representing the possession team's chance to win.

## 4. Backend Service (FastAPI)
The bridge between the Intelligence Layer and the UI.

*   **Framework:** FastAPI (Python 3.11).
*   **Endpoints:**
    *   `POST /predict/fourth-down`: Returns recommendation + probabilities.
    *   `POST /predict/win-probability`: Returns current WP.
    *   *(Future)* `POST /predict/offensive`, `POST /predict/defensive`.
*   **Latency Target:** < 50ms inference time per request.

## 5. Validation & Testing
*   **`train.py`**: Training pipeline with Adam optimizer and ReduceLROnPlateau.
*   **`test_models.py`**: Unit tests for model architecture dimensions.
*   **`validate_historical.py`**: Backtesting against known NFL game outcomes.

---
**Data Flow Summary:**
Raw Data → `NFLDataLoader` → Parquet → `FeatureEngineer` → Scaled Features → **PyTorch Models** → FastAPI → JSON Response.
