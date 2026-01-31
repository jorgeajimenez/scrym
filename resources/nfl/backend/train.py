"""
Training Script for All 5 NFL AI Coach Models
Trains PyTorch models and saves them for inference
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from pathlib import Path

from data_loader import NFLDataLoader
from feature_engineering import NFLFeatureEngineer
from models import create_model

# Paths
MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")


class ModelTrainer:
    """Handles training for all 5 models"""

    def __init__(self, batch_size=512, epochs=50, learning_rate=0.001):
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.device = device

    def train_classification_model(self, model, X_train, y_train, X_val, y_val, model_name):
        """
        Train a classification model

        Args:
            model: PyTorch model
            X_train, y_train: Training data
            X_val, y_val: Validation data
            model_name: Name for saving the model

        Returns:
            Trained model
        """
        print(f"\nTraining {model_name}...")

        # Convert to tensors
        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        y_train_tensor = torch.LongTensor(y_train).to(self.device)
        X_val_tensor = torch.FloatTensor(X_val).to(self.device)
        y_val_tensor = torch.LongTensor(y_val).to(self.device)

        # Create data loaders
        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)

        model = model.to(self.device)
        best_val_loss = float('inf')
        patience_counter = 0

        # Training loop
        for epoch in range(self.epochs):
            model.train()
            train_loss = 0.0

            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()

            train_loss /= len(train_loader)

            # Validation
            model.eval()
            with torch.no_grad():
                val_outputs = model(X_val_tensor)
                val_loss = criterion(val_outputs, y_val_tensor).item()

                _, predicted = torch.max(val_outputs, 1)
                accuracy = (predicted == y_val_tensor).float().mean().item()

            scheduler.step(val_loss)

            if (epoch + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{self.epochs}], Train Loss: {train_loss:.4f}, "
                      f"Val Loss: {val_loss:.4f}, Val Acc: {accuracy:.4f}")

            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                # Save best model
                torch.save(model.state_dict(), MODEL_DIR / f"{model_name}.pt")
            else:
                patience_counter += 1
                if patience_counter >= 10:
                    print(f"Early stopping at epoch {epoch+1}")
                    break

        print(f"Best validation loss: {best_val_loss:.4f}")
        return model

    def train_binary_model(self, model, X_train, y_train, X_val, y_val, model_name):
        """Train a binary classification model"""
        print(f"\nTraining {model_name}...")

        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        y_train_tensor = torch.FloatTensor(y_train).unsqueeze(1).to(self.device)
        X_val_tensor = torch.FloatTensor(X_val).to(self.device)
        y_val_tensor = torch.FloatTensor(y_val).unsqueeze(1).to(self.device)

        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)

        criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)

        model = model.to(self.device)
        best_val_loss = float('inf')
        patience_counter = 0

        for epoch in range(self.epochs):
            model.train()
            train_loss = 0.0

            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()

            train_loss /= len(train_loader)

            # Validation
            model.eval()
            with torch.no_grad():
                val_outputs = model(X_val_tensor)
                val_loss = criterion(val_outputs, y_val_tensor).item()

                predicted = (torch.sigmoid(val_outputs) > 0.5).float()
                accuracy = (predicted == y_val_tensor).float().mean().item()

            scheduler.step(val_loss)

            if (epoch + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{self.epochs}], Train Loss: {train_loss:.4f}, "
                      f"Val Loss: {val_loss:.4f}, Val Acc: {accuracy:.4f}")

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                torch.save(model.state_dict(), MODEL_DIR / f"{model_name}.pt")
            else:
                patience_counter += 1
                if patience_counter >= 10:
                    print(f"Early stopping at epoch {epoch+1}")
                    break

        print(f"Best validation loss: {best_val_loss:.4f}")
        return model

    def train_regression_model(self, model, X_train, y_train, X_val, y_val, model_name):
        """Train a regression model (for 4th down multi-output)"""
        print(f"\nTraining {model_name}...")

        X_train_tensor = torch.FloatTensor(X_train).to(self.device)
        X_val_tensor = torch.FloatTensor(X_val).to(self.device)

        # For 4th down model, we have multiple targets
        # y_train should be a dict with 'converted', 'fg_made', 'epa'
        y_conv_train = torch.FloatTensor(y_train['converted'].values).unsqueeze(1).to(self.device)
        y_fg_train = torch.FloatTensor(y_train['fg_made'].values).unsqueeze(1).to(self.device)
        y_epa_train = torch.FloatTensor(y_train['epa'].values).unsqueeze(1).to(self.device)

        y_conv_val = torch.FloatTensor(y_val['converted'].values).unsqueeze(1).to(self.device)
        y_fg_val = torch.FloatTensor(y_val['fg_made'].values).unsqueeze(1).to(self.device)
        y_epa_val = torch.FloatTensor(y_val['epa'].values).unsqueeze(1).to(self.device)

        train_dataset = TensorDataset(X_train_tensor, y_conv_train, y_fg_train, y_epa_train)
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)

        criterion_bce = nn.BCELoss()
        criterion_mse = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)

        model = model.to(self.device)
        best_val_loss = float('inf')
        patience_counter = 0

        for epoch in range(self.epochs):
            model.train()
            train_loss = 0.0

            for batch_X, batch_conv, batch_fg, batch_epa in train_loader:
                optimizer.zero_grad()
                conv_pred, fg_pred, epa_pred = model(batch_X)

                loss_conv = criterion_bce(conv_pred, batch_conv)
                loss_fg = criterion_bce(fg_pred, batch_fg)
                loss_epa = criterion_mse(epa_pred, batch_epa)

                loss = loss_conv + loss_fg + 0.5 * loss_epa  # Weighted combination
                loss.backward()
                optimizer.step()
                train_loss += loss.item()

            train_loss /= len(train_loader)

            # Validation
            model.eval()
            with torch.no_grad():
                conv_pred, fg_pred, epa_pred = model(X_val_tensor)

                val_loss_conv = criterion_bce(conv_pred, y_conv_val).item()
                val_loss_fg = criterion_bce(fg_pred, y_fg_val).item()
                val_loss_epa = criterion_mse(epa_pred, y_epa_val).item()

                val_loss = val_loss_conv + val_loss_fg + 0.5 * val_loss_epa

            scheduler.step(val_loss)

            if (epoch + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{self.epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                torch.save(model.state_dict(), MODEL_DIR / f"{model_name}.pt")
            else:
                patience_counter += 1
                if patience_counter >= 10:
                    print(f"Early stopping at epoch {epoch+1}")
                    break

        print(f"Best validation loss: {best_val_loss:.4f}")
        return model


def main():
    """Main training pipeline"""
    print("=" * 60)
    print("NFL AI COACH - MODEL TRAINING PIPELINE")
    print("=" * 60)

    # Load data
    loader = NFLDataLoader()
    data = loader.load_all_data(force_reload=False)

    # Feature engineering
    engineer = NFLFeatureEngineer()
    pbp_clean = engineer.clean_play_by_play(data['pbp'])

    trainer = ModelTrainer(batch_size=512, epochs=50, learning_rate=0.001)

    # ==================== Model 1: Offensive Play-Caller ====================
    print("\n" + "=" * 60)
    print("MODEL 1: OFFENSIVE PLAY-CALLER")
    print("=" * 60)

    X_off, y_off, _ = engineer.engineer_offensive_features(pbp_clean)
    X_off_norm = engineer.normalize_features(X_off, 'offensive')

    # Encode labels
    le_off = LabelEncoder()
    y_off_encoded = le_off.fit_transform(y_off)

    X_train, X_val, y_train, y_val = train_test_split(
        X_off_norm, y_off_encoded, test_size=0.2, random_state=42, stratify=y_off_encoded
    )

    off_model = create_model('offensive', input_dim=X_off_norm.shape[1],
                              num_classes=len(le_off.classes_))
    off_model = trainer.train_classification_model(off_model, X_train, y_train, X_val, y_val,
                                                     'offensive_model')

    # Save label encoder
    import joblib
    joblib.dump(le_off, MODEL_DIR / 'offensive_label_encoder.pkl')

    # ==================== Model 2: Defensive Coordinator ====================
    print("\n" + "=" * 60)
    print("MODEL 2: DEFENSIVE COORDINATOR")
    print("=" * 60)

    X_def, y_def = engineer.engineer_defensive_features(pbp_clean)
    X_def_norm = engineer.normalize_features(X_def, 'defensive')

    X_train, X_val, y_train, y_val = train_test_split(
        X_def_norm, y_def.values, test_size=0.2, random_state=42
    )

    def_model = create_model('defensive', input_dim=X_def_norm.shape[1])
    def_model = trainer.train_binary_model(def_model, X_train, y_train, X_val, y_val,
                                             'defensive_model')

    # ==================== Model 3: 4th Down Decision ====================
    print("\n" + "=" * 60)
    print("MODEL 3: 4TH DOWN DECISION ENGINE")
    print("=" * 60)

    X_4th, y_4th = engineer.engineer_fourth_down_features(pbp_clean)
    X_4th_norm = engineer.normalize_features(X_4th, 'fourth_down')

    X_train, X_val, y_train_idx, y_val_idx = train_test_split(
        X_4th_norm, np.arange(len(y_4th)), test_size=0.2, random_state=42
    )
    y_train = y_4th.iloc[y_train_idx]
    y_val = y_4th.iloc[y_val_idx]

    fourth_model = create_model('fourth_down', input_dim=X_4th_norm.shape[1])
    fourth_model = trainer.train_regression_model(fourth_model, X_train, y_train, X_val, y_val,
                                                    'fourth_down_model')

    # ==================== Model 4: Win Probability ====================
    print("\n" + "=" * 60)
    print("MODEL 4: WIN PROBABILITY CALCULATOR")
    print("=" * 60)

    X_wp, y_wp = engineer.engineer_win_prob_features(pbp_clean)
    X_wp_norm = engineer.normalize_features(X_wp, 'win_prob')

    X_train, X_val, y_train, y_val = train_test_split(
        X_wp_norm, y_wp.values, test_size=0.2, random_state=42
    )

    wp_model = create_model('win_prob', input_dim=X_wp_norm.shape[1])
    wp_model = trainer.train_binary_model(wp_model, X_train, y_train, X_val, y_val,
                                            'win_prob_model')

    # ==================== Model 5: Personnel Optimizer ====================
    print("\n" + "=" * 60)
    print("MODEL 5: PERSONNEL GROUPING OPTIMIZER")
    print("=" * 60)

    X_pers, y_pers, _ = engineer.engineer_personnel_features(pbp_clean, data['ftn'])
    X_pers_norm = engineer.normalize_features(X_pers, 'personnel')

    # Encode personnel labels
    le_pers = LabelEncoder()
    y_pers_encoded = le_pers.fit_transform(y_pers)

    X_train, X_val, y_train, y_val = train_test_split(
        X_pers_norm, y_pers_encoded, test_size=0.2, random_state=42, stratify=y_pers_encoded
    )

    pers_model = create_model('personnel', input_dim=X_pers_norm.shape[1],
                               num_personnel_groups=len(le_pers.classes_))
    pers_model = trainer.train_classification_model(pers_model, X_train, y_train, X_val, y_val,
                                                      'personnel_model')

    joblib.dump(le_pers, MODEL_DIR / 'personnel_label_encoder.pkl')

    # Save scalers and encoders
    engineer.save_scalers_and_encoders()

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print(f"All models saved to: {MODEL_DIR}")
    print(f"Scalers and encoders saved to: {DATA_DIR}")


if __name__ == "__main__":
    main()
