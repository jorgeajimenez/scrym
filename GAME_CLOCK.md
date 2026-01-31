# ⏱️ Game Clock & Simulation Logic

To move beyond static demos, we can simulate entire games by replaying historical data or generating synthetic sequences. This allows us to test the AI Coach in a continuous "Game Loop".

## 1. The Simulation Loop
The simulation runs state-to-state transitions based on the AI's decisions and probabilistic outcomes.

### Core State Object
```json
{
  "game_id": "sim_001",
  "qtr": 1,
  "time": 900, # Seconds remaining in quarter
  "score": {"home": 0, "away": 0},
  "possession": "home",
  "down": 1,
  "distance": 10,
  "ball_on": 25 # Own 25
}
```

### The Loop Logic
1.  **Input:** Current State.
2.  **AI Decision:** The Offense calls a play (e.g., "Pass").
3.  **Outcome Generation (The "Dice Roll"):**
    *   We use historical distributions to determine the result.
    *   *Example:* A "Pass" on "1st & 10" averages 7.5 yards, with a 65% completion rate.
    *   **Roll:** `rng.random()` -> Result: "Complete, 12 yards".
4.  **State Update:**
    *   `ball_on` += 12
    *   `down` = 1 (Reset)
    *   `distance` = 10
    *   **Clock Decay:** Subtract `avg_play_duration` (e.g., 35s for run, 10s for incomplete pass).
5.  **Check Triggers:**
    *   Did clock hit 0? -> End Quarter.
    *   Did ball cross 100? -> Touchdown (+6 pts).
    *   Is it 4th Down? -> Trigger 4th Down Bot.

## 2. Replaying Historical Games (Backtesting)
Instead of generating outcomes, we feed the system real plays from `pbp_2023.parquet` sequentially.

**Workflow:**
1.  Load Game `2023_01_KC_DET`.
2.  **Play 1:** `(KC, 1st & 10, Q1 15:00)`.
    *   **AI Predicts:** "Pass".
    *   **Actual:** "Pass, Mahomes to Kelce, 10 yards".
    *   **Score:** Match! (or Mismatch).
3.  **Play 2:** `(KC, 1st & 10, Q1 14:25)`.
    *   ...repeat...

**Metric:** "Agreement Rate" (How often did the AI agree with Andy Reid?).

## 3. Clock Management Logic
Testing the "Clock Strategy" features requires correct time simulation.

*   **Running Clock:** If play = `Run` or `Complete (in bounds)`, subtract ~40s (play + play clock).
*   **Stopped Clock:** If play = `Incomplete` or `Out of Bounds`, subtract ~6-10s (play duration only).
*   **Timeouts:** If AI suggests "Timeout", stop the clock decay logic for that step.

## 4. Implementation Plan (Future)
Create `backend/simulation.py`:
```python
class GameSimulator:
    def step(self, action):
        # Calculate result based on probabilities
        # Update clock
        # Update field position
        return new_state, reward, done
```
