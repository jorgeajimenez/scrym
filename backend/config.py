"""
Configuration Management for SCRYM Vision Agents
Loads environment variables and provides config access.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    # Stream API Credentials
    STREAM_API_KEY = os.getenv("STREAM_API_KEY", "9hp7cdp6dms7")
    STREAM_SECRET = os.getenv("STREAM_SECRET", "x27b5sv35qj9gjb6d563ujwvqrr4g4usccuzkahe4kcwzwrphcdhg7at43xatujq")

    # Optional: Future API keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

    # Vision Agent Mode
    USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"

    # WebSocket Settings
    WS_FPS = int(os.getenv("WS_FPS", "30"))  # 30 frames per second

    # File paths
    BASE_DIR = Path(__file__).parent.parent
    MODEL_DIR = BASE_DIR / "models"
    DATA_DIR = BASE_DIR / "data"

config = Config()
