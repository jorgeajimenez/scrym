"""
NFL Data Loading and Caching Module
Custom implementation for the 4th Down Bot Intelligence.
"""

import nfl_data_py as nfl
import pandas as pd
import os
from pathlib import Path

# Data directories
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

class NFLDataLoader:
    """Handles loading and caching NFL data from nfl_data_py"""

    def __init__(self, cache_dir=DATA_DIR):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def load_play_by_play(self, years=range(2018, 2025), force_reload=False):
        """
        Load play-by-play data with local parquet caching.
        """
        cache_file = self.cache_dir / f"pbp_{years.start}_{years.stop-1}.parquet"

        if cache_file.exists() and not force_reload:
            print(f"Loading cached play-by-play data from {cache_file}")
            return pd.read_parquet(cache_file)

        print(f"Downloading play-by-play data for years {list(years)}...")
        pbp = nfl.import_pbp_data(years=list(years))

        print(f"Caching data to {cache_file}")
        pbp.to_parquet(cache_file)
        return pbp

    def load_ftn_charting(self, years=range(2022, 2025), force_reload=False):
        """
        Load FTN charting data (personnel/defensive details)
        """
        cache_file = self.cache_dir / f"ftn_{years.start}_{years.stop-1}.parquet"

        if cache_file.exists() and not force_reload:
            print(f"Loading cached FTN data from {cache_file}")
            return pd.read_parquet(cache_file)

        try:
            print(f"Downloading FTN charting data for years {list(years)}...")
            ftn = nfl.import_ftn_data(years=list(years))
            ftn.to_parquet(cache_file)
            return ftn
        except Exception as e:
            print(f"Warning: Could not load FTN data: {e}")
            return None

    def load_all_intelligence_data(self, force_reload=False):
        """
        Load all data required for 4th down and WP model training.
        """
        print("Initializing Intelligence Data Pipeline...")
        data = {
            'pbp': self.load_play_by_play(force_reload=force_reload),
            'ftn': self.load_ftn_charting(force_reload=force_reload),
            'rosters': self.load_rosters(force_reload=force_reload)
        }
        return data

    def get_team_starters(self, team_abbr, year=2024):
        """
        Get key offensive starters for a team/year to provide context to Gemini.
        """
        try:
            rosters = self.load_rosters(years=[year])
            # Filter for team
            team_roster = rosters[rosters['team'] == team_abbr]
            
            # Simple heuristic for "Key Players" if depth chart data is missing
            # In a real app, we'd use 'depth_chart_position' == 1
            # Here we just grab the first player of each key position
            key_positions = ['QB', 'RB', 'WR', 'TE']
            starters = {}
            
            for pos in key_positions:
                players = team_roster[team_roster['position'] == pos]['player_name'].head(2).tolist()
                starters[pos] = players
                
            return starters
        except Exception as e:
            print(f"Warning: Could not load roster context: {e}")
            return {}

if __name__ == "__main__":
    loader = NFLDataLoader()
    # Test with a small sample if needed, but here we expect full load for training later
    data = loader.load_all_intelligence_data()
    print(f"Pipeline Ready: {len(data['pbp'])} plays ingested.")
