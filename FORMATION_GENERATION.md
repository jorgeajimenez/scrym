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

---

## 3. Visualization Payload & Coordinates
To render these formations on the Frontend (Canvas/SVG), the Backend returns a standard coordinate payload.

### 📐 Coordinate System
*   **Origin (0,0):** The Center / Ball at the Line of Scrimmage.
*   **X-Axis:** Horizontal Position (Yards). Range: `[-25, 25]` (Hash marks are approx +/- 6).
*   **Y-Axis:** Depth (Yards).
    *   **Negative (< 0):** Offensive Backfield.
    *   **Positive (> 0):** Defensive Secondary.

### 📦 JSON Payload Structure
The API response includes a `formation_data` object:

```json
{
  "formation_name": "Shotgun Spread",
  "players": [
    { "role": "C",  "x": 0,   "y": 0,  "color": "blue" },
    { "role": "QB", "x": 0,   "y": -5, "color": "blue" },
    { "role": "LT", "x": -2,  "y": 0,  "color": "blue" },
    { "role": "RT", "x": 2,   "y": 0,  "color": "blue" },
    { "role": "LG", "x": -1,  "y": 0,  "color": "blue" },
    { "role": "RG", "x": 1,   "y": 0,  "color": "blue" },
    { "role": "WR", "x": -20, "y": 0,  "color": "blue" },
    { "role": "WR", "x": 20,  "y": 0,  "color": "blue" },
    { "role": "WR", "x": -15, "y": 0,  "color": "blue" },
    { "role": "RB", "x": 3,   "y": -5, "color": "blue" },
    { "role": "TE", "x": 4,   "y": 0,  "color": "blue" }
  ]
}
```

### 📍 Preset Coordinates (The "Playbook")

#### A. Offensive Presets

**1. Shotgun Spread (11 Personnel)**
*   **Concept:** QB back, 3 WRs wide to stretch the field.
*   **Key Coords:**
    *   QB: `(0, -5)`
    *   RB: `(1.5, -5)` (Offset)
    *   WRs: `(-22, 0)`, `(22, 0)`, `(-18, 0)` (Slot)
    *   TE: `(4, 0)` (Inline)

**2. I-Formation (21 Personnel)**
*   **Concept:** Power Run. QB under center, FB and RB in a line.
*   **Key Coords:**
    *   QB: `(0, -1)`
    *   FB: `(0, -4)`
    *   RB: `(0, -7)`
    *   WRs: `(-20, 0)`, `(20, 0)`
    *   TE: `(3, 0)`

**3. Empty / 5-Wide (00/10 Personnel)**
*   **Concept:** Max passing. No backfield help.
*   **Key Coords:**
    *   QB: `(0, -5)`
    *   WRs: `(-22, 0)`, `(-16, 0)`, `(22, 0)`, `(16, 0)`, `(10, 0)` (Trips Right)

#### B. Defensive Presets

**1. Base 4-3**
*   **Concept:** Balanced.
*   **Key Coords:**
    *   DL: `(-3, 1)`, `(-1, 1)`, `(1, 1)`, `(3, 1)`
    *   LB: `(-4, 4)`, `(0, 4)` (Mike), `(4, 4)`
    *   CB: `(-22, 5)`, `(22, 5)`
    *   S: `(-8, 12)`, `(8, 12)`

**2. Nickel (4-2-5)**
*   **Concept:** Pass coverage replacement.
*   **Key Coords:**
    *   Removes one LB `(4, 4)`.
    *   Adds Nickel CB (Slot): `(-18, 3)` (Matches Slot WR).

**3. Goal Line (6-2)**
*   **Concept:** Stop the run. Everyone tight.
*   **Key Coords:**
    *   DL/LB Line: 6 players tight `y=1`.
    *   Secondary: 5 yards deep `y=5`.

### Implementation Strategy
Create a file `backend/formation_logic.py`:
1.  Define a dictionary `FORMATION_TEMPLATES` containing these coordinate lists.
2.  In the `suggest_offensive_formation` function, return the *entire* list of coordinates based on the selected name.