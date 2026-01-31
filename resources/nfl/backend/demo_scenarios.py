"""
Demo Testing Script for NFL AI Coach Models
Tests models with realistic game scenarios to validate training improvements

Run this to see how your retrained models perform on various game situations
"""

import torch
import numpy as np
import joblib
from pathlib import Path
from models import create_model
from typing import Dict, Any

# Paths
MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

# Device
device = torch.device('cpu')


class NFLModelTester:
    """Test NFL models with realistic game scenarios"""

    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.load_all_models()

    def load_all_models(self):
        """Load all models, scalers, and encoders"""
        print("Loading models and scalers...\n")

        # Load scalers
        self.scalers = joblib.load(DATA_DIR / "scalers.pkl")
        self.encoders = joblib.load(DATA_DIR / "encoders.pkl")

        # Load offensive model
        le_off = joblib.load(MODEL_DIR / 'offensive_label_encoder.pkl')
        X_shape = self.scalers['offensive'].mean_.shape[0]
        off_model = create_model('offensive', input_dim=X_shape, num_classes=len(le_off.classes_))
        off_model.load_state_dict(torch.load(MODEL_DIR / 'offensive_model.pt', map_location=device, weights_only=True))
        off_model.eval()
        self.models['offensive'] = (off_model, le_off)

        # Load defensive model
        X_shape = self.scalers['defensive'].mean_.shape[0]
        def_model = create_model('defensive', input_dim=X_shape)
        def_model.load_state_dict(torch.load(MODEL_DIR / 'defensive_model.pt', map_location=device, weights_only=True))
        def_model.eval()
        self.models['defensive'] = def_model

        # Load 4th down model
        X_shape = self.scalers['fourth_down'].mean_.shape[0]
        fourth_model = create_model('fourth_down', input_dim=X_shape)
        fourth_model.load_state_dict(torch.load(MODEL_DIR / 'fourth_down_model.pt', map_location=device, weights_only=True))
        fourth_model.eval()
        self.models['fourth_down'] = fourth_model

        # Load win probability model
        X_shape = self.scalers['win_prob'].mean_.shape[0]
        wp_model = create_model('win_prob', input_dim=X_shape)
        wp_model.load_state_dict(torch.load(MODEL_DIR / 'win_prob_model.pt', map_location=device, weights_only=True))
        wp_model.eval()
        self.models['win_prob'] = wp_model

        # Load personnel model
        le_pers = joblib.load(MODEL_DIR / 'personnel_label_encoder.pkl')
        X_shape = self.scalers['personnel'].mean_.shape[0]
        pers_model = create_model('personnel', input_dim=X_shape, num_personnel_groups=len(le_pers.classes_))
        pers_model.load_state_dict(torch.load(MODEL_DIR / 'personnel_model.pt', map_location=device, weights_only=True))
        pers_model.eval()
        self.models['personnel'] = (pers_model, le_pers)

        print("✓ All models loaded successfully!\n")

    def predict_offensive_play(self, scenario: Dict[str, Any]) -> Dict:
        """Predict offensive play call"""
        # Feature: down, ydstogo, yardline_100, score_differential, qtr,
        #          game_seconds_remaining, half_seconds_remaining, red_zone,
        #          goal_to_go, two_min_drill, posteam_timeouts_remaining, team_encoded
        features = np.array([[
            scenario['down'],
            scenario['distance'],
            scenario['yard_line'],
            scenario['score_diff'],
            scenario['quarter'],
            scenario['time_remaining'],
            scenario.get('half_seconds_remaining', scenario['time_remaining']),
            scenario['red_zone'],
            scenario['goal_to_go'],
            scenario['two_min_drill'],
            scenario['timeouts'],
            0  # team_encoded (default)
        ]])

        features_scaled = self.scalers['offensive'].transform(features)
        model, label_encoder = self.models['offensive']

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            probs = model.predict_proba(features_tensor).numpy()[0]

        play_types = label_encoder.classes_
        probabilities = {play: float(prob) for play, prob in zip(play_types, probs)}
        recommended = play_types[np.argmax(probs)]

        return {
            'recommended_play': recommended,
            'probabilities': probabilities,
            'confidence': float(max(probs))
        }

    def predict_defensive_tendency(self, scenario: Dict[str, Any]) -> Dict:
        """Predict opponent's play tendency"""
        # Feature: down, ydstogo, yardline_100, score_differential, qtr,
        #          game_seconds_remaining, team_pass_rate, team_avg_epa,
        #          red_zone, goal_to_go, two_min_drill
        features = np.array([[
            scenario['down'],
            scenario['distance'],
            scenario['yard_line'],
            scenario['score_diff'],
            scenario['quarter'],
            scenario['time_remaining'],
            0.58,  # league avg pass rate
            0.0,   # league avg epa
            scenario['red_zone'],
            scenario['goal_to_go'],
            scenario['two_min_drill']
        ]])

        features_scaled = self.scalers['defensive'].transform(features)
        model = self.models['defensive']

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            pass_prob = float(model.predict_proba(features_tensor).numpy()[0][0])

        return {
            'pass_probability': pass_prob,
            'run_probability': 1 - pass_prob,
            'prediction': 'PASS' if pass_prob > 0.5 else 'RUN'
        }

    def predict_fourth_down(self, scenario: Dict[str, Any]) -> Dict:
        """Predict 4th down decision"""
        # Feature: ydstogo, yardline_100, score_differential, qtr,
        #          game_seconds_remaining, posteam_timeouts_remaining
        features = np.array([[
            scenario['distance'],
            scenario['yard_line'],
            scenario['score_diff'],
            scenario['quarter'],
            scenario['time_remaining'],
            scenario['timeouts']
        ]])

        features_scaled = self.scalers['fourth_down'].transform(features)
        model = self.models['fourth_down']

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            conv_prob, fg_prob, epa = model.forward(features_tensor)

        conv_prob = float(conv_prob.numpy()[0][0])
        fg_prob = float(fg_prob.numpy()[0][0])

        # Calculate expected values
        in_fg_range = scenario['yard_line'] < 35
        ev_go = conv_prob * 3.0
        ev_fg = fg_prob * 3.0 if in_fg_range else 0.0
        ev_punt = 1.5

        decision_values = {'go': ev_go, 'kick': ev_fg, 'punt': ev_punt}
        recommendation = max(decision_values, key=decision_values.get)

        return {
            'recommendation': recommendation.upper(),
            'conversion_prob': conv_prob,
            'fg_success_prob': fg_prob if in_fg_range else None,
            'expected_values': decision_values
        }

    def predict_win_probability(self, scenario: Dict[str, Any]) -> Dict:
        """Predict win probability"""
        # Feature: score_differential, qtr, game_seconds_remaining, yardline_100,
        #          down, ydstogo, posteam_timeouts_remaining, defteam_timeouts_remaining
        features = np.array([[
            scenario['score_diff'],
            scenario['quarter'],
            scenario['time_remaining'],
            scenario['yard_line'],
            scenario['down'],
            scenario['distance'],
            scenario['timeouts'],
            scenario.get('opp_timeouts', 3)
        ]])

        features_scaled = self.scalers['win_prob'].transform(features)
        model = self.models['win_prob']

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            win_prob = float(model.predict_proba(features_tensor).numpy()[0][0])

        return {
            'win_probability': win_prob * 100,
            'lose_probability': (1 - win_prob) * 100
        }

    def predict_personnel(self, scenario: Dict[str, Any]) -> Dict:
        """Predict optimal personnel grouping"""
        # Feature: down, ydstogo, yardline_100, score_differential, red_zone, goal_to_go
        features = np.array([[
            scenario['down'],
            scenario['distance'],
            scenario['yard_line'],
            scenario['score_diff'],
            scenario['red_zone'],
            scenario['goal_to_go']
        ]])

        features_scaled = self.scalers['personnel'].transform(features)
        model, label_encoder = self.models['personnel']

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            probs = model.predict_proba(features_tensor).numpy()[0]

        personnel_groups = label_encoder.classes_
        probabilities = {group: float(prob) for group, prob in zip(personnel_groups, probs)}
        recommended = personnel_groups[np.argmax(probs)]

        return {
            'recommended_personnel': recommended,
            'probabilities': {k: v for k, v in probabilities.items() if v > 0.05},  # Only show >5%
            'confidence': float(max(probs))
        }

    def test_scenario(self, scenario: Dict[str, Any], name: str):
        """Test a complete game scenario"""
        print("=" * 80)
        print(f"SCENARIO: {name}")
        print("=" * 80)
        print(f"Situation: {scenario['down_text']} at {scenario['field_position']}")
        print(f"Score: {scenario['score_text']} | Q{scenario['quarter']} - {scenario['time_text']}")
        print(f"Timeouts: {scenario['timeouts']}")
        print()

        # Win Probability
        win_pred = self.predict_win_probability(scenario)
        print(f"📊 WIN PROBABILITY: {win_pred['win_probability']:.1f}%")
        print()

        # Offensive Play Call
        off_pred = self.predict_offensive_play(scenario)
        print(f"🏈 OFFENSIVE PLAY CALL:")
        print(f"   Recommended: {off_pred['recommended_play'].upper()} ({off_pred['confidence']:.1%} confidence)")
        print(f"   Play Probabilities:")
        for play, prob in sorted(off_pred['probabilities'].items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(prob * 30)
            print(f"      {play:12} {prob:5.1%} {bar}")
        print()

        # Defensive Prediction
        def_pred = self.predict_defensive_tendency(scenario)
        print(f"🛡️  DEFENSIVE COORDINATOR:")
        print(f"   Opponent likely to: {def_pred['prediction']}")
        print(f"   Pass probability: {def_pred['pass_probability']:.1%}")
        print(f"   Run probability:  {def_pred['run_probability']:.1%}")
        print()

        # Personnel
        pers_pred = self.predict_personnel(scenario)
        print(f"👥 PERSONNEL GROUPING:")
        print(f"   Recommended: {pers_pred['recommended_personnel']} personnel")
        if pers_pred['probabilities']:
            print(f"   Top choices:")
            for group, prob in sorted(pers_pred['probabilities'].items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"      {group}: {prob:.1%}")
        print()

        # 4th Down (if applicable)
        if scenario['down'] == 4:
            fourth_pred = self.predict_fourth_down(scenario)
            print(f"🎯 4TH DOWN DECISION:")
            print(f"   Recommendation: {fourth_pred['recommendation']}")
            print(f"   Conversion probability: {fourth_pred['conversion_prob']:.1%}")
            if fourth_pred['fg_success_prob'] is not None:
                print(f"   FG success probability: {fourth_pred['fg_success_prob']:.1%}")
            print(f"   Expected values: {fourth_pred['expected_values']}")
            print()

        print()


def main():
    """Run demo scenarios"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "NFL AI COACH - MODEL DEMO" + " " * 33 + "║")
    print("║" + " " * 15 + "Testing Retrained Models on Game Scenarios" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")

    tester = NFLModelTester()

    # Scenario 1: Goal line situation
    scenario1 = {
        'name': 'Goal Line - TD or Bust',
        'down': 3,
        'down_text': '3rd & Goal',
        'distance': 2,
        'yard_line': 2,
        'field_position': 'Opponent 2',
        'score_diff': -3,
        'score_text': 'Down by 3',
        'quarter': 4,
        'time_remaining': 120,
        'time_text': '2:00',
        'timeouts': 1,
        'opp_timeouts': 3,
        'red_zone': 1,
        'goal_to_go': 1,
        'two_min_drill': 1
    }

    # Scenario 2: Long 3rd down
    scenario2 = {
        'name': 'Desperation 3rd Down',
        'down': 3,
        'down_text': '3rd & 15',
        'distance': 15,
        'yard_line': 35,
        'field_position': 'Own 35',
        'score_diff': -7,
        'score_text': 'Down by 7',
        'quarter': 4,
        'time_remaining': 300,
        'time_text': '5:00',
        'timeouts': 2,
        'opp_timeouts': 2,
        'red_zone': 0,
        'goal_to_go': 0,
        'two_min_drill': 0
    }

    # Scenario 3: 4th and short
    scenario3 = {
        'name': 'Analytics Dream: 4th & 1',
        'down': 4,
        'down_text': '4th & 1',
        'distance': 1,
        'yard_line': 45,
        'field_position': 'Opponent 45',
        'score_diff': 0,
        'score_text': 'Tied',
        'quarter': 2,
        'time_remaining': 2100,
        'time_text': '5:00 (Q2)',
        'timeouts': 3,
        'opp_timeouts': 3,
        'red_zone': 0,
        'goal_to_go': 0,
        'two_min_drill': 0
    }

    # Scenario 4: Comfortable lead, clock management
    scenario4 = {
        'name': 'Clock Management Mode',
        'down': 2,
        'down_text': '2nd & 5',
        'distance': 5,
        'yard_line': 70,
        'field_position': 'Own 30',
        'score_diff': 10,
        'score_text': 'Up by 10',
        'quarter': 4,
        'time_remaining': 180,
        'time_text': '3:00',
        'timeouts': 3,
        'opp_timeouts': 0,
        'red_zone': 0,
        'goal_to_go': 0,
        'two_min_drill': 1
    }

    # Scenario 5: Hail Mary time
    scenario5 = {
        'name': 'Hail Mary Situation',
        'down': 4,
        'down_text': '4th & 10',
        'distance': 10,
        'yard_line': 60,
        'field_position': 'Own 40',
        'score_diff': -4,
        'score_text': 'Down by 4',
        'quarter': 4,
        'time_remaining': 3,
        'time_text': '0:03',
        'timeouts': 0,
        'opp_timeouts': 2,
        'red_zone': 0,
        'goal_to_go': 0,
        'two_min_drill': 1
    }

    # Scenario 6: Red zone, first down
    scenario6 = {
        'name': 'Red Zone - 1st Down',
        'down': 1,
        'down_text': '1st & 10',
        'distance': 10,
        'yard_line': 15,
        'field_position': 'Opponent 15',
        'score_diff': 3,
        'score_text': 'Up by 3',
        'quarter': 3,
        'time_remaining': 2700,
        'time_text': '0:00 (Q3 start)',
        'timeouts': 3,
        'opp_timeouts': 3,
        'red_zone': 1,
        'goal_to_go': 0,
        'two_min_drill': 0
    }

    scenarios = [scenario1, scenario2, scenario3, scenario4, scenario5, scenario6]

    for scenario in scenarios:
        tester.test_scenario(scenario, scenario['name'])

    print("=" * 80)
    print("TESTING COMPLETE!")
    print("=" * 80)
    print("\nThese predictions are based on your retrained models that now include:")
    print("  ✓ ALL plays (successful AND failed)")
    print("  ✓ 229,345 offensive plays (was ~115k)")
    print("  ✓ 253,995 personnel situations (was ~127k)")
    print("\nModels should now have better real-world performance!")
    print()


if __name__ == "__main__":
    main()
