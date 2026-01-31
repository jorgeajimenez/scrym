"""
Verification script for Issue #2 (Data Pipeline)
"""
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from data_loader import NFLDataLoader
    from feature_engineering import NFLFeatureEngineer
    
    print("🚀 Initializing Verification...")
    loader = NFLDataLoader()
    
    # Using 2023 only for rapid verification
    print("📥 Loading 2023 PBP data...")
    pbp = loader.load_play_by_play(years=range(2023, 2024))
    
    engineer = NFLFeatureEngineer()
    clean_pbp = engineer.clean_pbp(pbp)
    
    X_fd, y_fd = engineer.get_fourth_down_features(clean_pbp)
    X_wp, y_wp = engineer.get_win_prob_features(clean_pbp)
    
    print("\n✅ Verification Successful!")
    print(f"- PBP Total Plays: {len(pbp)}")
    print(f"- 4th Down Samples: {len(X_fd)}")
    print(f"- Win Prob Samples: {len(X_wp)}")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Ensure you have installed requirements: pip install -r backend/requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")

