# 🔗 Frontend-Backend Integration Guide: The "Nerve Center"

This document is **THE AUTHORITY** on how the `Next.js` frontend stitches together with the `FastAPI` backend. It goes beyond simple API contracts—it defines the *soul* of the application: the rhythm, the tension, and the flow of a live NFL game.

**Reference Documents:**
*   `API_GUIDE.md` (Endpoints)
*   `MODELS_AND_UX.md` (UI/Model Mapping)
*   `GAME_CLOCK.md` (Simulation State)
*   `FORMATION_GENERATION.md` (Visuals Logic)

---

## 1. System Philosophy: "The Coach's Headset"

The application is not just a dashboard; it is a **Headset**. It needs to feel immediate, authoritative, and responsive.

*   **Frontend (The Headset):**
    *   **Role:** Presentation & Tension.
    *   **Feel:** Slick, dark-mode, high-contrast (think NFL on Fox graphics).
    *   **Responsibility:** It *never* waits. The clock ticks, the crowd noise (visual) swells. It demands data from the backend but handles the "waiting" gracefully with pulsing skeletons and animations.
*   **Backend (The Coordinator):**
    *   **Role:** The Brain.
    *   **Responsibility:** Pure logic. It doesn't care about pixels. It cares about probability. It provides the "Source of Truth" for the game state.

---

## 2. Shared Data Models (The Contract)

To ensure type safety, the Frontend **TypeScript interfaces** must match the Backend **Pydantic models**.

### Core `GameState` Object
This object is the "Batton" passed back and forth. It *must* be consistent.

```typescript
// frontend/types/index.ts

export interface GameState {
  game_id: string;
  // Context
  qtr: number; // 1-4, 5 (OT)
  time_remaining: number; // Seconds (e.g., 900 for 15:00)
  play_clock: number; // Seconds (e.g., 40 or 25)
  clock_running: boolean; // Is the game clock currently ticking?
  score_home: number;
  score_away: number;
  possession: 'home' | 'away';
  
  // Field State
  down: number; // 1-4
  ydstogo: number; // Distance to 1st down
  yardline_100: number; // 0-100 (100 = Own Endzone, 0 = Opponent Endzone)
  
  // Logic Flags
  red_zone: boolean; // Calculated property (yardline_100 <= 20)
  goal_to_go: boolean;
  two_min_drill: boolean; // Calculated (time < 120 && qtrIsEnd)
  
  // Timeouts
  timeouts_home: number;
  timeouts_away: number;
}
```

### Response Interfaces

**1. Fourth Down Prediction (`/predict/fourth-down`)**
```typescript
export interface FourthDownResponse {
  recommendation: 'GO' | 'PUNT' | 'FG';
  conversion_probability: number;
  fg_probability: number;
  expected_epa: number;
  win_probability: number;
}
```

**2. Offensive Prediction (`/predict/offensive`)**
```typescript
export interface OffensiveResponse {
  recommendation: string; // "Pass", "Run"
  probabilities: Record<string, number>; // { "Pass": 0.6, "Run": 0.4 }
  // + Formation Data via separate call
}
```

---

## 3. The Heartbeat: Real-Time Clock Synchronization

To make the UI feel "live," the Game Clock and Play Clock must tick down in the UI while remaining synchronized with the Backend's simulation logic. **This is the most critical UX element.**

### ⏳ The Two-Clock System
1.  **Game Clock:** 15:00 per quarter. The overarching constraint.
2.  **Play Clock:** 40s. The immediate panic.

### 🔄 Synchronization Strategy (The "Rubber Band" Method)
*   **The Ticking Logic (Frontend):** 
    *   The Frontend uses a `useEffect` interval (every 1s) to decrement `time_remaining` and `play_clock` *locally*.
    *   *UX Note:* Use a monospace font for the digits. They should not "jump" around.
*   **The Source of Truth (Backend):**
    *   When a play is simulated (`/simulate/step`), the Backend calculates the *exact* result (e.g., "Run play took 6 seconds, plus 34 seconds runoff = 40s elapsed").
    *   The Frontend then **"snaps"** its local clock to the Backend's returned `time_remaining`.
    *   *Dev Aside:* If the UI clock drifts by 1-2 seconds, that's fine. If it drifts by 10s, the snap will look glitchy. Keep the local tick accurate.

### 🛑 Clock Stoppage Rules (Backend Logic)
The Backend must set `clock_running: false` if:
*   Incomplete Pass.
*   Out of Bounds.
*   Timeout.
*   Possession Change.
*   Penalty.

---

## 4. Feature Integration: "The Movie Script"

### 🚦 Feature A: Head Coach "Traffic Light" (The Climax)
**The Vibe:** It's 4th & 1. The stadium is shaking. You have 3 seconds to decide.
**Integration Logic:**
1.  **Trigger:** Frontend detects `GameState.down === 4`.
2.  **Action:** Async call to `POST /predict/fourth-down`.
3.  **Loading State:** Do **NOT** just show a spinner. Show a "CALCULATING..." text that flashes red/yellow/green rapidly, building tension.
4.  **The Reveal:** 
    *   The result (e.g., **"GO FOR IT"**) slams onto the screen.
    *   Confidence meter fills up.

### 📋 Feature B: Offensive Coordinator "Play Menu" (The Rhythm)
**The Vibe:** Rapid-fire calling. Read the defense, pick a card.
**Integration Logic:**
1.  **Trigger:** Immediately after a play ends.
2.  **Action:** Async call to `POST /predict/offensive`.
3.  **Formation Logic:** Call `POST /predict/formation` with the recommended play.
4.  **Render:** 
    *   **The Cards:** Three large clickable cards. The "Best" play is largest.
    *   **Visual:** Draw the formation (dots) on a mini-field using the returned coordinates.

### 🛡️ Feature C: Defensive Coordinator "Radar" (The Paranoia)
**The Vibe:** They are up to something. What is it?
**Integration Logic:**
1.  **Trigger:** Pre-snap.
2.  **Action:** Async call to `POST /predict/defensive`.
3.  **Render:** 
    *   **The Gauge:** A needle wobbling between "RUN" and "PASS". It shouldn't be perfectly still; add some CSS jitter to mimic uncertainty.
    *   **The Alarm:** If `pass_probability > 80%`, flash a "BLITZ ALERT" badge.

### 🧠 Feature D: Gemini Assistant Coach (The Wisdom)
**The Vibe:** A veteran coach whispering in your ear, reviewing the AI's logic.
**Integration Logic:**
1.  **Trigger:** After a predictive model returns a result (e.g., "GO" or "PASS").
2.  **Action:** Call `POST /analyze/play`.
3.  **Parallel Pattern:** 
    *   Call the Predictive Model and Gemini **simultaneously**. 
    *   The Predictive Model result is the **Primary Trigger** (shows the Green Light instantly).
    *   The Gemini response follows shortly after (e.g., +1s delay) as a **"Coach's Note"** or notification bubble.
4.  **Content:** This adds roster awareness (e.g., "Mahomes is in the rhythm, trust the pass") that the raw weights lack.

---

## 5. Simulation Mode: "Ghost in the Machine"

This allows the AI to play against itself, essential for demos.

### New API Endpoint: `POST /simulate/step`
**Request:**
```json
{
  "current_state": { ...GameState... },
  "action_taken": "Pass" 
}
```

**Response:**
```json
{
  "new_state": { ...GameState... }, // Updated time, score, etc.
  "play_result": {
    "yards_gained": 12,
    "description": "Pass complete to J.Jefferson for 12 yards.",
    "is_turnover": false,
    "clock_impact": "running"
  }
}
```

### The "Auto-Sim" Loop (Frontend)
When the user toggles **[AUTO-SIM]**:
1.  **Frontend:** "Taking control..."
2.  **Loop:**
    *   Get `GameState`.
    *   Call AI (OC/HC) -> Get Top Recommendation (e.g., "Pass").
    *   **Visual:** Highlight the "Pass" card as if a ghost clicked it.
    *   Send "Pass" to `/simulate/step`.
    *   **Visual:** Show text "Result: 12 Yard Gain".
    *   **Wait:** 2000ms (Let the user read).
    *   **Reset:** Reset Play Clock to 40.
    *   **Repeat.**

---

## 6. Development Checklist

### Backend Tasks
- [x] **Standardize Models:** Ensure `main.py` matches `GameState` exactly.
- [ ] **Implement Clock Logic:** In `simulate/step`, precise time math is key.
- [x] **Formation Logic:** Implement the "Logic Matrix" from `FORMATION_GENERATION.md`.

### Frontend Tasks
- [ ] **Clock Hook:** `useGameClock()` - The heartbeat.
- [ ] **State Provider:** `GameContext.tsx` - The single source of truth.
- [ ] **Visuals:** Implement the "Jitter" on the radar and the "Slam" on the 4th down decision.
