# ⏱️ Game Clock & Simulation Logic

To move beyond static demos, we can simulate entire games or **specific high-leverage segments** by replaying historical data or generating synthetic sequences. This allows us to test the AI Coach in a continuous "Game Loop".

## 1. The Simulation Loop
The simulation runs state-to-state transitions based on the AI's decisions and probabilistic outcomes.

### Core State Object
```json
{
  "game_id": "sim_001",
  "qtr": 1,
  "time": 900, 
  "score": {"home": 0, "away": 0},
  "possession": "home",
  "down": 1,
  "distance": 10,
  "ball_on": 25 
}
```

## 2. Partial Simulation ("Jump In" Mode)
Instead of starting from kickoff, we can initiate simulations for specific critical segments. This is essential for testing "Clutch" performance without waiting through early-game noise.

### Common "Jump In" Points:
*   **The 2-Minute Drill:** Start at Q4 2:00, down by 4-8 points.
*   **The Goal Line Stand:** Start at 1st & Goal on the 2-yard line.
*   **Overtime:** Start at OT 10:00, tied score.
*   **The Comeback:** Start at Q3 5:00, down by 21 points.

## 3. Entering Simulation Mode from the UI
The UI provides two primary entry points for the simulation engine:

### A. The "Simulate Scenario" Button
*   **Location:** Found inside the "Demo Scenarios" or "Quick Start" drawer.
*   **Interaction:** 
    1. User selects a scenario (e.g., "The Aggressive Go").
    2. User clicks the **"LIVE SIM"** button.
    3. The UI locks the "Manual Input" fields and begins auto-updating the state as the AI "plays" through the scenario.

### B. The "Contextual Playback" Toggle
*   **Location:** Top-right corner of the Dashboard.
*   **Interaction:** 
    1. A simple toggle switch: **[MANUAL | AUTO-SIM]**.
    2. In **AUTO-SIM**, every recommendation the AI makes is automatically "executed," and the state progresses.
    3. This is used for "Stress Testing" where a coach wants to see how the AI's logic plays out over a sequence of 5-10 plays.

## 4. Clock Management Logic
Testing the "Clock Strategy" features requires correct time simulation.

*   **Running Clock:** If play = `Run` or `Complete (in bounds)`, subtract ~40s (play + play clock).
*   **Stopped Clock:** If play = `Incomplete` or `Out of Bounds`, subtract ~6-10s (play duration only).
*   **Timeouts:** If AI suggests "Timeout", stop the clock decay logic for that step.

## 5. Implementation Plan (Future)
Create `backend/simulation.py`:
```python
class GameSimulator:
    def __init__(self, start_state=None):
        self.state = start_state or self.get_default_kickoff()

    def step(self, action):
        # 1. Calculate result based on probabilities
        # 2. Update clock based on play type
        # 3. Update field position/down/dist
        return self.state, is_done
```