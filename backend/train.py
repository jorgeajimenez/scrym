"""
Optimized Training Pipeline for ALL Models
Includes 4th Down, Win Prob, Offensive, Defensive, and Personnel.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import joblib

from data_loader import NFLDataLoader
from feature_engineering import NFLFeatureEngineer
from models import (
    FourthDownDecisionModel, WinProbabilityModel, 
    OffensivePlayCallerModel, DefensiveCoordinatorModel, PersonnelOptimizerModel,
    save_model
)

# Constants
MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR = Path(__file__).parent.parent / "data"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 512
EPOCHS = 40 # Slightly reduced for speed across 5 models
LEARNING_RATE = 0.001

def train_generic_model(model, train_loader, val_loader, criterion, optimizer, scheduler, model_name):
    print(f"\n--- Training {model_name} ---")
    
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            # Ensure correct shape for BCE (flatten outputs) vs CrossEntropy (logits)
            if isinstance(criterion, nn.BCELoss):
                loss = criterion(outputs, batch_y)
            else:
                loss = criterion(outputs, batch_y.long().squeeze()) # CrossEntropy expects LongTensor
                
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for v_X, v_y in val_loader:
                v_out = model(v_X)
                if isinstance(criterion, nn.BCELoss):
                    val_loss += criterion(v_out, v_y).item()
                else:
                    val_loss += criterion(v_out, v_y.long().squeeze()).item()
        
        avg_val_loss = val_loss/len(val_loader)
        scheduler.step(avg_val_loss)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {avg_val_loss:.4f} | LR: {optimizer.param_groups[0]['lr']}")
            
    save_model(model, MODEL_DIR / f"{model_name}.pt")
    return model

def train_fourth_down(X, y_data):
    print("\n--- Training 4th Down Decision Model (Weighted) ---")
    X_tensor = torch.FloatTensor(X).to(DEVICE)
    epa_clipped = np.clip(y_data['epa'].values, -5, 5)
    
    y_conv = torch.FloatTensor(y_data['converted'].values).view(-1, 1).to(DEVICE)
    y_fg = torch.FloatTensor(y_data['fg_made'].values).view(-1, 1).to(DEVICE)
    y_epa = torch.FloatTensor(epa_clipped).view(-1, 1).to(DEVICE)
    
    dataset = TensorDataset(X_tensor, y_conv, y_fg, y_epa)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)
    
    model = FourthDownDecisionModel(X.shape[1]).to(DEVICE)
    criterion_bce = nn.BCELoss()
    criterion_mse = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.5)
    
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0
        for b_X, b_conv, b_fg, b_epa in train_loader:
            optimizer.zero_grad()
            p_conv, p_fg, p_epa = model(b_X)
            loss = (5.0 * criterion_bce(p_conv, b_conv) + 
                    5.0 * criterion_bce(p_fg, b_fg) + 
                    1.0 * criterion_mse(p_epa, b_epa))
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for v_X, v_conv, v_fg, v_epa in val_loader:
                vp_conv, vp_fg, vp_epa = model(v_X)
                v_loss = (5.0 * criterion_bce(vp_conv, v_conv) + 
                          5.0 * criterion_bce(vp_fg, v_fg) + 
                          1.0 * criterion_mse(vp_epa, v_epa))
                val_loss += v_loss.item()
        
        avg_val_loss = val_loss/len(val_loader)
        scheduler.step(avg_val_loss)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {avg_val_loss:.4f} | LR: {optimizer.param_groups[0]['lr']}")
            
    save_model(model, MODEL_DIR / "fourth_down_model.pt")

def prepare_loaders(X, y, batch_size=BATCH_SIZE):
    X_tensor = torch.FloatTensor(X).to(DEVICE)
    y_tensor = torch.FloatTensor(y).view(-1, 1).to(DEVICE)
    dataset = TensorDataset(X_tensor, y_tensor)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])
    return DataLoader(train_ds, batch_size=batch_size, shuffle=True), DataLoader(val_ds, batch_size=batch_size)

def run_training():
    loader = NFLDataLoader()
    engineer = NFLFeatureEngineer()
    encoders = {}
    
    print("📥 Loading Data...")
    data = loader.load_all_intelligence_data()
    clean_pbp = engineer.clean_pbp(data['pbp'])
    
    # --- 1. Win Probability ---
    X_wp, y_wp = engineer.get_win_prob_features(clean_pbp)
    X_wp_s = engineer.scale_features(X_wp.values, "win_prob")
    tl, vl = prepare_loaders(X_wp_s, y_wp.values)
    
    model_wp = WinProbabilityModel(X_wp.shape[1]).to(DEVICE)
    opt_wp = optim.Adam(model_wp.parameters(), lr=LEARNING_RATE)
    sch_wp = optim.lr_scheduler.ReduceLROnPlateau(opt_wp, 'min', patience=5, factor=0.5)
    train_generic_model(model_wp, tl, vl, nn.BCELoss(), opt_wp, sch_wp, "win_prob_model")
    
    # --- 2. 4th Down ---
    X_fd, y_fd = engineer.get_fourth_down_features(clean_pbp)
    X_fd_s = engineer.scale_features(X_fd.values, "fourth_down")
    train_fourth_down(X_fd_s, y_fd)
    
    # --- 3. Offensive Play Caller (Multi-Class) ---
    X_off, y_off_raw = engineer.get_offensive_features(clean_pbp)
    X_off_s = engineer.scale_features(X_off.values, "offensive")
    
    le_off = LabelEncoder()
    y_off = le_off.fit_transform(y_off_raw)
    encoders['offensive'] = le_off
    
    tl, vl = prepare_loaders(X_off_s, y_off)
    model_off = OffensivePlayCallerModel(X_off.shape[1], num_classes=len(le_off.classes_)).to(DEVICE)
    opt_off = optim.Adam(model_off.parameters(), lr=LEARNING_RATE)
    sch_off = optim.lr_scheduler.ReduceLROnPlateau(opt_off, 'min', patience=5, factor=0.5)
    train_generic_model(model_off, tl, vl, nn.CrossEntropyLoss(), opt_off, sch_off, "offensive_model")
    
    # --- 4. Defensive Coordinator (Binary) ---
    X_def, y_def = engineer.get_defensive_features(clean_pbp)
    X_def_s = engineer.scale_features(X_def.values, "defensive")
    tl, vl = prepare_loaders(X_def_s, y_def.values)
    
    model_def = DefensiveCoordinatorModel(X_def.shape[1]).to(DEVICE)
    opt_def = optim.Adam(model_def.parameters(), lr=LEARNING_RATE)
    sch_def = optim.lr_scheduler.ReduceLROnPlateau(opt_def, 'min', patience=5, factor=0.5)
    train_generic_model(model_def, tl, vl, nn.BCELoss(), opt_def, sch_def, "defensive_model")
    
    # --- 5. Personnel Optimizer (Multi-Class) ---
    X_pers, y_pers_raw = engineer.get_personnel_features(clean_pbp, data['ftn'])
    X_pers_s = engineer.scale_features(X_pers.values, "personnel")
    
    le_pers = LabelEncoder()
    y_pers = le_pers.fit_transform(y_pers_raw)
    encoders['personnel'] = le_pers
    
    tl, vl = prepare_loaders(X_pers_s, y_pers)
    model_pers = PersonnelOptimizerModel(X_pers.shape[1], num_classes=len(le_pers.classes_)).to(DEVICE)
    opt_pers = optim.Adam(model_pers.parameters(), lr=LEARNING_RATE)
    sch_pers = optim.lr_scheduler.ReduceLROnPlateau(opt_pers, 'min', patience=5, factor=0.5)
    train_generic_model(model_pers, tl, vl, nn.CrossEntropyLoss(), opt_pers, sch_pers, "personnel_model")
    
    # Save all artifacts
    engineer.save_artifacts()
    joblib.dump(encoders, DATA_DIR / "encoders.pkl")
    print(f"\n✅ All 5 models trained. Encoders saved to {DATA_DIR}/encoders.pkl")

if __name__ == "__main__":
    run_training()
