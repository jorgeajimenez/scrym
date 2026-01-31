"""
Historical Validation Script
Tests model predictions against real NFL game outcomes

This loads real play-by-play data and compares model predictions
to what actually happened in historical games
"""

import torch
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from models import create_model
from data_loader import NFLDataLoader
from feature_engineering import NFLFeatureEngineer

# Paths
MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"
device = torch.device('cpu')


def load_models():
    """Load all models and scalers"""
    models = {}
    scalers = joblib.load(DATA_DIR / "scalers.pkl")

    # Load offensive model
    le_off = joblib.load(MODEL_DIR / 'offensive_label_encoder.pkl')
    X_shape = scalers['offensive'].mean_.shape[0]
    off_model = create_model('offensive', input_dim=X_shape, num_classes=len(le_off.classes_))
    off_model.load_state_dict(torch.load(MODEL_DIR / 'offensive_model.pt', map_location=device, weights_only=True))
    off_model.eval()
    models['offensive'] = (off_model, le_off, scalers['offensive'])

    # Load defensive model
    X_shape = scalers['defensive'].mean_.shape[0]
    def_model = create_model('defensive', input_dim=X_shape)
    def_model.load_state_dict(torch.load(MODEL_DIR / 'defensive_model.pt', map_location=device, weights_only=True))
    def_model.eval()
    models['defensive'] = (def_model, scalers['defensive'])

    # Load win prob model
    X_shape = scalers['win_prob'].mean_.shape[0]
    wp_model = create_model('win_prob', input_dim=X_shape)
    wp_model.load_state_dict(torch.load(MODEL_DIR / 'win_prob_model.pt', map_location=device, weights_only=True))
    wp_model.eval()
    models['win_prob'] = (wp_model, scalers['win_prob'])

    return models


def validate_offensive_model(pbp_sample, model, label_encoder, scaler):
    """Validate offensive play predictions"""
    print("\n" + "=" * 80)
    print("OFFENSIVE MODEL VALIDATION (Random Sample of 10 Plays)")
    print("=" * 80)

    correct = 0
    total = 0

    for idx, row in pbp_sample.iterrows():
        # Prepare features (same as training)
        features = np.array([[
            row['down'],
            row['ydstogo'],
            row['yardline_100'],
            row['score_differential'],
            row['qtr'],
            row['game_seconds_remaining'],
            row['half_seconds_remaining'],
            row['red_zone'],
            row['goal_to_go'],
            row['two_min_drill'],
            row['posteam_timeouts_remaining'],
            0  # team_encoded placeholder
        ]])

        features_scaled = scaler.transform(features)

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            probs = model.predict_proba(features_tensor).numpy()[0]

        predicted_play = label_encoder.classes_[np.argmax(probs)]
        actual_play = row['play_category']

        is_correct = predicted_play == actual_play
        if is_correct:
            correct += 1
        total += 1

        # Show each prediction
        status = "✓" if is_correct else "✗"
        print(f"\n{status} Play {total}:")
        print(f"   Situation: {int(row['down'])} & {int(row['ydstogo'])} at yard line {int(row['yardline_100'])}")
        print(f"   Q{int(row['qtr'])}, Score diff: {int(row['score_differential'])}")
        print(f"   Predicted: {predicted_play.upper()} ({probs.max():.1%} confidence)")
        print(f"   Actual: {actual_play.upper()}")

        # Show all probabilities
        for play_type, prob in zip(label_encoder.classes_, probs):
            bar = "█" * int(prob * 20)
            print(f"      {play_type:12} {prob:5.1%} {bar}")

    accuracy = correct / total if total > 0 else 0
    print(f"\n{'=' * 80}")
    print(f"Accuracy: {correct}/{total} = {accuracy:.1%}")
    print(f"{'=' * 80}")

    return accuracy


def validate_defensive_model(pbp_sample, model, scaler):
    """Validate defensive play type predictions"""
    print("\n" + "=" * 80)
    print("DEFENSIVE MODEL VALIDATION (Random Sample of 10 Plays)")
    print("=" * 80)

    correct = 0
    total = 0

    for idx, row in pbp_sample.iterrows():
        features = np.array([[
            row['down'],
            row['ydstogo'],
            row['yardline_100'],
            row['score_differential'],
            row['qtr'],
            row['game_seconds_remaining'],
            row.get('team_pass_rate', 0.58),
            row.get('team_avg_epa', 0.0),
            row['red_zone'],
            row['goal_to_go'],
            row['two_min_drill']
        ]])

        features_scaled = scaler.transform(features)

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            pass_prob = float(model.predict_proba(features_tensor).numpy()[0][0])

        predicted = "pass" if pass_prob > 0.5 else "run"
        actual = row['play_type']

        is_correct = predicted == actual
        if is_correct:
            correct += 1
        total += 1

        status = "✓" if is_correct else "✗"
        print(f"\n{status} Play {total}:")
        print(f"   Situation: {int(row['down'])} & {int(row['ydstogo'])}")
        print(f"   Predicted: {predicted.upper()} ({max(pass_prob, 1-pass_prob):.1%} confidence)")
        print(f"   Actual: {actual.upper()}")
        print(f"   Pass probability: {pass_prob:.1%}")

    accuracy = correct / total if total > 0 else 0
    print(f"\n{'=' * 80}")
    print(f"Accuracy: {correct}/{total} = {accuracy:.1%}")
    print(f"{'=' * 80}")

    return accuracy


def validate_win_probability(pbp_sample, model, scaler):
    """Validate win probability predictions"""
    print("\n" + "=" * 80)
    print("WIN PROBABILITY MODEL VALIDATION (Random Sample of 10 Plays)")
    print("=" * 80)

    errors = []

    for idx, row in pbp_sample.iterrows():
        features = np.array([[
            row['score_differential'],
            row['qtr'],
            row['game_seconds_remaining'],
            row['yardline_100'],
            row['down'],
            row['ydstogo'],
            row['posteam_timeouts_remaining'],
            row.get('defteam_timeouts_remaining', 3)
        ]])

        features_scaled = scaler.transform(features)

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            predicted_prob = float(model.predict_proba(features_tensor).numpy()[0][0])

        actual_outcome = row['posteam_won']
        error = abs(predicted_prob - actual_outcome)
        errors.append(error)

        print(f"\nPlay {len(errors)}:")
        print(f"   Situation: Q{int(row['qtr'])}, {int(row['game_seconds_remaining'])}s remaining")
        print(f"   Score diff: {int(row['score_differential'])}")
        print(f"   Predicted win prob: {predicted_prob:.1%}")
        print(f"   Actual outcome: {'WON' if actual_outcome == 1 else 'LOST'}")
        print(f"   Calibration error: {error:.1%}")

    mean_error = np.mean(errors)
    print(f"\n{'=' * 80}")
    print(f"Mean Absolute Error: {mean_error:.1%}")
    print(f"{'=' * 80}")

    return mean_error


def main():
    """Run historical validation"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 18 + "HISTORICAL VALIDATION REPORT" + " " * 31 + "║")
    print("║" + " " * 10 + "Testing Models Against Real NFL Game Outcomes" + " " * 22 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")

    print("Loading historical play-by-play data...")
    loader = NFLDataLoader()
    data = loader.load_all_data()

    print("Preparing features...")
    engineer = NFLFeatureEngineer()
    pbp_clean = engineer.clean_play_by_play(data['pbp'])

    print("Loading trained models...")
    models = load_models()

    # Prepare data for each model
    print("\n" + "=" * 80)
    print("PREPARING TEST SAMPLES")
    print("=" * 80)

    # Offensive model data
    X_off, y_off, _ = engineer.engineer_offensive_features(pbp_clean)
    plays_with_features = pbp_clean[pbp_clean['play_type'].isin(['run', 'pass'])].copy()

    def categorize_play(row):
        if row['play_type'] == 'run':
            return 'run'
        elif row['play_type'] == 'pass':
            desc = str(row.get('desc', '')).lower()
            if 'screen' in desc:
                return 'screen'
            elif 'draw' in desc:
                return 'draw'
            elif 'play-action' in desc or 'play action' in desc:
                return 'play_action'
            else:
                return 'pass'
        return 'pass'

    plays_with_features['play_category'] = plays_with_features.apply(categorize_play, axis=1)

    # Sample 10 random plays
    sample_size = 10
    off_sample = plays_with_features.dropna(subset=[
        'down', 'ydstogo', 'yardline_100', 'score_differential', 'qtr',
        'game_seconds_remaining', 'half_seconds_remaining', 'red_zone',
        'goal_to_go', 'two_min_drill', 'posteam_timeouts_remaining'
    ]).sample(n=sample_size, random_state=42)

    print(f"✓ Sampled {len(off_sample)} plays for offensive model validation")

    # Defensive model data
    X_def, y_def = engineer.engineer_defensive_features(pbp_clean)
    def_plays = pbp_clean[pbp_clean['play_type'].isin(['run', 'pass'])].copy()

    # Calculate team tendencies
    team_tendencies = def_plays.groupby('posteam').agg({
        'play_type': lambda x: (x == 'pass').mean(),
        'epa': 'mean'
    }).rename(columns={'play_type': 'team_pass_rate', 'epa': 'team_avg_epa'})

    def_plays = def_plays.merge(team_tendencies, left_on='posteam', right_index=True, how='left')

    def_sample = def_plays.dropna(subset=[
        'down', 'ydstogo', 'yardline_100', 'score_differential', 'qtr',
        'game_seconds_remaining', 'red_zone', 'goal_to_go', 'two_min_drill'
    ]).sample(n=sample_size, random_state=42)

    print(f"✓ Sampled {len(def_sample)} plays for defensive model validation")

    # Win probability model data
    X_wp, y_wp = engineer.engineer_win_prob_features(pbp_clean)
    wp_plays = pbp_clean.copy()

    # Get game outcomes
    game_outcomes = wp_plays.groupby(['game_id', 'home_team', 'away_team']).agg({
        'total_home_score': 'last',
        'total_away_score': 'last'
    }).reset_index()

    game_outcomes['home_won'] = (game_outcomes['total_home_score'] >
                                   game_outcomes['total_away_score']).astype(int)

    wp_plays = wp_plays.merge(game_outcomes[['game_id', 'home_won']], on='game_id', how='left')
    wp_plays['posteam_won'] = wp_plays.apply(
        lambda row: row['home_won'] if row['posteam'] == row['home_team'] else 1 - row['home_won'],
        axis=1
    )

    wp_sample = wp_plays.dropna(subset=[
        'score_differential', 'qtr', 'game_seconds_remaining', 'yardline_100',
        'down', 'ydstogo', 'posteam_timeouts_remaining', 'posteam_won'
    ]).sample(n=sample_size, random_state=42)

    print(f"✓ Sampled {len(wp_sample)} plays for win probability validation")

    # Run validations
    off_model, le_off, off_scaler = models['offensive']
    off_accuracy = validate_offensive_model(off_sample, off_model, le_off, off_scaler)

    def_model, def_scaler = models['defensive']
    def_accuracy = validate_defensive_model(def_sample, def_model, def_scaler)

    wp_model, wp_scaler = models['win_prob']
    wp_mae = validate_win_probability(wp_sample, wp_model, wp_scaler)

    # Final summary
    print("\n\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "FINAL SUMMARY" + " " * 37 + "║")
    print("╚" + "═" * 78 + "╝")
    print(f"\n  Offensive Model Accuracy:      {off_accuracy:.1%}")
    print(f"  Defensive Model Accuracy:      {def_accuracy:.1%}")
    print(f"  Win Prob Mean Absolute Error:  {wp_mae:.1%}")
    print("\nNote: These are tested on a random sample of historical plays.")
    print("For full validation, run this multiple times or increase sample size.\n")


if __name__ == "__main__":
    main()
