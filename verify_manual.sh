#!/bin/bash

# Ensure we have the virtual environment activated
# source venv/bin/activate

echo "=================================================="
echo "      NFL AI COACH - MANUAL VERIFICATION"
echo "=================================================="

echo -e "\nScenario 1: THE AGGRESSIVE GO"
echo "4th & 1 on Opponent 45 | Tie Game | 3rd Quarter"
echo "Expectation: High Conversion Prob (>60%), Recommendation: GO"
echo "--------------------------------------------------"
python backend/verify_inference.py \
  --down 4 \
  --togo 1 \
  --ydline 45 \
  --score_diff 0 \
  --qtr 3 \
  --time_rem 900 \
  --to_pos 3 \
  --to_def 3

echo -e "\n\nScenario 2: THE OBVIOUS PUNT"
echo "4th & 10 on Own 20 | Up by 3 | 4th Quarter"
echo "Expectation: Low Conversion Prob, Recommendation: KICK/PUNT"
echo "--------------------------------------------------"
python backend/verify_inference.py \
  --down 4 \
  --togo 10 \
  --ydline 80 \
  --score_diff 3 \
  --qtr 4 \
  --time_rem 300 \
  --to_pos 2 \
  --to_def 2

echo -e "\n\nScenario 3: FIELD GOAL RANGE"
echo "4th & 5 on Opponent 25 | Down by 1 | Last Play"
echo "Expectation: High FG Prob, Recommendation: KICK/PUNT (FG)"
echo "--------------------------------------------------"
python backend/verify_inference.py \
  --down 4 \
  --togo 5 \
  --ydline 25 \
  --score_diff -1 \
  --qtr 4 \
  --time_rem 4 \
  --to_pos 0 \
  --to_def 0
