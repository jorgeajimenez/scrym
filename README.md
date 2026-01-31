# NFL AI Coach: The Playbook (4th Down Bot Demo) 🏈

**NFL AI Coach** is a data-driven decision support system designed for the **Gemini 3 SuperHack 2026**. This demo version focuses specifically on the **4th Down Bot**, a critical component that builds the foundation for the full AI coaching suite.

## 🚀 Demo Focus: The 4th Down Bot
The platform uses a multi-output neural network to analyze 4th down situations and recommend the optimal decision: **Go for it**, **Punt**, or **Field Goal**.

### Key Capabilities
1.  **Conversion Probability**: Calculates the likelihood of converting on 4th down.
2.  **Field Goal Probability**: Estimates the success rate of a field goal attempt from the current distance.
3.  **Expected Points (EPA)**: Compares the expected value of each decision to recommend the mathematically optimal choice.
4.  **Win Probability Integration**: Contextualizes decisions based on the current score and time remaining.

## 🛠 Tech Stack
-   **Frontend**: Next.js 15 (App Router, TypeScript, Tailwind CSS)
-   **Backend**: Python 3.11 (FastAPI, PyTorch, nfl_data_py)
-   **Data**: NFL Play-by-Play (PBP) via nflverse (2018-2024).
-   **Models**: PyTorch Feedforward Networks.

## 📂 Project Structure
-   `backend/`: FastAPI server and ML training logic (4th Down focused).
-   `frontend/`: Next.js web dashboard (4th Down Calculator).
-   `data/`: Local cache for NFL datasets.
-   `models/`: Serialized PyTorch models.

## 🏁 Quick Start (Development)
Detailed setup instructions will be provided as implementation progresses.
1.  **Backend**: Setup virtual environment, install requirements, and run the FastAPI server.
2.  **Frontend**: Install Node dependencies and start the Next.js dev server.

## 📜 Compliance
-   **Hackathon Track**: Statement One - The Playbook (Computational Sports).
-   **New Work Only**: All core logic is being re-implemented from scratch.
-   **Open Source**: This project is intended for open-source distribution.

---
Built for the **Gemini 3 SuperHack 2026**.
