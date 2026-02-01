"""
Manual Verification Script for NFL AI Coach Models
"""
import argparse
import torch
import joblib
import numpy as np
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))
from architectures import FourthDownDecisionModel, WinProbabilityModel

# Correct Paths
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

def load_artifacts():
    print(f"📥 Loading from {MODEL_DIR}...")
    try:
        scaler_path = DATA_DIR / "scalers.pkl"
        scalers = joblib.load(scaler_path)
        
        fd_model = FourthDownDecisionModel(input_dim=6)
        fd_model.load_state_dict(torch.load(MODEL_DIR / "fourth_down_model.pt", map_location='cpu'))
        fd_model.eval()
        
        wp_model = WinProbabilityModel(input_dim=8)
        wp_model.load_state_dict(torch.load(MODEL_DIR / "win_prob_model.pt", map_location='cpu'))
        wp_model.eval()
        
        return fd_model, wp_model, scalers
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--down", type=int, required=True)
    parser.add_argument("--togo", type=int, required=True)
    parser.add_argument("--ydline", type=int, required=True)
    parser.add_argument("--score_diff", type=int, required=True)
    parser.add_argument("--qtr", type=int, required=True)
    parser.add_argument("--time_rem", type=int, required=True)
    parser.add_argument("--to_pos", type=int, required=True)
    parser.add_argument("--to_def", type=int, required=True)
    args = parser.parse_args()
    
    fd_model, wp_model, scalers = load_artifacts()
    
    fd_input = np.array([[args.togo, args.ydline, args.score_diff, args.qtr, args.time_rem, args.to_pos]])
    fd_scaled = torch.FloatTensor(scalers['fourth_down'].transform(fd_input))
    with torch.no_grad():
        conv_prob, fg_prob, epa = fd_model(fd_scaled)
        
    wp_input = np.array([[args.score_diff, args.qtr, args.time_rem, args.ydline, args.down, args.togo, args.to_pos, args.to_def]])
    wp_scaled = torch.FloatTensor(scalers['win_prob'].transform(wp_input))
    with torch.no_grad():
        win_prob = wp_model(wp_scaled)
        
    print(f"\n🤖 4th Down: Conv {conv_prob.item():.2%}, FG {fg_prob.item():.2%}, EPA {epa.item():.4f}")
    print(f"🏆 Win Prob: {win_prob.item():.2%}")

if __name__ == "__main__":
    main()