# 🎬 Demo Guide: The "4th Down Bot" Experience

This script is designed to guide a presenter (or user) through the core capabilities of the application. It leverages the "Jump In" scenarios and "Auto-Sim" features defined in the `INTEGRATION_GUIDE.md`.

**Target Audience:** Hackathon Judges, Coaches, Fans.
**Goal:** Prove the AI provides "Context-Aware Intelligence" in real-time.

---

## 🎭 Scene 1: The "Gut Check" (Head Coach)
**Context:** It's the 4th Quarter. Tie Game. 4th & 2 on the Opponent's 45. The "No Man's Land".

1.  **Setup:** 
    *   Open the "Demo Scenarios" Drawer.
    *   Click **"Scenario: The Gut Check"**.
    *   *Result:* The dashboard loads. The Field View shows the ball at the 45. The Down Indicator shows "4th & 2".

2.  **The Action:**
    *   **User:** "We are in the classic 'Go or Punt' zone. Old school coaches punt here. Let's ask the bot."
    *   **Visual:** The "Traffic Light" component pulses "CALCULATING...".
    *   **The Reveal:** The light turns **GREEN**. Text slams: **"GO FOR IT"**.
    *   **Detail:** Hover over the decision. 
    *   **User:** "The AI sees a 58% conversion probability, adding +4.2% to our Win Probability. Punting only nets us 30 yards of field position. The math says GO."

---

## 🎭 Scene 2: The "Two-Minute Drill" (Offensive Coordinator)
**Context:** Down by 6. 1:50 remaining. Own 25 yard line. Need a Touchdown.

1.  **Setup:**
    *   Click **"Scenario: 2-Min Drill"**.
    *   *Result:* Clock set to 1:50. `two_min_drill` flag is active.

2.  **The Action:**
    *   **User:** "We need speed. The AI knows we are in 'Two Minute Mode'."
    *   **Visual:** The "Play Menu" shows 3 cards. The biggest one is **"PASS (Deep)"**.
    *   **Secondary Visual:** Next to the card, the Formation Icon shows **"Empty Set (5-Wide)"**.
    *   **User:** "See? It's not just calling 'Pass'. It's suggesting an 'Empty Set' formation to spread the defense and stop the clock. It knows the context."

3.  **Interaction:**
    *   Click the **"PASS"** card.
    *   *Result:* Simulation runs. "Incomplete. Clock stops at 1:45."
    *   **User:** "Incomplete. Clock stops. The AI immediately suggests the next play."

---

## 🎭 Scene 3: The "Mind Reader" (Defensive Coordinator)
**Context:** Opponent is driving. 3rd & Long.

1.  **Setup:**
    *   Toggle the **"View Mode"** switch from `[OFFENSE]` to `[DEFENSE]`.
    *   Click **"Scenario: 3rd & Long"**.

2.  **The Action:**
    *   **User:** "We are on defense. We need to know what's coming."
    *   **Visual:** The "Radar" gauge jitters nervously but swings hard to the right (PASS).
    *   **Alert:** A flashing badge appears: **"⚠️ NICKEL PACKAGE RECOMMENDED"**.
    *   **User:** "The AI detects a 92% pass probability. It automatically suggests swapping a Linebacker for a Defensive Back (Nickel Package) to match the speed."

---

## 🎭 Scene 4: "Ghost Mode" (Auto-Simulation)
**Context:** Let the AI play the game.

1.  **Setup:**
    *   Toggle the **[MANUAL | AUTO-SIM]** switch to **AUTO-SIM**.

2.  **The Action:**
    *   **User:** "I'm going to take my hands off the keyboard. Let's watch the AI coach itself."
    *   **Visual:** 
        1.  AI highlights "Run".
        2.  *Sim Step:* "Run for 4 yards." Clock ticks down.
        3.  AI highlights "Pass".
        4.  *Sim Step:* "Pass Complete for 12 yards (1st Down)."
        5.  **User:** "It manages the clock, calls the plays, and adjusts the formation. This is a closed-loop coaching system."

---

## 🏁 The Closing Statement

"This isn't just a stat sheet. It's a real-time decision engine that understands the flow of football, from the clock management to the formation alignment. Thank you."
