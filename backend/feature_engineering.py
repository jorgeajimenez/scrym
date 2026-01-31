"""
Feature Engineering Pipeline for 4th Down Bot
Focuses on situational awareness and win probability features.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import joblib

DATA_DIR = Path(__file__).parent.parent / "data"

class NFLFeatureEngineer:
    """Feature engineering specifically for 4th Down and Win Prob models"""

    def __init__(self):
        self.scalers = {}

    def clean_pbp(self, pbp):
        """Standard cleaning for NFL play-by-play data"""
        # Filter for Regular Season and Playoffs
        df = pbp[pbp['season_type'].isin(['REG', 'POST'])].copy()
        
        # Add core situational flags
        df['red_zone'] = (df['yardline_100'] <= 20).astype(int)
        df['goal_to_go'] = (df['yardline_100'] <= 10).astype(int)
        df['two_min_drill'] = ((df['game_seconds_remaining'] <= 120) & 
                              (df['qtr'].isin([2, 4]))).astype(int)
        
        return df

    def get_fourth_down_features(self, pbp):
        """Extract features and targets for 4th down decision model"""
        fd = pbp[pbp['down'] == 4].copy()
        
        # Define Decision Target
        def get_decision(row):
            if row.get('field_goal_attempt') == 1: return 'kick'
            if row.get('punt_attempt') == 1: return 'punt'
            return 'go'
        
        fd['decision'] = fd.apply(get_decision, axis=1)
        
        # Feature columns per Architecture Diagram
        features = [
            'ydstogo', 'yardline_100', 'score_differential',
            'qtr', 'game_seconds_remaining', 'posteam_timeouts_remaining'
        ]
        
        # Targets: Conversion (binary), FG Success (binary), EPA (float)
        fd['converted'] = ((fd['series_success'] == 1) & (fd['decision'] == 'go')).astype(int)
        fd['fg_made'] = (fd['field_goal_result'] == 'made').astype(int)
        
        df_clean = fd[features + ['decision', 'converted', 'fg_made', 'epa']].dropna(subset=features)
        return df_clean[features], df_clean[['decision', 'converted', 'fg_made', 'epa']]

    def get_win_prob_features(self, pbp):
        """Extract features and targets for Win Probability model"""
        # Calculate game winners
        outcomes = pbp.groupby('game_id').agg({
            'total_home_score': 'last',
            'total_away_score': 'last',
            'home_team': 'first'
        }).reset_index()
        
        outcomes['home_win'] = (outcomes['total_home_score'] > outcomes['total_away_score']).astype(int)
        
        # Merge back to PBP
        df = pbp.merge(outcomes[['game_id', 'home_win']], on='game_id', how='left')
        
        # Target: Did the possession team win?
        df['posteam_won'] = np.where(df['posteam'] == df['home_team'], df['home_win'], 1 - df['home_win'])
        
        features = [
            'score_differential', 'qtr', 'game_seconds_remaining',
            'yardline_100', 'down', 'ydstogo',
            'posteam_timeouts_remaining', 'defteam_timeouts_remaining'
        ]
        
        df_clean = df[features + ['posteam_won']].dropna()
        return df_clean[features], df_clean['posteam_won']

    def scale_features(self, X, name):
        """Apply and cache StandardScaler for real-time inference"""
        if name not in self.scalers:
            self.scalers[name] = StandardScaler()
            return self.scalers[name].fit_transform(X)
        return self.scalers[name].transform(X)

    def save_artifacts(self):
        """Save scalers for backend inference"""
        joblib.dump(self.scalers, DATA_DIR / "scalers.pkl")
        print(f"Artifacts saved to {DATA_DIR}/scalers.pkl")

if __name__ == "__main__":
    # Quick verification
    from data_loader import NFLDataLoader
    loader = NFLDataLoader()
    pbp = loader.load_play_by_play(years=range(2023, 2024)) # Test with 1 year
    
    fe = NFLFeatureEngineer()
    clean_df = fe.clean_pbp(pbp)
    X_fd, y_fd = fe.get_fourth_down_features(clean_df)
    X_wp, y_wp = fe.get_win_prob_features(clean_df)
    
    print(f"4th Down Data: {X_fd.shape}, Win Prob Data: {X_wp.shape}")
