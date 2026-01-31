# User Persona: Head Coach (HC)

**Role:** The Executive Decision Maker.
**Environment:** High-noise, high-stress sideline. Split-second decisions.
**UX Requirement:** **"The Traffic Light"** - Information must be absorbable in < 1 second. Big fonts, clear colors (Red/Green), minimal text.

## Core Use Cases

### 1. The "Go/No-Go" Signal (4th Down)
**Goal:** Instantly decide whether to keep the offense on the field.
- **Workflow:**
    1.  HC glances at the tablet as 3rd down ends.
    2.  **UI:** Screen is dominated by a single color/word:
        -   **GREEN / "GO"** (if conversion probability > threshold).
        -   **BLUE / "PUNT"**.
        -   **YELLOW / "KICK"**.
    3.  **Action:** HC yells "Stay on the field!" or signals the punt team immediately.
- **Simplicity Constraint:** No probabilities visible unless expanded. Just the decision.

### 2. Clock Strategy Check
**Goal:** Know exactly when to burn a timeout without doing mental math.
- **Workflow:**
    1.  Opponent gets a first down with 2 mins left.
    2.  **UI:** A flashing prompt: **"TAKE TIMEOUT"** vs. **"LET IT RUN"**.
    3.  **Action:** HC calls timeout immediately if prompted.

### 3. Challenge Assistant
**Goal:** Decide whether to throw the red flag.
- **Workflow:**
    1.  Questionable call on the field.
    2.  **UI:** Simple probability meter: **"WIN PROB: LOW" (Red)** or **"WIN PROB: HIGH" (Green)**.
    3.  **Action:** HC keeps the flag in pocket (Red) or throws it (Green).
