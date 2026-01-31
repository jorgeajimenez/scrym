# 🔍 Demo Gap Analysis

This document compares the current `mockups/` (visual prototype) against the `INTEGRATION_GUIDE.md` (functional requirements) to identify the work needed for the Next.js implementation.

## 1. Core Logic Gaps (The "Brain" Transplant)

The mockups use `Math.random()` and hardcoded arrays. The Next.js app must replace these with live API calls.

| Feature | Mockup State | Required Integration | Gap |
| :--- | :--- | :--- | :--- |
| **Clock** | `setInterval` decrements local var | **Sync with Backend:** Need `useGameClock` hook to sync with `GameState.time_remaining` from API. | 🔴 High |
| **4th Down Decision** | Static HTML "GO FOR IT" | **Live Inference:** Call `/predict/fourth-down`. Handle "Loading" state (spinner/pulse). Map API probability to "Confidence Meter". | 🔴 High |
| **Offensive Play** | Click toggles text | **Dynamic Cards:** Call `/predict/offensive`. Render top 3 choices as cards. Sort by probability. | 🔴 High |
| **Defensive Radar** | Static SVG | **Live Gauge:** Call `/predict/defensive`. Animate needle based on `pass_probability`. | 🟠 Medium |
| **Formations** | Hardcoded `FORMATIONS` const | **API Fetch:** Call `/predict/formation` based on the selected play. Render returned `(x,y)` coordinates. | 🟠 Medium |

## 2. Visual Gaps (The "Polish")

The mockups look good but lack the feedback loops defined in the Integration Guide.

*   **Loading States:** The mockups assume instant data. We need "calculating..." animations for the 50-100ms API latency.
*   **Gemini Integration:** The mockups do not show the "Coach's Note" bubble. We need a UI component to display the text from `/analyze/play`.
*   **Error Handling:** What happens if the API is down? The mockup doesn't show an "Offline" or "Retry" state.

## 3. Data Structure Mismatches

### Formation Coordinates
*   **Mockup:** Uses `0.0 - 1.0` normalized canvas coordinates.
*   **API:** Returns **Yards** (`-25` to `25`).
*   **Fix:** The Frontend `Canvas` component needs a **Coordinate Mapper**:
    ```typescript
    const mapX = (yardX: number) => canvasWidth/2 + (yardX * PIXELS_PER_YARD);
    const mapY = (yardY: number) => LOS_Y - (yardY * PIXELS_PER_YARD);
    ```

### Game State Input
*   **Mockup:** Doesn't really track `down`, `distance`, `score`. It just visualizes.
*   **Requirement:** The Next.js app needs a **Control Panel** (or use the "Demo Scenario" dropdown) to actually *set* the state passed to the API.

## 4. Action Plan for Next.js Sprint

1.  **Scaffold:** Initialize Next.js with the `api.ts` client from the Guide.
2.  **State:** Build `GameContext` to hold the "Master State" (Down, Dist, Clock).
3.  **Components:** Port the HTML/CSS from mockups into React Components (`<Hudson>`, `<Radar>`, `<Field>`).
4.  **Wiring:**
    *   Hook up `<TrafficLight>` to `api.predictFourthDown`.
    *   Hook up `<Field>` to `api.getFormation`.
5.  **Gemini:** Add the "Assistant" chat bubble component.
