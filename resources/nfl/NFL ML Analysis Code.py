import nfl_data_py as nfl
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib # For saving the model for production use

def build_nfl_model():
    """
    Pipeline to train a baseline Play-Type Prediction model.
    """
    print("Fetching data from nflverse...")
    # Load recent data
    data = nfl.import_pbp_data([2023, 2024])
    
    # Preprocessing
    # Filter only for runs and passes, excluding penalties, spikes, kneels
    pbp = data[(data['play_type'] == 'run') | (data['play_type'] == 'pass')].copy()
    
    # Define Target
    pbp['label'] = (pbp['play_type'] == 'pass').astype(int) # 1 if Pass, 0 if Run
    
    # Define Features
    # 'yardline_100' is distance to opponent goal
    features = [
        'down', 
        'ydstogo', 
        'yardline_100', 
        'score_differential', 
        'qtr', 
        'half_seconds_remaining'
    ]
    
    # Clean nulls
    df_clean = pbp[features + ['label']].dropna()
    
    X = df_clean[features]
    y = df_clean['label']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Training
    print("Training XGBoost Classifier...")
    clf = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    clf.fit(X_train, y_train)
    
    accuracy = clf.score(X_test, y_test)
    print(f"Model Training Complete. Accuracy: {accuracy:.2%}")
    
    return clf

if __name__ == "__main__":
    trained_model = build_nfl_model()
    
    # Example Inference:
    # 2nd and 5, at midfield (50yd), tie game, 2nd quarter, 2 mins left in half
    sample_play = pd.DataFrame([[2, 5, 50, 0, 2, 120]], 
                               columns=['down', 'ydstogo', 'yardline_100', 'score_differential', 'qtr', 'half_seconds_remaining'])
    
    prob = trained_model.predict_proba(sample_play)[0][1]
    print(f"Calculated Pass Probability for Sample Play: {prob:.1%}")