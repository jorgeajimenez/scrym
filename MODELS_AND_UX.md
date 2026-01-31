# 🧠 Models & UX Integration Guide

This document explains how the 5 Neural Networks in the backend map directly to the features in the "NFL AI Coach" UI.

---

## 1. The "Traffic Light" (Head Coach View)
**Goal:** High-pressure decision making on 4th Down.

### 🤖 Model: 4th Down Decision Engine
*   **What it Computes:**
    *   `conversion_prob` (0-100%): Chance of getting the 1st down.
    *   `fg_prob` (0-100%): Chance of making the kick.
    *   `expected_epa`: Mathematical value of the decision.
*   **When to Run:** Automatically triggers when `down == 4`.
*   **UI Mapping:**
    *   **Green Light ("GO"):** If `conversion_prob > threshold` AND `epa(GO) > epa(PUNT)`.
    *   **Yellow Light ("KICK"):** If `fg_prob` is high and `epa(KICK)` is maximized.
    *   **Blue Light ("PUNT"):** Default safe option.

### 🤖 Model: Win Probability Calculator
*   **What it Computes:** `win_prob` (0-100%).
*   **When to Run:** Updates after *every* play result.
*   **UI Mapping:**
    *   displayed as a live percentage (e.g., "Win Prob: 42%").
    *   Used to contextually color-code decisions (e.g., if Win Prob is < 5%, the "GO" threshold lowers because you *need* to take risks).

---

## 2. The "Play Menu" (Offensive Coordinator View)
**Goal:** Instant play-calling suggestions before the play clock expires.

### 🤖 Model: Offensive Play Caller
*   **What it Computes:** Probabilities for 5 play types:
    *   `Pass`, `Run`, `Play Action`, `Screen`, `Draw`.
*   **When to Run:** Immediately after a play ends (for the *next* down).
*   **UI Mapping:**
    *   **The Cards:** The top 3 highest-probability classes become the big "Play Cards" in the UI.
    *   *Example:* If Model outputs `{Pass: 0.6, Run: 0.3, Screen: 0.1}`, the UI shows a huge **"PASS"** card and a smaller **"RUN"** card.

### 🤖 Model: Personnel Optimizer
*   **What it Computes:** Ideal personnel grouping (e.g., `11`, `12`, `22`).
*   **When to Run:** When entering the Red Zone or on critical 3rd downs.
*   **UI Mapping:**
    *   **Alert Icon:** "⚠️ Rec: 12 Personnel" pops up if the current personnel doesn't match the optimal one.

### 🏈 Suggesting Formations (Strategic Look)
While personnel defines *who* is on the field, **Formations** define *where* they stand.
*   **Offensive Formation (OC):** 
    *   *Mechanism:* The Offensive Model can be extended to suggest "Shotgun" vs. "Under Center" based on the `two_min_drill` or `ydstogo` features.
    *   *UI:* Displays a small icon next to the Play Card indicating the suggested formation.
*   **Defensive Formation (DC):**
    *   *Mechanism:* Predicted by the Defensive Model. If the predicted `is_pass_prob` is high, the system suggests moving from **Base** (4-3/3-4) to **Nickel** (5 DBs) or **Dime** (6 DBs).
    *   *UI:* The "Radar" view explicitly labels the recommendation: **"MATCH: NICKEL"**.

---

## 3. The "Radar" (Defensive Coordinator View)
**Goal:** Anticipating opponent moves to call the perfect defense.

### 🤖 Model: Defensive Coordinator
*   **What it Computes:** `is_pass_prob` (0-100%).
*   **When to Run:** Pre-snap, as the offense lines up.
*   **UI Mapping:**
    *   **Tendency Bar:** A visual slider showing "Run vs. Pass" likelihood.
    *   **High Alert:** If `is_pass_prob > 80%`, the screen flashes **"⚠️ PASS ALERT"**.
    *   **Formation Match:** Suggests "Nickel" vs. "Base" defense based on the predicted likelihood.

---

## Summary Table

| Model | Trigger Event | UI Component | Output Data |
| :--- | :--- | :--- | :--- |
| **4th Down** | 4th Down Situation | Head Coach "Traffic Light" | Recommendation (Go/Punt) |
| **Win Prob** | End of Play | Score Bug / Context | % Win Chance |
| **Offensive** | Start of Play Clock | OC "Play Menu" | Top 3 Play Types |
| **Defensive** | Pre-Snap | DC "Radar" | Run/Pass Tendency |
| **Personnel** | Substitution / Red Zone | OC/DC "Matchup Alert" | Grouping Code (e.g., "11") |
