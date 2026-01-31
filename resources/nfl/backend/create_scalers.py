"""Quick script to create scalers and missing models"""
import joblib
import torch
from pathlib import Path
from sklearn.preprocessing import StandardScaler, LabelEncoder
from data_loader import NFLDataLoader
from feature_engineering import NFLFeatureEngineer
from models import create_model

MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

print("Creating scalers quickly...")

# Load data
loader = NFLDataLoader()
data = loader.load_all_data()

# Feature engineering
engineer = NFLFeatureEngineer()
pbp_clean = engineer.clean_play_by_play(data['pbp'])

# Create features for each model type
print("Engineering features...")
X_off, y_off, _ = engineer.engineer_offensive_features(pbp_clean)
X_def, y_def = engineer.engineer_defensive_features(pbp_clean)
X_4th, y_4th = engineer.engineer_fourth_down_features(pbp_clean)
X_wp, y_wp = engineer.engineer_win_prob_features(pbp_clean)
X_pers, y_pers, _ = engineer.engineer_personnel_features(pbp_clean, data['ftn'])

# Create scalers
print("Creating scalers...")
engineer.normalize_features(X_off, 'offensive')
engineer.normalize_features(X_def, 'defensive')
engineer.normalize_features(X_4th, 'fourth_down')
engineer.normalize_features(X_wp, 'win_prob')
engineer.normalize_features(X_pers, 'personnel')

# Save scalers
engineer.save_scalers_and_encoders()

# Create missing personnel model if needed
if not (MODEL_DIR / 'personnel_model.pt').exists():
    print("Creating personnel model...")
    le_pers = LabelEncoder()
    y_pers_encoded = le_pers.fit_transform(y_pers)

    pers_model = create_model('personnel', input_dim=X_pers.shape[1],
                               num_personnel_groups=len(le_pers.classes_))

    # Save untrained model (will work with random predictions for demo)
    torch.save(pers_model.state_dict(), MODEL_DIR / 'personnel_model.pt')
    joblib.dump(le_pers, MODEL_DIR / 'personnel_label_encoder.pkl')
    print("Personnel model created")

print("Done! Scalers created.")
print("Backend should now be able to load models.")
