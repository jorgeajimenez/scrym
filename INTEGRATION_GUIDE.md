# 🔗 Frontend-Backend Integration Guide: The "Nerve Center" (v2.0)

This document is **THE AUTHORITY** for connecting the Next.js Frontend to the FastAPI Backend. It is designed for a seamless "Copy-Paste" integration experience.

---

## 1. The Contract: Exact TypeScript Interfaces

These interfaces match the Backend's JSON responses exactly. **Copy this into `frontend/types/api.ts`.**

```typescript
// frontend/types/api.ts

export interface FourthDownResponse {
  recommendation: 'GO' | 'PUNT/KICK';
  conversion_probability: number; // 0.0 - 1.0
  fg_probability: number;         // 0.0 - 1.0
  expected_epa: number;
  win_probability: number;        // 0.0 - 1.0
}

export interface OffensiveResponse {
  recommendation: string;         // e.g., "Pass"
  probabilities: Record<string, number>; // e.g. { "Pass": 0.65, "Run": 0.35 }
}

export interface DefensiveResponse {
  recommendation: 'Pass Defense' | 'Run Defense';
  pass_probability: number;       // 0.0 - 1.0
}

export interface PersonnelResponse {
  recommendation: string;         // e.g., "11", "22"
  probabilities: Record<string, number>;
}

export interface FormationResponse {
  formation_name: string;         // e.g., "Shotgun Spread"
  players: Array<{
    role: string;                 // "QB", "WR", etc.
    x: number;                    // -25 to 25 (Horizontal)
    y: number;                    // Negative = Offense, Positive = Defense
    color: string;                // "blue" or "red"
  }>;
}

export interface AnalysisResponse {
  analysis: string;               // The Gemini "Coach's Note" text
}
```

---

## 2. The Bridge: Ready-to-Use API Client

**Copy this into `frontend/lib/api.ts`.** It handles the endpoints and the necessary data transformations (like sorting the offensive plays).

```typescript
// frontend/lib/api.ts
import { GameState } from '@/types'; // Your local state type
import { 
  FourthDownResponse, OffensiveResponse, DefensiveResponse, 
  FormationResponse, PersonnelResponse, AnalysisResponse 
} from '@/types/api';

const API_BASE = 'http://localhost:8000';

async function post<T>(endpoint: string, body: any): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API Error: ${res.statusText}`);
  return res.json();
}

export const api = {
  // 1. Head Coach (Traffic Light)
  predictFourthDown: (state: GameState) => 
    post<FourthDownResponse>('/predict/fourth-down', state),

  // 2. Offensive Coord (Play Menu)
  predictOffense: async (state: GameState) => {
    const data = await post<OffensiveResponse>('/predict/offensive', state);
    // Transform dict to sorted array for UI
    const sorted = Object.entries(data.probabilities)
      .map(([name, prob]) => ({ name, prob }))
      .sort((a, b) => b.prob - a.prob);
    return { ...data, sortedPredictions: sorted };
  },

  // 3. Defensive Coord (Radar)
  predictDefense: (state: GameState) => 
    post<DefensiveResponse>('/predict/defensive', state),

  // 4. Visuals (Formation)
  getFormation: (playType: string, personnel: string, ydstogo: number) => 
    post<FormationResponse>('/predict/formation', { 
      play_type: playType, personnel, ydstogo 
    }),

  // 5. Assistant Coach (Gemini)
  analyzePlay: (state: GameState, recommendation: string) => 
    post<AnalysisResponse>('/analyze/play', { 
      state, recommendation, team_abbr: "KC" 
    })
};
```

---

## 3. Integration Patterns (The "How-To")

### A. The "Parallel Load" Pattern
*   **Problem:** We want instant numbers (PyTorch) but also smart text (Gemini).
*   **Solution:** Fire both requests at once. Do not await Gemini to show the Green Light.

```typescript
// In your Component
const handlePrediction = async () => {
  setLoading(true);
  
  // 1. Fire Critical Path (Math)
  const mathPromise = api.predictFourthDown(gameState);
  
  // 2. Fire Secondary Path (Context) - Don't await yet!
  const textPromise = api.analyzePlay(gameState, "Analyzing...");

  // 3. Show Math ASAP
  const result = await mathPromise;
  setResult(result); // UI turns Green/Red immediately
  setLoading(false);

  // 4. Show Text when ready
  const analysis = await textPromise;
  setCoachNote(analysis.analysis); // Pop-up appears 1-2s later
};
```

### B. The "Formation Chaining" Pattern
*   **Context:** The Offensive Model gives us a play ("Pass"), but we need to show dots on a field.
*   **Logic:**
    1.  Call `predictOffense`.
    2.  Get the top recommendation (e.g., "Pass").
    3.  *Then* call `getFormation("Pass", currentPersonnel, distance)`.
    4.  Render the canvas.

### C. Clock Synchronization ("The Heartbeat")
The frontend runs a `setInterval` every 1000ms to tick the clock.
*   **IF** `clock_running === true`: Decrement `time_remaining`.
*   **IF** `time_remaining === 0`: End Quarter.
*   **Important:** This is purely visual. The Backend is the source of truth for the *actual* game time during simulations.

---

## 4. Troubleshooting for Frontend Devs

*   **Error:** `{"detail":"Models not loaded"}`
    *   **Fix:** The backend hasn't been trained. Tell the backend engineer to run `python backend/train.py`.
*   **Error:** `Connection Refused`
    *   **Fix:** Ensure `uvicorn` is running on port 8000.
*   **Visual:** "The formation dots look weird."
    *   **Fix:** Remember `y` coordinates: Negative is Offense (bottom), Positive is Defense (top). Origin `(0,0)` is the ball.