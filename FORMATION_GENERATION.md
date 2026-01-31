# ♟️ Formation Generation Logic

While the AI models predict *what* to do (e.g., "Pass" or "Run Defense"), **Formation Generation** translates that intent into a visual on-field alignment.

## 1. Offensive Formation Logic
We deduce the formation from the **Situation** and the **Recommended Play**.

### Inputs
*   **Situational Context:** `ydstogo`, `two_min_drill`, `score_differential`
*   **Predicted Play:** `Pass` vs `Run`
*   **Predicted Personnel:** `11`, `12`, `22`, etc.

### Logic Matrix

| Play Type | Situation | Personnel | **Suggested Formation** | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Pass** | 3rd & Long (>7) | 11 / 10 | **Shotgun Spread** | Maximize visibility and receiver spacing. |
| **Pass** | Standard | 12 / 13 | **Singleback Ace** | Balanced look to sell the run. |
| **Run** | Short Yardage (<2) | 22 / 13 | **I-Formation** | Lead blocker (FB) leverage. |
| **Run** | Standard | 11 | **Pistol / Shotgun** | Read-option threat. |
| **Any** | 2-Min Drill | Any | **Empty / 5-Wide** | No-huddle efficiency. |

### Implementation Snippet (Pseudocode)
```python
def suggest_offensive_formation(play_type, personnel, ydstogo, is_2min):
    if is_2min: return "Empty Set (5-Wide)"
    
    if play_type == 'run':
        if personnel in ['21', '22'] and ydstogo < 3: return "I-Formation (Power)"
        return "Pistol"
    
    if play_type == 'pass':
        if ydstogo > 7: return "Shotgun Trips"
        return "Singleback"
```

---

## 2. Defensive Formation Logic
Defense is reactive. We align based on the **Predicted Offense** and the **Offensive Personnel**.

### Inputs
*   **Offensive Personnel:** (e.g., `11` - 3 WRs)
*   **Predicted Offense:** `Pass` (High Prob) vs `Run`
*   **Field Position:** `red_zone`, `goal_to_go`

### Logic Matrix

| Off. Personnel | Predicted Intent | Situation | **Suggested Defense** | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **11 (3 WRs)** | High Pass Prob | Standard | **Nickel (4-2-5)** | Swap LB for CB (Nickel) to cover slot. |
| **10 / 01 (4-5 WRs)**| High Pass Prob | Any | **Dime (4-1-6)** | Maximum speed on field. |
| **21 / 12 (2 WRs)** | High Run Prob | Standard | **Base (4-3 / 3-4)** | Standard front to plug gaps. |
| **22 / 13 (Heavy)** | High Run Prob | Short Yardage | **Goal Line (5-3 / 6-2)**| Sell out to stop the run. |

### Implementation Snippet (Pseudocode)
```python
def suggest_defensive_alignment(off_personnel, is_pass_likely, is_goal_line):
    if is_goal_line: return "6-2 Goal Line"
    
    wr_count = get_wr_count(off_personnel) # e.g., '11' -> 3 WRs
    
    if wr_count >= 4: return "Dime"
    if wr_count == 3: return "Nickel"
    
    if is_pass_likely: return "Nickel (Blitz Look)"
    return "Base 4-3"
```
