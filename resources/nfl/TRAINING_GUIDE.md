# NFL AI Coach - Training and Testing Guide

## Overview

Training the NFL AI Coach involves 5 neural network models that analyze different aspects of NFL game situations. This guide covers everything needed to train and test the models effectively.

## Prerequisites

### System Requirements
- **Python:** 3.8+ (you have 3.12.12 ✓)
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** ~500 MB for data and models
- **GPU:** Optional (speeds up training 5-10x)
- **Time:** 30-60 minutes on CPU, 5-10 minutes on GPU

### Dependencies

All dependencies are already installed:
- ✓ PyTorch 2.9.1
- ✓ FastAPI 0.128.0
- ✓ pandas 2.3.3
- ✓ scikit-learn 1.8.0
- ✓ nfl_data_py (via pip)

If you need to reinstall:
```bash
pip install -r requirements.txt
```

## Training Pipeline

### Step 1: Data Download (Already Complete ✓)

Your data is already cached:
- ✓ pbp_2018_2024.parquet (128.5 MB) - 7 seasons of play-by-play data
- ✓ ftn_2022_2024.parquet (2.0 MB) - FTN charting data
- ✓ rosters_2022_2024.parquet (1.0 MB) - Player rosters

To re-download fresh data:
```bash
cd backend
python data_loader.py
```

### Step 2: Train All Models

**Currently running in background...**

```bash
cd backend
python train.py
```

This trains all 5 models:
1. **Offensive Play-Caller** (~12 min)
2. **Defensive Coordinator** (~15 min)
3. **4th Down Decision** (~5 min)
4. **Win Probability** (~15 min)
5. **Personnel Optimizer** (~8 min)

**Expected Total Time:** 30-60 minutes on CPU

### What Happens During Training

For each model:
1. **Data Loading:** Loads cached NFL data from parquet files
2. **Feature Engineering:** Extracts relevant features (down, distance, score, etc.)
3. **Normalization:** Scales features using StandardScaler
4. **Train/Val Split:** 80/20 split with stratification
5. **Training Loop:** 50 epochs max with early stopping
6. **Model Saving:** Saves best model based on validation loss

### Training Configuration

Default hyperparameters (in `train.py`):
```python
batch_size = 512
epochs = 50 (with early stopping)
learning_rate = 0.001
optimizer = Adam
scheduler = ReduceLROnPlateau
```

### Expected Training Metrics

**Model 1: Offensive Play-Caller**
- Input: 12 features
- Output: 5 classes (pass, run, play-action, screen, draw)
- Expected Accuracy: ~65%
- Training Data: ~150K successful plays (EPA > 0)

**Model 2: Defensive Coordinator**
- Input: 11 features
- Output: Binary (pass vs run prediction)
- Expected Accuracy: ~62%
- Training Data: ~250K plays

**Model 3: 4th Down Decision**
- Input: 6 features
- Output: 3 values (conversion prob, FG prob, EPA)
- Expected Val Loss: ~0.45
- Training Data: ~15K 4th down plays

**Model 4: Win Probability**
- Input: 8 features
- Output: Binary (win probability)
- Expected Accuracy: ~70%
- Training Data: ~250K plays with outcomes

**Model 5: Personnel Optimizer**
- Input: 6 features
- Output: 6 classes (personnel packages)
- Expected Accuracy: ~58%
- Training Data: ~50K plays (2022-2024)

## Model Outputs

After training completes, you'll have:

```
models/
├── offensive_model.pt                  # ~60 KB
├── offensive_label_encoder.pkl         # ~500 B
├── defensive_model.pt                  # ~38 KB
├── fourth_down_model.pt                # ~19 KB
├── win_prob_model.pt                   # ~62 KB
├── personnel_model.pt                  # ~37 KB
└── personnel_label_encoder.pkl         # ~500 B

data/
├── scalers.pkl                         # Feature scalers for all models
└── encoders.pkl                        # Team encoders
```

## Testing

### Automated Test Suite

Run the comprehensive test suite:
```bash
cd backend
python test_models.py
```

This validates:
- ✓ All 5 model files exist
- ✓ Models load correctly
- ✓ Models make predictions
- ✓ Data files exist
- ✓ Scalers and encoders are valid

### Expected Test Output

```
======================================================================
NFL AI COACH - MODEL TESTING SUITE
======================================================================

1. Checking Model Files:
  ✓ offensive_model.pt exists
  ✓ defensive_model.pt exists
  ✓ fourth_down_model.pt exists
  ✓ win_prob_model.pt exists
  ✓ personnel_model.pt exists

2. Testing Model Loading and Inference:
  ✓ offensive_model loaded and tested successfully
  ✓ defensive_model loaded and tested successfully
  ✓ fourth_down_model loaded and tested successfully
  ✓ win_prob_model loaded and tested successfully
  ✓ personnel_model loaded and tested successfully

🎉 ALL TESTS PASSED! Models are ready for inference.
```

### Manual API Testing

Start the backend server:
```bash
cd backend
python main.py
# Or: uvicorn main:app --reload
```

Test with curl:
```bash
# Health check
curl http://localhost:8000/health

# Test offensive prediction
curl -X POST http://localhost:8000/predict/offensive \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Integration Testing with Frontend

1. Start backend (port 8000)
2. Start frontend (port 3000):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Open browser to `http://localhost:3000`
4. Input game scenario and click "Get Predictions"
5. Verify all 5 tabs show predictions

## Monitoring Training Progress

### Check Training Status

```bash
# View live training output
tail -f /tmp/claude/-Users-dr-gretchenboria-nfl/tasks/bfb79f3.output

# Or check the saved log
tail -f backend/training_output.log
```

### Training Progress Indicators

You'll see output like:
```
==============================================================
MODEL 1: OFFENSIVE PLAY-CALLER
==============================================================
Epoch [10/50], Train Loss: 1.2453, Val Loss: 1.3021, Val Acc: 0.5234
Epoch [20/50], Train Loss: 1.0124, Val Loss: 1.1234, Val Acc: 0.6012
...
Early stopping at epoch 35
Best validation loss: 0.9876
```

## Troubleshooting

### Training Issues

**Issue:** "Out of memory" error
**Fix:** Reduce batch_size in `train.py` from 512 to 256 or 128

**Issue:** Training is very slow
**Fix:** Normal on CPU. Consider using Google Colab with GPU for faster training

**Issue:** "No module named 'nfl_data_py'"
**Fix:** `pip install nfl_data_py`

**Issue:** Data download fails
**Fix:** Check internet connection. nfl_data_py may have rate limits - wait and retry

### Model Loading Issues

**Issue:** "Model not loaded" error in API
**Fix:** Ensure `python train.py` completed successfully

**Issue:** Architecture mismatch errors
**Fix:** Delete models/ directory and retrain from scratch

**Issue:** "scalers.pkl not found"
**Fix:** Run `python train.py` which creates scalers automatically

## Retraining from Scratch

To completely retrain:

```bash
# 1. Remove old models and artifacts
rm -rf models/*
rm -rf data/scalers.pkl data/encoders.pkl

# 2. Optionally download fresh data
cd backend
python data_loader.py

# 3. Train all models
python train.py

# 4. Test models
python test_models.py

# 5. Start server
python main.py
```

## Performance Optimization

### GPU Training (Recommended for Fast Training)

If you have NVIDIA GPU with CUDA:
```bash
# Check if PyTorch sees GPU
python -c "import torch; print(torch.cuda.is_available())"

# Training will automatically use GPU if available
python train.py
```

### Hyperparameter Tuning

Edit `train.py` to experiment:
- `batch_size`: Larger = faster but more memory (256, 512, 1024)
- `learning_rate`: Try 0.0001 to 0.01
- `epochs`: Increase max epochs (50 → 100)
- Early stopping patience: Adjust patience in training loops

## Data Freshness

### Update with Latest NFL Data

To include the most recent games:

```bash
cd backend
python data_loader.py  # Downloads latest available data
python train.py        # Retrain with new data
```

Note: nfl_data_py is usually updated weekly during the season.

## Model Evaluation

### Evaluate Model Performance

Create a test set and evaluate:
```python
# In train.py, after training
X_test, y_test = train_test_split(X, y, test_size=0.1)
model.eval()
with torch.no_grad():
    predictions = model(X_test)
    accuracy = compute_accuracy(predictions, y_test)
    print(f"Test Accuracy: {accuracy}")
```

### Metrics to Track

- **Classification models:** Accuracy, Precision, Recall, F1-Score
- **Regression models:** MAE, MSE, R²
- **Win Probability:** Calibration plots, Brier score

## Next Steps After Training

1. ✓ Run `python test_models.py` to validate
2. ✓ Start backend: `python main.py`
3. ✓ Test API endpoints with curl or Postman
4. ✓ Start frontend and test full integration
5. ✓ Evaluate model predictions on real game scenarios
6. Consider adding:
   - Model versioning
   - A/B testing different architectures
   - Confidence intervals
   - Explainability (SHAP values)

## Support

If you encounter issues:
1. Check the logs: `backend/training_output.log`
2. Verify all dependencies: `pip list`
3. Test individual components: `python models.py`, `python feature_engineering.py`
4. Review error messages carefully
5. Ensure Python 3.8+

---

**Current Status:** Training in progress...
**Estimated completion:** Check with `tail -f backend/training_output.log`
