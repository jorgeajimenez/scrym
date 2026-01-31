"""
NFL Data Loading and Caching Module
Handles data retrieval from nfl_data_py and caching for fast reloading
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
        Load play-by-play data with caching

        Args:
            years: Range of years to load (default 2018-2024)
            force_reload: Force download even if cache exists

        Returns:
            DataFrame with play-by-play data
        """
        cache_file = self.cache_dir / "pbp_2018_2024.parquet"

        if cache_file.exists() and not force_reload:
            print(f"Loading cached play-by-play data from {cache_file}")
            return pd.read_parquet(cache_file)

        print(f"Downloading play-by-play data for years {list(years)}...")
        pbp = nfl.import_pbp_data(years=list(years))

        # Save to cache
        print(f"Caching data to {cache_file}")
        pbp.to_parquet(cache_file)

        return pbp

    def load_ftn_charting(self, years=range(2022, 2025), force_reload=False):
        """
        Load FTN charting data (personnel groupings)

        Args:
            years: Range of years to load (default 2022-2024)
            force_reload: Force download even if cache exists

        Returns:
            DataFrame with FTN charting data or None if not available
        """
        cache_file = self.cache_dir / "ftn_2022_2024.parquet"

        if cache_file.exists() and not force_reload:
            print(f"Loading cached FTN data from {cache_file}")
            return pd.read_parquet(cache_file)

        try:
            print(f"Downloading FTN charting data for years {list(years)}...")
            ftn = nfl.import_ftn_data(years=list(years))

            # Save to cache
            print(f"Caching FTN data to {cache_file}")
            ftn.to_parquet(cache_file)

            return ftn
        except Exception as e:
            print(f"Warning: Could not load FTN data: {e}")
            return None

    def load_rosters(self, years=range(2022, 2025), force_reload=False):
        """
        Load roster data

        Args:
            years: Range of years to load
            force_reload: Force download even if cache exists

        Returns:
            DataFrame with roster data
        """
        cache_file = self.cache_dir / "rosters_2022_2024.parquet"

        if cache_file.exists() and not force_reload:
            print(f"Loading cached roster data from {cache_file}")
            return pd.read_parquet(cache_file)

        print(f"Downloading roster data for years {list(years)}...")
        rosters = nfl.import_seasonal_rosters(years=list(years))

        # Save to cache
        print(f"Caching roster data to {cache_file}")
        rosters.to_parquet(cache_file)

        return rosters

    def load_all_data(self, force_reload=False):
        """
        Load all required data for model training

        Returns:
            Dictionary with all data sources
        """
        print("Loading all NFL data...")

        data = {
            'pbp': self.load_play_by_play(force_reload=force_reload),
            'ftn': self.load_ftn_charting(force_reload=force_reload),
            'rosters': self.load_rosters(force_reload=force_reload)
        }

        print(f"Data loaded: PBP={len(data['pbp'])} plays, "
              f"FTN={len(data['ftn']) if data['ftn'] is not None else 0} plays")

        return data


if __name__ == "__main__":
    # Test data loading
    loader = NFLDataLoader()
    data = loader.load_all_data()

    print("\nPlay-by-play columns:", data['pbp'].columns.tolist()[:20], "...")
    print("Shape:", data['pbp'].shape)
