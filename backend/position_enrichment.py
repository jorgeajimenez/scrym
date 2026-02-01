"""
Position Enrichment for ML Models
Converts Vision Agent position data into features for EPA/WP models.
"""
import numpy as np
from typing import List, Dict

def extract_formation_features(players: List[Dict]) -> Dict:
    """
    Extract formation features from player positions.
    Returns dict of features for ML models.
    """
    offense = [p for p in players if p['team'] == 'offense']
    defense = [p for p in players if p['team'] == 'defense']

    # Receiver spread (horizontal variance)
    receiver_positions = [p for p in offense if p['role'] in ['WR', 'TE']]
    if receiver_positions:
        receiver_xs = [p['x'] for p in receiver_positions]
        receiver_spread = float(np.std(receiver_xs))
    else:
        receiver_spread = 0.0

    # Defensive front pressure (distance to QB)
    qb = next((p for p in offense if p['role'] == 'QB'), None)
    if qb:
        d_line = [p for p in defense if p['role'] in ['DE', 'DT']]
        if d_line:
            distances = [abs(p['y'] - qb['y']) for p in d_line]
            avg_pressure_distance = float(np.mean(distances))
        else:
            avg_pressure_distance = 0.5
    else:
        avg_pressure_distance = 0.5

    # Coverage shell depth (safety positioning)
    safeties = [p for p in defense if p['role'] == 'S']
    if safeties:
        safety_depth = float(np.mean([p['y'] for p in safeties]))
    else:
        safety_depth = 0.3

    # Personnel count
    num_receivers = len([p for p in offense if p['role'] in ['WR', 'TE']])
    num_backs = len([p for p in offense if p['role'] in ['RB', 'FB']])

    return {
        'receiver_spread': receiver_spread,
        'pressure_distance': avg_pressure_distance,
        'safety_depth': safety_depth,
        'num_receivers': num_receivers,
        'num_backs': num_backs,
        'is_empty_set': 1 if num_backs == 0 else 0,
        'is_heavy_set': 1 if num_backs >= 2 else 0
    }

def calculate_coverage_gaps(players: List[Dict]) -> List[Dict]:
    """
    Identify coverage gaps based on defensive positioning.
    Returns list of gap zones: {x, y, radius, severity}
    """
    offense_receivers = [p for p in players if p['team'] == 'offense' and p['role'] in ['WR', 'TE']]
    defense_secondary = [p for p in players if p['team'] == 'defense' and p['role'] in ['CB', 'S']]

    gaps = []

    for receiver in offense_receivers:
        # Find nearest defender
        if defense_secondary:
            distances = [
                float(np.sqrt((receiver['x'] - d['x'])**2 + (receiver['y'] - d['y'])**2))
                for d in defense_secondary
            ]
            min_distance = min(distances)

            # Gap detected if receiver is uncovered
            if min_distance > 0.15:  # Threshold: 15% of field width
                gaps.append({
                    'x': receiver['x'],
                    'y': receiver['y'],
                    'radius': min_distance,
                    'severity': min(min_distance / 0.3, 1.0)  # Normalize 0-1
                })

    return gaps
