"""
Live NFL Game Data Integration
Fetches real-time game data from ESPN API
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime


class NFLLiveDataAPI:
    """Fetch live NFL game data from ESPN"""

    ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    ESPN_GAME_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def get_live_games(self) -> List[Dict]:
        """
        Get all live/in-progress NFL games

        Returns:
            List of game dictionaries with basic info
        """
        try:
            response = self.session.get(self.ESPN_SCOREBOARD_URL, timeout=10)
            response.raise_for_status()
            data = response.json()

            games = []
            for event in data.get('events', []):
                competition = event['competitions'][0]
                status = competition['status']

                # Check if game is live
                if status['type']['state'] in ['in', 'post']:  # in-progress or recently finished
                    game_info = {
                        'game_id': event['id'],
                        'name': event['name'],
                        'status': status['type']['description'],
                        'quarter': status.get('period', 1),
                        'clock': status.get('displayClock', '15:00'),
                        'home_team': competition['competitors'][0]['team']['abbreviation'],
                        'away_team': competition['competitors'][1]['team']['abbreviation'],
                        'home_score': int(competition['competitors'][0]['score']),
                        'away_score': int(competition['competitors'][1]['score']),
                        'is_live': status['type']['state'] == 'in'
                    }
                    games.append(game_info)

            return games

        except Exception as e:
            print(f"Error fetching live games: {e}")
            return []

    def get_game_details(self, game_id: str) -> Optional[Dict]:
        """
        Get detailed game situation for a specific game

        Args:
            game_id: ESPN game ID

        Returns:
            Dictionary with detailed game state or None
        """
        try:
            response = self.session.get(
                self.ESPN_GAME_URL,
                params={'event': game_id},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            # Extract game details
            header = data.get('header', {})
            competition = header['competitions'][0]
            status = competition['status']
            situation = competition.get('situation', {})

            home_team = competition['competitors'][0]['team']['abbreviation']
            away_team = competition['competitors'][1]['team']['abbreviation']
            possession_team = situation.get('possession', home_team) if situation else home_team

            # Parse clock to seconds
            clock_display = status.get('displayClock', '15:00')
            try:
                if ':' in clock_display:
                    parts = clock_display.split(':')
                    time_seconds = int(parts[0]) * 60 + int(parts[1])
                else:
                    time_seconds = 900  # Default to 15 min
            except:
                time_seconds = 900

            # Calculate game seconds remaining
            quarter = status.get('period', 1)
            if quarter <= 4:
                quarters_remaining = 4 - quarter
                game_seconds_remaining = quarters_remaining * 900 + time_seconds
            else:  # Overtime
                game_seconds_remaining = time_seconds

            game_state = {
                'home_team': home_team,
                'away_team': away_team,
                'possession': possession_team,
                'quarter': quarter if quarter <= 4 else 5,  # 5 for OT
                'time_remaining': game_seconds_remaining,
                'down': situation.get('downDistanceText', '1st & 10').split('&')[0].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '').strip() if situation else 1,
                'distance': situation.get('distance', 10) if situation else 10,
                'yard_line': 100 - situation.get('yardLine', 50) if situation else 50,  # Convert to yards from opponent goal
                'home_score': int(competition['competitors'][0]['score']),
                'away_score': int(competition['competitors'][1]['score']),
                'home_timeouts': situation.get('homeTimeouts', 3) if situation else 3,
                'away_timeouts': situation.get('awayTimeouts', 3) if situation else 3,
            }

            # Clean down value
            try:
                down_text = situation.get('shortDownDistanceText', '1st')
                if '1st' in down_text:
                    game_state['down'] = 1
                elif '2nd' in down_text:
                    game_state['down'] = 2
                elif '3rd' in down_text:
                    game_state['down'] = 3
                elif '4th' in down_text:
                    game_state['down'] = 4
                else:
                    game_state['down'] = 1
            except:
                game_state['down'] = 1

            return game_state

        except Exception as e:
            print(f"Error fetching game details: {e}")
            return None


if __name__ == "__main__":
    # Test the API
    api = NFLLiveDataAPI()

    print("Fetching live NFL games...")
    live_games = api.get_live_games()

    if live_games:
        print(f"\nFound {len(live_games)} live/recent games:\n")
        for game in live_games:
            print(f"  {game['name']}")
            print(f"  Status: {game['status']}")
            print(f"  Score: {game['home_team']} {game['home_score']} - {game['away_team']} {game['away_score']}")
            print(f"  Q{game['quarter']} - {game['clock']}")
            print()

        # Get details for first game
        if live_games:
            print(f"\nGetting details for: {live_games[0]['name']}")
            details = api.get_game_details(live_games[0]['game_id'])
            if details:
                print("\nGame State:")
                for key, value in details.items():
                    print(f"  {key}: {value}")
    else:
        print("No live games found. Try during NFL game time!")
