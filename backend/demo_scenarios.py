"""
Demo Scenarios for NFL AI Coach
Curated high-pressure situations to showcase the system's capabilities.
"""

SCENARIOS = {
    "scen_1": {
        "id": "scen_1",
        "title": "The aggressive Go",
        "description": "4th & 1 on Opponent 45. Tie Game. 3rd Quarter.",
        "state": {
            "down": 4,
            "ydstogo": 1,
            "yardline_100": 45,
            "score_differential": 0,
            "qtr": 3,
            "game_seconds_remaining": 900,
            "posteam_timeouts_remaining": 3,
            "defteam_timeouts_remaining": 3
        },
        "expected_result": {
            "recommendation": "GO",
            "confidence": "HIGH",
            "win_prob_delta": "+3.5%"
        }
    },
    "scen_2": {
        "id": "scen_2",
        "title": "The Conservative Punt",
        "description": "4th & 8 on Own 30. Up by 4. 4th Quarter (2:00 left).",
        "state": {
            "down": 4,
            "ydstogo": 8,
            "yardline_100": 70,
            "score_differential": 4,
            "qtr": 4,
            "game_seconds_remaining": 120,
            "posteam_timeouts_remaining": 2,
            "defteam_timeouts_remaining": 3
        },
        "expected_result": {
            "recommendation": "PUNT",
            "confidence": "VERY HIGH",
            "win_prob_delta": "-12.0% if GO fail"
        }
    },
    "scen_3": {
        "id": "scen_3",
        "title": "Field Goal Range",
        "description": "4th & 5 on Opponent 25. Down by 2. 4th Quarter (0:04 left).",
        "state": {
            "down": 4,
            "ydstogo": 5,
            "yardline_100": 25,
            "score_differential": -2,
            "qtr": 4,
            "game_seconds_remaining": 4,
            "posteam_timeouts_remaining": 0,
            "defteam_timeouts_remaining": 0
        },
        "expected_result": {
            "recommendation": "KICK",
            "confidence": "MAXIMUM",
            "win_prob_delta": "Win or Lose"
        }
    }
}

def get_demo_scenarios():
    return list(SCENARIOS.values())

def get_scenario_by_id(scenario_id):
    return SCENARIOS.get(scenario_id)
