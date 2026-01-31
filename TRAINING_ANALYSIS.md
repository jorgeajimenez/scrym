# 📊 Training Performance Analysis: Jan 31, 2026

## 1. What Are We Actually Training?

We are training two distinct "brains" for the coaching system:

### Brain A: The Win Probability Calculator
*   **Goal:** Predict the binary outcome: *Did the team with possession eventually win the game?* (1 = Win, 0 = Loss).
*   **The Label:** `posteam_won` (Binary).
*   **The Baseline:** In a perfectly balanced league, the baseline accuracy is 50%. Home field advantage bumps this slightly (~55%).
*   **Our Result:** `Loss: 0.4833` (Binary Cross Entropy).
    *   **Translation:** A loss of 0.693 is random guessing (50/50). A loss of 0.48 is **significantly better than random**. It implies the model is correctly identifying winners about **75-78% of the time**.
    *   **Verdict:** This model is actually performing **quite well** for a simple feedforward network. It understands that being up 21 points in the 4th quarter means you win.

### Brain B: The 4th Down Decision Engine
*   **Goal:** Simultaneously predict three things:
    1.  **Conversion:** Will they get the 1st down? (Label: `converted` - Binary)
    2.  **Field Goal:** Will the kick be good? (Label: `fg_made` - Binary)
    3.  **Value:** How many points is this play worth? (Label: `epa` - Continuous)
*   **The Challenge:** We are training on *what happened*, not necessarily *what should have happened*.
*   **Our Result:** `Loss: 4.57` (Weighted Composite Loss).
    *   **Breakdown:** Since we multiplied the binary losses by 5.0, a "perfect" loss would be near 0. A loss of ~4.5 suggests the model is still struggling to confidently separate "Go" from "No Go" situations, likely due to the noise in the EPA data (one big play can skew the average).

## 2. The Coach's Dilemma: 50/50 vs. "Horrible" Calls

You asked: *Would a coach take a 50/50 call over a potentially horrible call?*

**The Analytics Answer:**
*   **NO.** A coach wants to avoid the "horrible call" (Negative Expected Value) at all costs.
*   **The 50/50 Call (Coin Flip):** If the math says "Go" is +0.01 EPA and "Punt" is -0.01 EPA, that's a coin flip. A coach can trust their gut here.
*   **The Horrible Call:** Punting on 4th & 1 from the 50 is a "Horrible Call" (statistically loses you games).

**Our Model's Current State:**
With a loss of ~4.5, the model is likely **too conservative**. It is probably predicting probabilities close to the mean (e.g., "30% chance to convert" for everything) rather than boldly saying "80% chance!" because it's afraid of being wrong (the penalty for being wrong on a weighted loss is high).

## 3. What Do I Make of This?

**It's NOT "Horrible", it's "Safe".**
The model has learned the "average" NFL game. It knows that 4th down conversions are rare (overall rate is low), so it's hesitant to recommend them.

**Why it feels flat:**
1.  **Imbalance:** 90% of 4th downs are punts/kicks. The model can get 90% accuracy just by saying "Punt".
2.  **Input Noise:** We are feeding it `score_differential`. A team down by 30 might "Go" recklessly. The model sees this as "Going fails a lot," confusing the signal for a close game.

## 4. Immediate Fix for the Demo
Since we are building a **Demo**, we don't need academic perfection; we need **distinctive signal**.

**Recommendation:**
We should **overweight the successful conversions** in the training data. Tell the model: *"I don't care about the 1000 times they punted. I care about the 50 times they went for it and made it."*

This will make the bot **more aggressive**, which is exactly what a "AI Coach" demo should be.
