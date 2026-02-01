"""
Mock Player Tracking Data Generator
Simulates 22 NFL players moving on field with realistic physics.
Mimics YOLO output format for Vision Agents compatibility.
"""
import asyncio
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Dict
import time

@dataclass
class PlayerPosition:
    """Single player position snapshot (YOLO-compatible format)"""
    id: str              # Player identifier (e.g., "QB", "WR1", "DE")
    x: float             # Normalized X coordinate (0-1, left to right)
    y: float             # Normalized Y coordinate (0-1, top to bottom)
    vx: float            # Velocity X component (yards/sec)
    vy: float            # Velocity Y component (yards/sec)
    team: str            # "offense" or "defense"
    role: str            # Position (QB, RB, WR, etc.)
    orientation: float   # Direction facing (radians)

    def to_dict(self):
        return asdict(self)

class MockPlayerTracker:
    """
    Generates realistic player movements simulating:
    - Pre-snap alignment (static formation)
    - Snap animation (routes/rushes)
    - Post-play reset
    """

    def __init__(self):
        self.time_start = time.time()
        self.play_state = "pre_snap"  # pre_snap, in_play, post_play
        self.play_clock = 0.0

        # Initial formations
        self.offense_formation = self._init_offense_shotgun()
        self.defense_formation = self._init_defense_base_43()

    def _init_offense_shotgun(self) -> List[PlayerPosition]:
        """Initialize offense in shotgun formation"""
        return [
            PlayerPosition("QB", 0.5, 0.7, 0, 0, "offense", "QB", -np.pi/2),
            PlayerPosition("RB", 0.6, 0.7, 0, 0, "offense", "RB", -np.pi/2),
            # O-Line
            PlayerPosition("LT", 0.35, 0.6, 0, 0, "offense", "OL", -np.pi/2),
            PlayerPosition("LG", 0.42, 0.6, 0, 0, "offense", "OL", -np.pi/2),
            PlayerPosition("C", 0.5, 0.6, 0, 0, "offense", "OL", -np.pi/2),
            PlayerPosition("RG", 0.58, 0.6, 0, 0, "offense", "OL", -np.pi/2),
            PlayerPosition("RT", 0.65, 0.6, 0, 0, "offense", "OL", -np.pi/2),
            # Receivers
            PlayerPosition("WR1", 0.1, 0.58, 0, 0, "offense", "WR", -np.pi/2),
            PlayerPosition("WR2", 0.9, 0.58, 0, 0, "offense", "WR", -np.pi/2),
            PlayerPosition("WR3", 0.2, 0.58, 0, 0, "offense", "WR", -np.pi/2),
            PlayerPosition("TE", 0.7, 0.6, 0, 0, "offense", "TE", -np.pi/2),
        ]

    def _init_defense_base_43(self) -> List[PlayerPosition]:
        """Initialize defense in 4-3 base"""
        return [
            # D-Line
            PlayerPosition("DE1", 0.35, 0.5, 0, 0, "defense", "DE", np.pi/2),
            PlayerPosition("DT1", 0.45, 0.5, 0, 0, "defense", "DT", np.pi/2),
            PlayerPosition("DT2", 0.55, 0.5, 0, 0, "defense", "DT", np.pi/2),
            PlayerPosition("DE2", 0.65, 0.5, 0, 0, "defense", "DE", np.pi/2),
            # Linebackers
            PlayerPosition("LB1", 0.35, 0.4, 0, 0, "defense", "LB", np.pi/2),
            PlayerPosition("MLB", 0.5, 0.4, 0, 0, "defense", "MLB", np.pi/2),
            PlayerPosition("LB2", 0.65, 0.4, 0, 0, "defense", "LB", np.pi/2),
            # Secondary
            PlayerPosition("CB1", 0.15, 0.45, 0, 0, "defense", "CB", np.pi/2),
            PlayerPosition("CB2", 0.85, 0.45, 0, 0, "defense", "CB", np.pi/2),
            PlayerPosition("FS", 0.5, 0.25, 0, 0, "defense", "S", np.pi/2),
            PlayerPosition("SS", 0.6, 0.3, 0, 0, "defense", "S", np.pi/2),
        ]

    def update(self, dt: float) -> List[PlayerPosition]:
        """
        Update all player positions based on play state
        dt: Delta time since last update (seconds)
        """
        self.play_clock += dt

        # State machine: Cycle through play phases
        if self.play_state == "pre_snap":
            # Idle breathing motion
            self._apply_idle_motion(dt)

            # Snap ball after 3 seconds
            if self.play_clock > 3.0:
                self.play_state = "in_play"
                self.play_clock = 0.0

        elif self.play_state == "in_play":
            # Execute play animation
            self._simulate_play_motion(dt)

            # Play ends after 5 seconds
            if self.play_clock > 5.0:
                self.play_state = "post_play"
                self.play_clock = 0.0

        elif self.play_state == "post_play":
            # Slow down and reset
            self._reset_formation(dt)

            # Return to pre-snap
            if self.play_clock > 2.0:
                self.play_state = "pre_snap"
                self.play_clock = 0.0

        return self.offense_formation + self.defense_formation

    def _apply_idle_motion(self, dt: float):
        """Small random movements (breathing)"""
        for player in self.offense_formation + self.defense_formation:
            player.x += (np.random.random() - 0.5) * 0.0002
            player.y += (np.random.random() - 0.5) * 0.0002
            player.vx = 0
            player.vy = 0

    def _simulate_play_motion(self, dt: float):
        """Execute play routes/rushes with boundary constraints"""
        for player in self.offense_formation:
            if player.role == "QB":
                # QB drops back (constrained)
                player.y = min(0.85, player.y + 0.001)
                player.vy = 1.5
            elif player.role == "WR":
                # WRs run routes (constrained)
                player.y = max(0.2, player.y - 0.002)
                player.vy = -5.0
            elif player.role == "RB":
                # RB motion (constrained)
                player.x = max(0.1, min(0.9, player.x + 0.001))
                player.y = max(0.3, player.y - 0.001)
                player.vx = 2.0
                player.vy = -3.0
            # Keep OL stationary
            elif player.role == "OL":
                player.vx = 0
                player.vy = 0

        for player in self.defense_formation:
            if player.role in ["DE", "DT"]:
                # D-line rushes QB (constrained)
                player.y = min(0.75, player.y + 0.002)
                player.vy = 4.0
            elif player.role == "CB":
                # CBs follow WRs (constrained)
                player.y = max(0.25, player.y - 0.002)
                player.vy = -4.5
            elif player.role in ["LB", "MLB"]:
                # LBs read and react (constrained)
                player.y = min(0.65, player.y + 0.001)
                player.vy = 2.0
            elif player.role == "S":
                # Safeties stay deep
                player.vy = 0

    def _reset_formation(self, dt: float):
        """Return players to original positions"""
        # Reinitialize formations
        self.offense_formation = self._init_offense_shotgun()
        self.defense_formation = self._init_defense_base_43()

    def get_frame_data(self) -> Dict:
        """Get current frame in Vision Agent format"""
        players = self.update(1/30)  # 30fps update

        return {
            "timestamp": time.time(),
            "frame_id": int(self.play_clock * 30),
            "play_state": self.play_state,
            "players": [p.to_dict() for p in players],
            "confidence": 0.95,  # Mock confidence score
            "source": "mock_tracker"
        }

# Global tracker instance
_tracker = MockPlayerTracker()

async def generate_mock_stream():
    """Async generator for streaming mock data"""
    while True:
        yield _tracker.get_frame_data()
        await asyncio.sleep(1/30)  # 30fps
