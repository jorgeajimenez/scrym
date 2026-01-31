"""
Feature Engineering Pipeline for NFL AI Coach
Prepares features for all 5 ML models
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pathlib import Path
import joblib

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


class NFLFeatureEngineer:
    """Feature engineering for all 5 models"""

    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.team_stats = {}

    def clean_play_by_play(self, pbp):
        """
        Clean and filter play-by-play data

        Args:
            pbp: Raw play-by-play DataFrame

        Returns:
            Cleaned DataFrame
        """
        print("Cleaning play-by-play data...")

        # Filter for regular season and playoffs only
        pbp = pbp[pbp['season_type'].isin(['REG', 'POST'])].copy()

        # Remove garbage time (score differential > 17 in Q4)
        pbp = pbp[~((pbp['qtr'] == 4) & (abs(pbp['score_differential']) > 17))].copy()

        # Add derived features
        pbp['red_zone'] = (pbp['yardline_100'] <= 20).astype(int)
        pbp['goal_to_go'] = (pbp['yardline_100'] <= 10).astype(int)
        pbp['two_min_drill'] = ((pbp['game_seconds_remaining'] <= 120) &
                                 (pbp['qtr'].isin([2, 4]))).astype(int)

        print(f"Cleaned data: {len(pbp)} plays")
        return pbp

    def engineer_offensive_features(self, pbp):
        """
        Engineer features for offensive play-calling model

        Features:
        - Situational: down, distance, field position, score, time
        - Historical: team tendencies
        - Success metrics: EPA-based features

        Returns:
            DataFrame with features and target
        """
        print("Engineering offensive play-calling features...")

        # Filter for run/pass plays only
        plays = pbp[(pbp['play_type'].isin(['run', 'pass']))].copy()

        # Define play categories (5 classes)
        def categorize_play(row):
            if row['play_type'] == 'run':
                if row.get('rush_attempt', 0) == 1:
                    return 'run'
            elif row['play_type'] == 'pass':
                # Check for play-action, screen, etc. from play description
                desc = str(row.get('desc', '')).lower()
                if 'screen' in desc:
                    return 'screen'
                elif 'draw' in desc:
                    return 'draw'
                elif 'play-action' in desc or 'play action' in desc:
                    return 'play_action'
                else:
                    return 'pass'
            return 'pass'  # Default

        plays['play_category'] = plays.apply(categorize_play, axis=1)

        # Base situational features
        features = [
            'down', 'ydstogo', 'yardline_100',
            'score_differential', 'qtr', 'game_seconds_remaining',
            'half_seconds_remaining', 'red_zone', 'goal_to_go',
            'two_min_drill', 'posteam_timeouts_remaining'
        ]

        # Add team encoding (categorical to numeric)
        if 'posteam' in plays.columns:
            le = LabelEncoder()
            plays['team_encoded'] = le.fit_transform(plays['posteam'].fillna('UNKNOWN'))
            features.append('team_encoded')
            self.encoders['team'] = le

        # Clean nulls
        df = plays[features + ['play_category', 'epa']].copy()
        df = df.dropna(subset=features)

        # Train on ALL plays (removed EPA > 0 filter to include failed plays)
        print(f"Offensive features: {len(df)} total plays")
        print(f"Play categories: {df['play_category'].value_counts().to_dict()}")

        return df[features], df['play_category'], df['epa']

    def engineer_defensive_features(self, pbp):
        """
        Engineer features for defensive coordinator model
        Predicts opponent's next play

        Returns:
            DataFrame with features and target (opponent play type)
        """
        print("Engineering defensive coordinator features...")

        # Filter for run/pass plays
        plays = pbp[(pbp['play_type'].isin(['run', 'pass']))].copy()

        # Calculate team offensive tendencies
        team_tendencies = plays.groupby('posteam').agg({
            'play_type': lambda x: (x == 'pass').mean(),  # Pass rate
            'epa': 'mean'
        }).rename(columns={'play_type': 'team_pass_rate', 'epa': 'team_avg_epa'})

        plays = plays.merge(team_tendencies, left_on='posteam', right_index=True, how='left')

        # Calculate down/distance tendencies
        down_dist_tendencies = plays.groupby(['posteam', 'down', pd.cut(plays['ydstogo'], bins=[0, 3, 7, 15, 100])]).agg({
            'play_type': lambda x: (x == 'pass').mean()
        }).rename(columns={'play_type': 'situation_pass_rate'})

        features = [
            'down', 'ydstogo', 'yardline_100',
            'score_differential', 'qtr', 'game_seconds_remaining',
            'team_pass_rate', 'team_avg_epa',
            'red_zone', 'goal_to_go', 'two_min_drill'
        ]

        # Target: 1 if pass, 0 if run
        plays['is_pass'] = (plays['play_type'] == 'pass').astype(int)

        df = plays[features + ['is_pass']].dropna()

        print(f"Defensive features: {len(df)} plays")
        print(f"Pass rate: {df['is_pass'].mean():.2%}")

        return df[features], df['is_pass']

    def engineer_fourth_down_features(self, pbp):
        """
        Engineer features for 4th down decision model

        Returns:
            DataFrame with features and outcomes
        """
        print("Engineering 4th down features...")

        # Filter for 4th down plays only
        fourth_downs = pbp[pbp['down'] == 4].copy()

        # Determine decision made
        def get_decision(row):
            if row.get('field_goal_attempt', 0) == 1:
                return 'kick'
            elif row.get('punt_attempt', 0) == 1:
                return 'punt'
            else:
                return 'go'

        fourth_downs['decision'] = fourth_downs.apply(get_decision, axis=1)

        # Features
        features = [
            'ydstogo', 'yardline_100', 'score_differential',
            'qtr', 'game_seconds_remaining',
            'posteam_timeouts_remaining'
        ]

        # Outcomes
        fourth_downs['converted'] = ((fourth_downs['series_success'] == 1) &
                                      (fourth_downs['decision'] == 'go')).astype(int)
        fourth_downs['fg_made'] = (fourth_downs.get('field_goal_result', '') == 'made').astype(int)

        df = fourth_downs[features + ['decision', 'converted', 'fg_made', 'epa', 'wpa']].dropna(subset=features)

        print(f"4th down features: {len(df)} plays")
        print(f"Decisions: {df['decision'].value_counts().to_dict()}")

        return df[features], df[['decision', 'converted', 'fg_made', 'epa', 'wpa']]

    def engineer_win_prob_features(self, pbp):
        """
        Engineer features for win probability model

        Returns:
            DataFrame with features and binary outcome (win/loss)
        """
        print("Engineering win probability features...")

        # We need game outcomes - get final scores
        game_outcomes = pbp.groupby(['game_id', 'home_team', 'away_team']).agg({
            'total_home_score': 'last',
            'total_away_score': 'last'
        }).reset_index()

        game_outcomes['home_won'] = (game_outcomes['total_home_score'] >
                                       game_outcomes['total_away_score']).astype(int)

        # Merge outcomes back to plays
        pbp_with_outcome = pbp.merge(game_outcomes[['game_id', 'home_won']], on='game_id', how='left')

        # Determine if possession team won
        pbp_with_outcome['posteam_won'] = pbp_with_outcome.apply(
            lambda row: row['home_won'] if row['posteam'] == row['home_team'] else 1 - row['home_won'],
            axis=1
        )

        features = [
            'score_differential', 'qtr', 'game_seconds_remaining',
            'yardline_100', 'down', 'ydstogo',
            'posteam_timeouts_remaining', 'defteam_timeouts_remaining'
        ]

        df = pbp_with_outcome[features + ['posteam_won']].dropna()

        print(f"Win probability features: {len(df)} plays")

        return df[features], df['posteam_won']

    def engineer_personnel_features(self, pbp, ftn=None):
        """
        Engineer features for personnel grouping optimizer

        Returns:
            DataFrame with features and target (personnel grouping)
        """
        print("Engineering personnel features...")

        # Check if pbp has personnel data
        if 'offense_personnel' in pbp.columns:
            merged = pbp[pbp['offense_personnel'].notna()].copy()
        elif ftn is not None and 'offense_personnel' in ftn.columns:
            # Merge FTN data with PBP
            merged = pbp.merge(ftn[['game_id', 'play_id', 'offense_personnel']],
                              on=['game_id', 'play_id'], how='inner')
        else:
            print("Warning: No personnel data available, using situation-based categories")
            # Create synthetic personnel categories based on situation
            merged = pbp.copy()
            def assign_personnel(row):
                # Rule-based personnel assignment
                if row.get('goal_to_go', 0) == 1:
                    return '13'  # Goal line
                elif row.get('ydstogo', 10) <= 2:
                    return '21'  # Short yardage
                elif row.get('ydstogo', 10) > 7:
                    return '11'  # Passing downs
                else:
                    return '12'  # Balanced
            merged['offense_personnel'] = merged.apply(assign_personnel, axis=1)

        # Train on ALL plays (removed EPA > 0.5 filter to include all personnel usage)
        features = [
            'down', 'ydstogo', 'yardline_100',
            'score_differential', 'red_zone', 'goal_to_go'
        ]

        # Clean personnel encoding (extract first 2 digits)
        merged['personnel_code'] = merged['offense_personnel'].astype(str).str[:2]

        df = merged[features + ['personnel_code', 'epa']].dropna()

        print(f"Personnel features: {len(df)} plays")
        print(f"Personnel groups: {df['personnel_code'].value_counts().head().to_dict()}")

        return df[features], df['personnel_code'], df['epa']

    def normalize_features(self, X, feature_name):
        """
        Normalize features using StandardScaler

        Args:
            X: Feature DataFrame
            feature_name: Name for caching the scaler

        Returns:
            Normalized features as numpy array
        """
        if feature_name not in self.scalers:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers[feature_name] = scaler
        else:
            X_scaled = self.scalers[feature_name].transform(X)

        return X_scaled

    def save_scalers_and_encoders(self):
        """Save all scalers and encoders for inference"""
        scalers_file = DATA_DIR / "scalers.pkl"
        encoders_file = DATA_DIR / "encoders.pkl"

        joblib.dump(self.scalers, scalers_file)
        joblib.dump(self.encoders, encoders_file)

        print(f"Saved scalers to {scalers_file}")
        print(f"Saved encoders to {encoders_file}")

    def load_scalers_and_encoders(self):
        """Load saved scalers and encoders"""
        scalers_file = DATA_DIR / "scalers.pkl"
        encoders_file = DATA_DIR / "encoders.pkl"

        if scalers_file.exists():
            self.scalers = joblib.load(scalers_file)
            print(f"Loaded scalers from {scalers_file}")

        if encoders_file.exists():
            self.encoders = joblib.load(encoders_file)
            print(f"Loaded encoders from {encoders_file}")


if __name__ == "__main__":
    from data_loader import NFLDataLoader

    # Test feature engineering
    loader = NFLDataLoader()
    data = loader.load_all_data()

    engineer = NFLFeatureEngineer()
    pbp_clean = engineer.clean_play_by_play(data['pbp'])

    X_off, y_off, epa_off = engineer.engineer_offensive_features(pbp_clean)
    print(f"\nOffensive features shape: {X_off.shape}")
    print(f"Target distribution: {y_off.value_counts()}")
