"""
Formation Generation Logic for NFL AI Coach
Translates game situations and predicted plays into visual coordinates.
"""

# Coordinate System:
# Origin (0,0) = Center/Ball
# X: Horizontal (-25 to 25)
# Y: Depth (Negative = Offense, Positive = Defense)

FORMATION_TEMPLATES = {
    # --- OFFENSIVE FORMATIONS ---
    "Shotgun Spread": [
        {"role": "C", "x": 0, "y": 0, "color": "blue"},
        {"role": "LG", "x": -1.5, "y": 0, "color": "blue"},
        {"role": "RG", "x": 1.5, "y": 0, "color": "blue"},
        {"role": "LT", "x": -3, "y": 0, "color": "blue"},
        {"role": "RT", "x": 3, "y": 0, "color": "blue"},
        {"role": "QB", "x": 0, "y": -5, "color": "blue"},
        {"role": "RB", "x": 1.5, "y": -5, "color": "blue"},
        {"role": "WR", "x": -20, "y": 0, "color": "blue"},
        {"role": "WR", "x": 20, "y": 0, "color": "blue"},
        {"role": "WR", "x": -15, "y": 0, "color": "blue"}, # Slot
        {"role": "TE", "x": 4.5, "y": 0, "color": "blue"}
    ],
    "Gun Bunch Right": [
        {"role": "C", "x": 0, "y": 0, "color": "blue"},
        {"role": "LG", "x": -1.5, "y": 0, "color": "blue"},
        {"role": "RG", "x": 1.5, "y": 0, "color": "blue"},
        {"role": "LT", "x": -3, "y": 0, "color": "blue"},
        {"role": "RT", "x": 3, "y": 0, "color": "blue"},
        {"role": "QB", "x": 0, "y": -5, "color": "blue"},
        {"role": "RB", "x": -1.5, "y": -5, "color": "blue"}, # Weak side RB
        {"role": "WR", "x": -20, "y": 0, "color": "blue"},   # Iso X
        {"role": "WR", "x": 12, "y": 0, "color": "blue"},    # Point
        {"role": "WR", "x": 14, "y": -1, "color": "blue"},   # Wing
        {"role": "TE", "x": 10, "y": -1, "color": "blue"}    # Inside Bunch
    ],
    "Singleback Ace": [
        {"role": "C", "x": 0, "y": 0, "color": "blue"},
        {"role": "LG", "x": -1.5, "y": 0, "color": "blue"},
        {"role": "RG", "x": 1.5, "y": 0, "color": "blue"},
        {"role": "LT", "x": -3, "y": 0, "color": "blue"},
        {"role": "RT", "x": 3, "y": 0, "color": "blue"},
        {"role": "QB", "x": 0, "y": -1, "color": "blue"},
        {"role": "RB", "x": 0, "y": -6, "color": "blue"},
        {"role": "WR", "x": -20, "y": 0, "color": "blue"},
        {"role": "WR", "x": 20, "y": 0, "color": "blue"},
        {"role": "TE", "x": -4.5, "y": 0, "color": "blue"},
        {"role": "TE", "x": 4.5, "y": 0, "color": "blue"}
    ],
    "I-Formation": [
        {"role": "C", "x": 0, "y": 0, "color": "blue"},
        {"role": "LG", "x": -1.5, "y": 0, "color": "blue"},
        {"role": "RG", "x": 1.5, "y": 0, "color": "blue"},
        {"role": "LT", "x": -3, "y": 0, "color": "blue"},
        {"role": "RT", "x": 3, "y": 0, "color": "blue"},
        {"role": "QB", "x": 0, "y": -1, "color": "blue"},
        {"role": "FB", "x": 0, "y": -4, "color": "blue"},
        {"role": "RB", "x": 0, "y": -7, "color": "blue"},
        {"role": "WR", "x": -20, "y": 0, "color": "blue"},
        {"role": "WR", "x": 20, "y": 0, "color": "blue"},
        {"role": "TE", "x": 4.5, "y": 0, "color": "blue"}
    ],
    "Pistol Strong": [
        {"role": "C", "x": 0, "y": 0, "color": "blue"},
        {"role": "LG", "x": -1.5, "y": 0, "color": "blue"},
        {"role": "RG", "x": 1.5, "y": 0, "color": "blue"},
        {"role": "LT", "x": -3, "y": 0, "color": "blue"},
        {"role": "RT", "x": 3, "y": 0, "color": "blue"},
        {"role": "QB", "x": 0, "y": -4, "color": "blue"},
        {"role": "RB", "x": 0, "y": -7, "color": "blue"},
        {"role": "TE", "x": 4.5, "y": 0, "color": "blue"}, # Y
        {"role": "TE", "x": -4.5, "y": -1, "color": "blue"}, # H-Back (Wing)
        {"role": "WR", "x": -20, "y": 0, "color": "blue"},
        {"role": "WR", "x": 20, "y": 0, "color": "blue"}
    ],
    "Empty Set": [
        {"role": "C", "x": 0, "y": 0, "color": "blue"},
        {"role": "LG", "x": -1.5, "y": 0, "color": "blue"},
        {"role": "RG", "x": 1.5, "y": 0, "color": "blue"},
        {"role": "LT", "x": -3, "y": 0, "color": "blue"},
        {"role": "RT", "x": 3, "y": 0, "color": "blue"},
        {"role": "QB", "x": 0, "y": -5, "color": "blue"},
        {"role": "WR", "x": -22, "y": 0, "color": "blue"},
        {"role": "WR", "x": -16, "y": 0, "color": "blue"},
        {"role": "WR", "x": 22, "y": 0, "color": "blue"},
        {"role": "WR", "x": 16, "y": 0, "color": "blue"},
        {"role": "WR", "x": 10, "y": 0, "color": "blue"}
    ],
    "Goal Line Jumbo": [
        {"role": "C", "x": 0, "y": 0, "color": "blue"},
        {"role": "LG", "x": -1.5, "y": 0, "color": "blue"},
        {"role": "RG", "x": 1.5, "y": 0, "color": "blue"},
        {"role": "LT", "x": -3, "y": 0, "color": "blue"},
        {"role": "RT", "x": 3, "y": 0, "color": "blue"},
        {"role": "TE", "x": -4.5, "y": 0, "color": "blue"},
        {"role": "TE", "x": 4.5, "y": 0, "color": "blue"},
        {"role": "TE", "x": 6, "y": 0, "color": "blue"}, # Extra heavy
        {"role": "QB", "x": 0, "y": -1, "color": "blue"},
        {"role": "FB", "x": 0, "y": -3, "color": "blue"},
        {"role": "RB", "x": 0, "y": -6, "color": "blue"}
    ],
    
    # --- DEFENSIVE FORMATIONS ---
    "Base 4-3": [
        {"role": "DE", "x": -4, "y": 1, "color": "red"},
        {"role": "DT", "x": -1.5, "y": 1, "color": "red"},
        {"role": "DT", "x": 1.5, "y": 1, "color": "red"},
        {"role": "DE", "x": 4, "y": 1, "color": "red"},
        {"role": "LB", "x": -4, "y": 4, "color": "red"},
        {"role": "MLB", "x": 0, "y": 4, "color": "red"},
        {"role": "LB", "x": 4, "y": 4, "color": "red"},
        {"role": "CB", "x": -20, "y": 5, "color": "red"},
        {"role": "CB", "x": 20, "y": 5, "color": "red"},
        {"role": "S", "x": -8, "y": 12, "color": "red"},
        {"role": "S", "x": 8, "y": 12, "color": "red"}
    ],
    "Nickel 4-2-5": [
        {"role": "DE", "x": -4, "y": 1, "color": "red"},
        {"role": "DT", "x": -1.5, "y": 1, "color": "red"},
        {"role": "DT", "x": 1.5, "y": 1, "color": "red"},
        {"role": "DE", "x": 4, "y": 1, "color": "red"},
        {"role": "LB", "x": -3, "y": 4, "color": "red"},
        {"role": "LB", "x": 3, "y": 4, "color": "red"},
        {"role": "NCB", "x": -15, "y": 3, "color": "red"}, # Slot corner
        {"role": "CB", "x": -20, "y": 5, "color": "red"},
        {"role": "CB", "x": 20, "y": 5, "color": "red"},
        {"role": "S", "x": -8, "y": 12, "color": "red"},
        {"role": "S", "x": 8, "y": 12, "color": "red"}
    ],
    "Goal Line 6-2": [
        {"role": "DL", "x": -5, "y": 1, "color": "red"},
        {"role": "DL", "x": -3, "y": 1, "color": "red"},
        {"role": "DL", "x": -1, "y": 1, "color": "red"},
        {"role": "DL", "x": 1, "y": 1, "color": "red"},
        {"role": "DL", "x": 3, "y": 1, "color": "red"},
        {"role": "DL", "x": 5, "y": 1, "color": "red"},
        {"role": "LB", "x": -2, "y": 2.5, "color": "red"},
        {"role": "LB", "x": 2, "y": 2.5, "color": "red"},
        {"role": "DB", "x": -10, "y": 4, "color": "red"},
        {"role": "DB", "x": 10, "y": 4, "color": "red"},
        {"role": "S", "x": 0, "y": 6, "color": "red"}
    ]
}

def get_offensive_formation(play_type, personnel, ydstogo, is_2min):
    """Determine offensive formation name based on context."""
    if is_2min: return "Empty Set"
    
    # Goal Line Logic
    if ydstogo <= 1 and personnel in ['22', '23', '13']:
        return "Goal Line Jumbo"

    if "run" in play_type.lower():
        if personnel in ['21', '22', '13']:
            # Variance: Pistol or I-Form?
            # Use distance as heuristic: Short = Power (I), Medium = Pistol
            if ydstogo < 3: return "I-Formation"
            return "Pistol Strong"
        return "Singleback Ace"
        
    # Passing Logic
    if ydstogo >= 10: return "Empty Set" # Aggressive spread
    if ydstogo > 6: return "Shotgun Spread"
    if ydstogo >= 3: return "Gun Bunch Right" # Man-beater territory
    
    return "Singleback Ace"

def get_defensive_formation(off_personnel, is_pass_likely, is_goal_line):
    """Determine defensive alignment based on context."""
    if is_goal_line: return "Goal Line 6-2"
        
    # Check for spread sets (3+ WRs)
    if off_personnel in ['11', '10', '01']:
        return "Nickel 4-2-5"
    
    if is_pass_likely > 0.75:
        return "Nickel 4-2-5" # Blitz look
        
    return "Base 4-3"

def generate_formation_payload(formation_name):
    """Return the coordinate list for the given formation."""
    return FORMATION_TEMPLATES.get(formation_name, [])
