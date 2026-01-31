"""
Training Pipeline for 4th Down and Win Probability Models
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
from pathlib import Path

from data_loader import NFLDataLoader
from feature_engineering import NFLFeatureEngineer
from models import FourthDownDecisionModel, WinProbabilityModel, save_model

# Constants
MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 512
EPOCHS = 50

def train_win_prob(X, y):
    print("\n--- Training Win Probability Model ---")
    X_tensor = torch.FloatTensor(X).to(DEVICE)
    y_tensor = torch.FloatTensor(y).view(-1, 1).to(DEVICE)
    
    dataset = TensorDataset(X_tensor, y_tensor)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    model = WinProbabilityModel(X.shape[1]).to(DEVICE)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for batch_X, batch_y in loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss/len(loader):.4f}")
            
    save_model(model, MODEL_DIR / "win_prob_model.pt")
    return model

def train_fourth_down(X, y_data):
    print("\n--- Training 4th Down Decision Model ---")
    X_tensor = torch.FloatTensor(X).to(DEVICE)
    
    # Targets: conv_prob, fg_prob, epa
    y_conv = torch.FloatTensor(y_data['converted'].values).view(-1, 1).to(DEVICE)
    y_fg = torch.FloatTensor(y_data['fg_made'].values).view(-1, 1).to(DEVICE)
    y_epa = torch.FloatTensor(y_data['epa'].values).view(-1, 1).to(DEVICE)
    
    dataset = TensorDataset(X_tensor, y_conv, y_fg, y_epa)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    model = FourthDownDecisionModel(X.shape[1]).to(DEVICE)
    criterion_bce = nn.BCELoss()
    criterion_mse = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for b_X, b_conv, b_fg, b_epa in loader:
            optimizer.zero_grad()
            p_conv, p_fg, p_epa = model(b_X)
            
            loss = (criterion_bce(p_conv, b_conv) + 
                    criterion_bce(p_fg, b_fg) + 
                    criterion_mse(p_epa, b_epa))
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {total_loss/len(loader):.4f}")
            
    save_model(model, MODEL_DIR / "fourth_down_model.pt")
    return model

def run_training():
    loader = NFLDataLoader()
    engineer = NFLFeatureEngineer()
    
    print("📥 Loading Data...")
    data = loader.load_all_intelligence_data()
    clean_pbp = engineer.clean_pbp(data['pbp'])
    
    # 1. Win Probability
    X_wp, y_wp = engineer.get_win_prob_features(clean_pbp)
    X_wp_scaled = engineer.scale_features(X_wp.values, "win_prob")
    train_win_prob(X_wp_scaled, y_wp.values)
    
    # 2. 4th Down
    X_fd, y_fd = engineer.get_fourth_down_features(clean_pbp)
    X_fd_scaled = engineer.scale_features(X_fd.values, "fourth_down")
    train_fourth_down(X_fd_scaled, y_fd)
    
    # Save artifacts
    engineer.save_artifacts()
    print("\n✅ Training Complete. All models and scalers saved.")

if __name__ == "__main__":
    run_training()
