# Formation Visualization & Customization Feature - Architecture Design

## NFL Terminology Clarification

**Official NFL Lingo:**
- **Personnel Package/Grouping**: Player composition (e.g., "11 personnel" = 1 RB, 1 TE, 3 WR)
- **Formation**: Player alignment on field (e.g., "Shotgun", "I-Formation", "Bunch")
- **Alignment**: Specific positioning (e.g., "Trips Right", "Split Backs")
- **Motion**: Pre-snap player movement
- **Play**: The actual play design with routes/assignments

**Offensive Personnel Codes:**
- `11`: 1 RB, 1 TE, 3 WR (most common passing)
- `12`: 1 RB, 2 TE, 2 WR (balanced)
- `13`: 1 RB, 3 TE, 1 WR (heavy/goal line)
- `21`: 2 RB, 1 TE, 2 WR (power running)
- `22`: 2 RB, 2 TE, 1 WR (heavy running)
- `10`: 1 RB, 0 TE, 4 WR (spread/empty)
- `01`: 0 RB, 1 TE, 4 WR (empty/passing)
- `00`: 0 RB, 0 TE, 5 WR (5-wide)

**Defensive Personnel:**
- **Base**: 4-3 (4 DL, 3 LB, 4 DB) or 3-4 (3 DL, 4 LB, 4 DB)
- **Nickel**: 5 DBs (extra CB)
- **Dime**: 6 DBs (2 extra DBs)
- **Quarter**: 7 DBs (rare)

---

## Feature Requirements

### Core Capabilities
1. **Visualize** current/recommended formations on interactive field
2. **Customize** player positions with drag-and-drop
3. **Simulate** formation effectiveness using ML models
4. **Approve** formations and save to playbook
5. **Compare** multiple formations side-by-side
6. **Integrate** with Personnel Optimizer ML model

---

## System Architecture

### 1. Data Models

```python
# backend/models/formation_models.py

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Literal
from enum import Enum

# ==================== Enums ====================

class PositionType(str, Enum):
    """Official NFL position abbreviations"""
    # Offense
    QB = "QB"   # Quarterback
    RB = "RB"   # Running Back
    FB = "FB"   # Fullback
    WR = "WR"   # Wide Receiver
    TE = "TE"   # Tight End
    LT = "LT"   # Left Tackle
    LG = "LG"   # Left Guard
    C = "C"     # Center
    RG = "RG"   # Right Guard
    RT = "RT"   # Right Tackle

    # Defense
    DE = "DE"   # Defensive End
    DT = "DT"   # Defensive Tackle
    NT = "NT"   # Nose Tackle
    OLB = "OLB" # Outside Linebacker
    MLB = "MLB" # Middle Linebacker
    ILB = "ILB" # Inside Linebacker
    CB = "CB"   # Cornerback
    FS = "FS"   # Free Safety
    SS = "SS"   # Strong Safety

class PersonnelPackage(str, Enum):
    """Standard offensive personnel groupings"""
    PERSONNEL_11 = "11"  # 1 RB, 1 TE, 3 WR
    PERSONNEL_12 = "12"  # 1 RB, 2 TE, 2 WR
    PERSONNEL_13 = "13"  # 1 RB, 3 TE, 1 WR
    PERSONNEL_21 = "21"  # 2 RB, 1 TE, 2 WR
    PERSONNEL_22 = "22"  # 2 RB, 2 TE, 1 WR
    PERSONNEL_10 = "10"  # 1 RB, 0 TE, 4 WR
    PERSONNEL_01 = "01"  # 0 RB, 1 TE, 4 WR (Empty)
    PERSONNEL_00 = "00"  # 0 RB, 0 TE, 5 WR (5-wide)

class FormationType(str, Enum):
    """Standard offensive formations"""
    SHOTGUN = "Shotgun"
    PISTOL = "Pistol"
    SINGLEBACK = "Singleback"
    I_FORMATION = "I-Formation"
    WILDCAT = "Wildcat"
    EMPTY = "Empty"
    BUNCH = "Bunch"
    TRIPS = "Trips"
    SPREAD = "Spread"

class DefensiveFront(str, Enum):
    """Defensive fronts"""
    BASE_43 = "4-3"
    BASE_34 = "3-4"
    NICKEL = "Nickel"
    DIME = "Dime"
    QUARTER = "Quarter"

# ==================== Core Models ====================

class FieldPosition(BaseModel):
    """Position on field (coordinates)"""
    x: float = Field(..., ge=0, le=53.33, description="Lateral position (yards, 0=left sideline, 53.33=right)")
    y: float = Field(..., ge=0, le=120, description="Longitudinal position (yards from own endzone)")

    class Config:
        schema_extra = {
            "example": {"x": 26.67, "y": 50.0}  # Center of field at 50-yard line
        }

class PlayerOnField(BaseModel):
    """Individual player in formation"""
    player_id: Optional[str] = Field(None, description="Unique player identifier from roster")
    player_name: str = Field(..., description="Player name")
    position: PositionType = Field(..., description="Player position")
    jersey_number: int = Field(..., ge=0, le=99)
    field_position: FieldPosition = Field(..., description="Position on field")
    alignment: Optional[str] = Field(None, description="Alignment detail (e.g., 'Wide Left', 'Slot Right')")
    depth: Optional[float] = Field(None, description="Depth from line of scrimmage (yards)")

    class Config:
        schema_extra = {
            "example": {
                "player_id": "P123456",
                "player_name": "Patrick Mahomes",
                "position": "QB",
                "jersey_number": 15,
                "field_position": {"x": 26.67, "y": 55.0},
                "alignment": "Shotgun",
                "depth": 5.0
            }
        }

class Formation(BaseModel):
    """Complete formation configuration"""
    formation_id: Optional[str] = Field(None, description="Unique formation identifier")
    name: str = Field(..., description="Formation name (e.g., 'Shotgun Trips Right')")
    personnel_package: PersonnelPackage = Field(..., description="Personnel grouping")
    formation_type: FormationType = Field(..., description="Base formation type")
    hash_mark: Literal["left", "middle", "right"] = Field("middle", description="Ball position")
    yard_line: int = Field(..., ge=1, le=99, description="Yard line (distance from opponent goal)")

    offensive_players: List[PlayerOnField] = Field(..., min_items=11, max_items=11)

    # Optional metadata
    down: Optional[int] = Field(None, ge=1, le=4)
    distance: Optional[int] = Field(None, ge=1, le=99)
    game_situation: Optional[str] = Field(None, description="e.g., 'Red Zone', '2-Minute Drill'")

    # AI-generated metrics
    predicted_success_rate: Optional[float] = Field(None, ge=0, le=1)
    recommended_plays: Optional[List[str]] = Field(None)
    defensive_vulnerability: Optional[str] = Field(None)

    @validator('offensive_players')
    def validate_personnel_count(cls, players, values):
        """Validate player count matches personnel package"""
        if 'personnel_package' not in values:
            return players

        package = values['personnel_package']

        # Count skill positions
        rb_count = sum(1 for p in players if p.position == PositionType.RB or p.position == PositionType.FB)
        te_count = sum(1 for p in players if p.position == PositionType.TE)
        wr_count = sum(1 for p in players if p.position == PositionType.WR)

        # Expected counts based on package
        package_map = {
            "11": (1, 1, 3),
            "12": (1, 2, 2),
            "13": (1, 3, 1),
            "21": (2, 1, 2),
            "22": (2, 2, 1),
            "10": (1, 0, 4),
            "01": (0, 1, 4),
            "00": (0, 0, 5)
        }

        expected = package_map.get(package.value)
        if expected:
            exp_rb, exp_te, exp_wr = expected
            if rb_count != exp_rb or te_count != exp_te or wr_count != exp_wr:
                raise ValueError(
                    f"Personnel package {package} requires {exp_rb} RB, {exp_te} TE, {exp_wr} WR. "
                    f"Got {rb_count} RB, {te_count} TE, {wr_count} WR"
                )

        return players

class FormationSimulationRequest(BaseModel):
    """Request for formation simulation"""
    formation: Formation
    opponent_defense: Optional[DefensiveFront] = Field(None, description="Expected defensive front")
    game_context: Optional[Dict] = Field(None, description="Score, time, field position context")
    play_type: Optional[Literal["run", "pass", "play_action"]] = Field(None)

class FormationSimulationResult(BaseModel):
    """Results from formation simulation"""
    formation_id: str
    personnel_match_score: float = Field(..., ge=0, le=1, description="How well personnel fits situation")
    expected_epa: float = Field(..., description="Expected points added")
    success_probability: float = Field(..., ge=0, le=1)

    # Breakdown by play type
    run_efficiency: float = Field(..., ge=0, le=1)
    pass_efficiency: float = Field(..., ge=0, le=1)

    # Recommendations
    optimal_play_types: List[str]
    defensive_weakness: str
    adjustments_recommended: List[str]

    # Visual heatmap data (for frontend)
    blocking_strength_zones: Optional[Dict[str, float]] = Field(None)
    receiving_threat_zones: Optional[Dict[str, float]] = Field(None)

class Playbook(BaseModel):
    """Collection of saved formations"""
    playbook_id: str
    team_name: str
    formations: List[Formation]
    created_at: str
    updated_at: str
    tags: List[str] = Field(default_factory=list)
```

---

## 2. Backend API Design

```python
# backend/formation_api.py

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/formations", tags=["formations"])

# ==================== Endpoints ====================

@router.post("/create", response_model=Formation)
async def create_formation(formation: Formation):
    """
    Create a new formation

    - Validates personnel package matches player count
    - Assigns unique formation_id
    - Returns formation with metadata
    """
    if not formation.formation_id:
        formation.formation_id = f"FORM-{uuid.uuid4().hex[:8]}"

    # TODO: Save to database

    return formation


@router.post("/simulate", response_model=FormationSimulationResult)
async def simulate_formation(request: FormationSimulationRequest):
    """
    Simulate formation effectiveness using ML models

    - Uses Personnel Optimizer to validate personnel choice
    - Uses Offensive Play-Caller to predict optimal plays
    - Uses Defensive Coordinator to identify defensive response
    - Returns comprehensive simulation results
    """
    formation = request.formation

    # Extract game context
    game_state = {
        'down': formation.down or 1,
        'distance': formation.distance or 10,
        'yard_line': formation.yard_line,
        'personnel': formation.personnel_package.value
    }

    # Call ML models (integrate with existing models)
    personnel_score = await evaluate_personnel_choice(game_state)
    play_predictions = await predict_optimal_plays(game_state, formation)
    defensive_response = await predict_defensive_alignment(game_state, formation)

    # Calculate efficiency metrics
    run_eff, pass_eff = calculate_formation_efficiency(formation, play_predictions)

    result = FormationSimulationResult(
        formation_id=formation.formation_id,
        personnel_match_score=personnel_score,
        expected_epa=play_predictions.get('expected_epa', 0.0),
        success_probability=play_predictions.get('success_prob', 0.5),
        run_efficiency=run_eff,
        pass_efficiency=pass_eff,
        optimal_play_types=play_predictions.get('recommended_plays', []),
        defensive_weakness=defensive_response.get('weakness', 'Unknown'),
        adjustments_recommended=generate_adjustments(formation, defensive_response)
    )

    return result


@router.get("/templates", response_model=List[Formation])
async def get_formation_templates(
    personnel: Optional[PersonnelPackage] = None,
    formation_type: Optional[FormationType] = None
):
    """
    Get pre-built formation templates

    - Returns standard NFL formations
    - Can filter by personnel package or formation type
    - Includes recommended use cases
    """
    templates = load_formation_templates()

    if personnel:
        templates = [f for f in templates if f.personnel_package == personnel]

    if formation_type:
        templates = [f for f in templates if f.formation_type == formation_type]

    return templates


@router.post("/validate", response_model=Dict[str, Any])
async def validate_formation(formation: Formation):
    """
    Validate formation for rule compliance

    Checks:
    - 11 players on field
    - Personnel package matches actual positions
    - Minimum 7 players on line of scrimmage
    - Eligible receivers properly aligned
    - No illegal formations
    """
    validation_errors = []

    # Check player count
    if len(formation.offensive_players) != 11:
        validation_errors.append(f"Must have exactly 11 players (found {len(formation.offensive_players)})")

    # Check line of scrimmage (7 players within 1 yard)
    los_players = [p for p in formation.offensive_players
                   if p.field_position.y <= formation.yard_line + 1]
    if len(los_players) < 7:
        validation_errors.append(f"Must have at least 7 players on line of scrimmage (found {len(los_players)})")

    # Check for eligible receivers
    # In NFL, ends on line and all backs are eligible
    # Interior linemen must be numbered 50-79 and cannot be eligible

    return {
        "valid": len(validation_errors) == 0,
        "errors": validation_errors,
        "warnings": generate_formation_warnings(formation)
    }


@router.post("/compare", response_model=Dict[str, Any])
async def compare_formations(formations: List[Formation], game_context: Dict):
    """
    Compare multiple formations side-by-side

    - Simulates each formation in same game context
    - Returns comparison metrics
    - Recommends best formation for situation
    """
    results = []

    for formation in formations:
        sim_request = FormationSimulationRequest(
            formation=formation,
            game_context=game_context
        )
        sim_result = await simulate_formation(sim_request)
        results.append({
            "formation": formation,
            "simulation": sim_result
        })

    # Rank formations
    ranked = sorted(results,
                   key=lambda x: x['simulation'].expected_epa,
                   reverse=True)

    return {
        "formations_compared": len(formations),
        "best_formation": ranked[0]['formation'].name,
        "comparison": ranked,
        "recommendation": generate_formation_recommendation(ranked, game_context)
    }


@router.post("/playbook/save")
async def save_to_playbook(playbook_id: str, formation: Formation):
    """Save formation to team playbook"""
    # TODO: Database operation
    return {"message": f"Formation '{formation.name}' saved to playbook {playbook_id}"}


@router.get("/playbook/{playbook_id}", response_model=Playbook)
async def get_playbook(playbook_id: str):
    """Retrieve team playbook with all formations"""
    # TODO: Database query
    pass


@router.post("/auto-generate")
async def auto_generate_formation(
    personnel: PersonnelPackage,
    game_situation: Dict,
    opponent_defense: Optional[DefensiveFront] = None
):
    """
    AI-generated formation based on game situation

    - Uses ML models to determine optimal personnel
    - Generates player positions optimized for situation
    - Returns formation with confidence scores
    """
    # Use Personnel Optimizer model
    recommended_personnel = await get_ml_personnel_recommendation(game_situation)

    # Generate formation based on personnel and situation
    formation = generate_optimal_formation(
        personnel=personnel or recommended_personnel,
        situation=game_situation,
        opponent=opponent_defense
    )

    return {
        "formation": formation,
        "confidence": 0.85,
        "reasoning": generate_formation_reasoning(formation, game_situation)
    }


# ==================== Helper Functions ====================

async def evaluate_personnel_choice(game_state: Dict) -> float:
    """Use Personnel Optimizer ML model"""
    # TODO: Integrate with existing personnel_model
    # Features: down, ydstogo, yardline_100, score_differential, red_zone, goal_to_go
    return 0.82  # Placeholder

async def predict_optimal_plays(game_state: Dict, formation: Formation) -> Dict:
    """Use Offensive Play-Caller ML model"""
    # TODO: Integrate with existing offensive_model
    return {
        "expected_epa": 0.25,
        "success_prob": 0.68,
        "recommended_plays": ["Inside Zone", "RPO Slant", "Play Action Boot"]
    }

async def predict_defensive_alignment(game_state: Dict, formation: Formation) -> Dict:
    """Use Defensive Coordinator ML model"""
    # TODO: Integrate with existing defensive_model
    return {
        "predicted_front": "Nickel",
        "pass_prob": 0.72,
        "weakness": "Weak against outside zone runs"
    }

def calculate_formation_efficiency(formation: Formation, predictions: Dict) -> tuple:
    """Calculate run/pass efficiency scores"""
    # Analyze formation structure
    rb_count = sum(1 for p in formation.offensive_players if p.position in [PositionType.RB, PositionType.FB])
    te_count = sum(1 for p in formation.offensive_players if p.position == PositionType.TE)
    wr_count = sum(1 for p in formation.offensive_players if p.position == PositionType.WR)

    # Heuristic: More RBs/TEs = better run, More WRs = better pass
    run_efficiency = (rb_count * 0.3 + te_count * 0.2 + 0.3)
    pass_efficiency = (wr_count * 0.15 + te_count * 0.1 + 0.4)

    return min(run_efficiency, 1.0), min(pass_efficiency, 1.0)

def generate_adjustments(formation: Formation, defensive_response: Dict) -> List[str]:
    """Suggest formation adjustments"""
    adjustments = []

    if defensive_response.get('pass_prob', 0) > 0.7:
        adjustments.append("Consider adding max protect (6-man protection)")
        adjustments.append("Use quick game/hot routes vs blitz")

    if "3-4" in defensive_response.get('predicted_front', ''):
        adjustments.append("Target A-gaps with inside zone")

    return adjustments

def generate_formation_warnings(formation: Formation) -> List[str]:
    """Generate coaching warnings"""
    warnings = []

    # Check for mismatches
    if formation.personnel_package == PersonnelPackage.PERSONNEL_11:
        if formation.yard_line <= 5:
            warnings.append("11 personnel at goal line: Consider heavier package (13/21)")

    return warnings
```

---

## 3. Frontend Components (React/Next.js)

```typescript
// frontend/components/FormationEditor.tsx

import React, { useState, useCallback } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

interface FieldPosition {
  x: number;  // 0-53.33 yards
  y: number;  // 0-120 yards
}

interface PlayerOnField {
  player_id: string;
  player_name: string;
  position: string;
  jersey_number: number;
  field_position: FieldPosition;
}

interface Formation {
  formation_id?: string;
  name: string;
  personnel_package: string;
  formation_type: string;
  yard_line: number;
  offensive_players: PlayerOnField[];
}

// ==================== Field Visualization Component ====================

const FootballField: React.FC<{
  formation: Formation;
  onPlayerMove: (playerId: string, newPosition: FieldPosition) => void;
  editMode: boolean;
}> = ({ formation, onPlayerMove, editMode }) => {

  const FIELD_WIDTH = 53.33;  // yards
  const SCALE = 10;  // pixels per yard

  return (
    <div className="football-field" style={{
      width: `${FIELD_WIDTH * SCALE}px`,
      height: `${40 * SCALE}px`,  // Show 40 yards
      backgroundImage: 'url(/field-texture.png)',
      position: 'relative',
      border: '2px solid #228B22'
    }}>
      {/* Yard lines */}
      {Array.from({ length: 40 }, (_, i) => (
        <div key={i} style={{
          position: 'absolute',
          top: `${i * SCALE}px`,
          left: 0,
          width: '100%',
          height: '1px',
          backgroundColor: i % 5 === 0 ? '#fff' : '#ddd',
          opacity: 0.5
        }} />
      ))}

      {/* Hash marks */}
      <div className="hash-marks left" style={{
        position: 'absolute',
        left: `${18.5 * SCALE}px`,
        height: '100%',
        borderLeft: '2px dashed #fff'
      }} />
      <div className="hash-marks right" style={{
        position: 'absolute',
        right: `${18.5 * SCALE}px`,
        height: '100%',
        borderLeft: '2px dashed #fff'
      }} />

      {/* Line of scrimmage */}
      <div className="line-of-scrimmage" style={{
        position: 'absolute',
        top: `${formation.yard_line * SCALE}px`,
        left: 0,
        width: '100%',
        height: '3px',
        backgroundColor: '#FFD700'
      }} />

      {/* Players */}
      {formation.offensive_players.map(player => (
        <DraggablePlayer
          key={player.player_id}
          player={player}
          scale={SCALE}
          editMode={editMode}
          onMove={(newPos) => onPlayerMove(player.player_id, newPos)}
        />
      ))}
    </div>
  );
};

// ==================== Draggable Player Component ====================

const DraggablePlayer: React.FC<{
  player: PlayerOnField;
  scale: number;
  editMode: boolean;
  onMove: (pos: FieldPosition) => void;
}> = ({ player, scale, editMode, onMove }) => {

  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'player',
    item: { player },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
    canDrag: editMode,
  }));

  const positionColors = {
    QB: '#FF0000',
    RB: '#00FF00',
    FB: '#00AA00',
    WR: '#0000FF',
    TE: '#FF00FF',
    LT: '#FFA500',
    LG: '#FFA500',
    C: '#FFA500',
    RG: '#FFA500',
    RT: '#FFA500',
  };

  return (
    <div
      ref={drag}
      style={{
        position: 'absolute',
        left: `${player.field_position.x * scale}px`,
        top: `${player.field_position.y * scale}px`,
        width: '30px',
        height: '30px',
        borderRadius: '50%',
        backgroundColor: positionColors[player.position] || '#888',
        border: '2px solid white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontWeight: 'bold',
        fontSize: '10px',
        cursor: editMode ? 'move' : 'default',
        opacity: isDragging ? 0.5 : 1,
        transform: 'translate(-50%, -50%)',
        zIndex: 10
      }}
      title={`${player.player_name} (${player.position})`}
    >
      {player.position}
    </div>
  );
};

// ==================== Main Formation Editor ====================

export const FormationEditor: React.FC = () => {
  const [formation, setFormation] = useState<Formation | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [simulationResults, setSimulationResults] = useState(null);

  const handlePlayerMove = useCallback((playerId: string, newPosition: FieldPosition) => {
    if (!formation) return;

    setFormation({
      ...formation,
      offensive_players: formation.offensive_players.map(p =>
        p.player_id === playerId
          ? { ...p, field_position: newPosition }
          : p
      )
    });
  }, [formation]);

  const handleSimulate = async () => {
    if (!formation) return;

    const response = await fetch('/api/formations/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        formation,
        game_context: {
          down: formation.down,
          distance: formation.distance,
          yard_line: formation.yard_line
        }
      })
    });

    const results = await response.json();
    setSimulationResults(results);
  };

  const handleApprove = async () => {
    if (!formation) return;

    await fetch('/api/formations/playbook/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        playbook_id: 'default',
        formation
      })
    });

    alert(`Formation "${formation.name}" saved to playbook!`);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="formation-editor">
        <div className="toolbar">
          <button onClick={() => setEditMode(!editMode)}>
            {editMode ? 'View Mode' : 'Edit Mode'}
          </button>
          <button onClick={handleSimulate}>Simulate</button>
          <button onClick={handleApprove} disabled={!simulationResults}>
            Approve & Save
          </button>
        </div>

        {formation && (
          <FootballField
            formation={formation}
            onPlayerMove={handlePlayerMove}
            editMode={editMode}
          />
        )}

        {simulationResults && (
          <SimulationResults results={simulationResults} />
        )}
      </div>
    </DndProvider>
  );
};

// ==================== Simulation Results Display ====================

const SimulationResults: React.FC<{ results: any }> = ({ results }) => {
  return (
    <div className="simulation-results">
      <h3>Formation Analysis</h3>

      <div className="metric">
        <label>Personnel Match Score:</label>
        <ProgressBar value={results.personnel_match_score} />
      </div>

      <div className="metric">
        <label>Expected EPA:</label>
        <span className={results.expected_epa > 0 ? 'positive' : 'negative'}>
          {results.expected_epa.toFixed(2)}
        </span>
      </div>

      <div className="metric">
        <label>Success Probability:</label>
        <ProgressBar value={results.success_probability} />
      </div>

      <div className="efficiency">
        <div>Run Efficiency: {(results.run_efficiency * 100).toFixed(0)}%</div>
        <div>Pass Efficiency: {(results.pass_efficiency * 100).toFixed(0)}%</div>
      </div>

      <div className="recommendations">
        <h4>Optimal Play Types:</h4>
        <ul>
          {results.optimal_play_types.map((play, i) => (
            <li key={i}>{play}</li>
          ))}
        </ul>
      </div>

      <div className="defensive-analysis">
        <h4>Defensive Weakness:</h4>
        <p>{results.defensive_weakness}</p>
      </div>

      {results.adjustments_recommended.length > 0 && (
        <div className="adjustments">
          <h4>Suggested Adjustments:</h4>
          <ul>
            {results.adjustments_recommended.map((adj, i) => (
              <li key={i}>{adj}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

const ProgressBar: React.FC<{ value: number }> = ({ value }) => {
  const percentage = Math.round(value * 100);
  const color = value > 0.7 ? '#4CAF50' : value > 0.4 ? '#FF9800' : '#F44336';

  return (
    <div style={{
      width: '200px',
      height: '20px',
      backgroundColor: '#eee',
      borderRadius: '10px',
      overflow: 'hidden'
    }}>
      <div style={{
        width: `${percentage}%`,
        height: '100%',
        backgroundColor: color,
        transition: 'width 0.3s ease'
      }}>
        <span style={{ marginLeft: '10px', color: 'white', fontSize: '12px' }}>
          {percentage}%
        </span>
      </div>
    </div>
  );
};
```

---

## 4. Database Schema

```sql
-- formations.sql

CREATE TABLE formations (
    formation_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    personnel_package VARCHAR(2) NOT NULL,
    formation_type VARCHAR(50) NOT NULL,
    hash_mark VARCHAR(10) DEFAULT 'middle',
    yard_line INT NOT NULL,
    down INT,
    distance INT,
    game_situation VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(100),

    -- ML predictions
    predicted_success_rate DECIMAL(5,4),

    INDEX idx_personnel (personnel_package),
    INDEX idx_formation_type (formation_type),
    INDEX idx_situation (game_situation)
);

CREATE TABLE formation_players (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    formation_id VARCHAR(50) NOT NULL,
    player_id VARCHAR(50),
    player_name VARCHAR(200) NOT NULL,
    position VARCHAR(5) NOT NULL,
    jersey_number INT NOT NULL,
    x_position DECIMAL(6,2) NOT NULL,
    y_position DECIMAL(6,2) NOT NULL,
    alignment VARCHAR(50),
    depth DECIMAL(5,2),

    FOREIGN KEY (formation_id) REFERENCES formations(formation_id) ON DELETE CASCADE,
    INDEX idx_formation (formation_id)
);

CREATE TABLE playbooks (
    playbook_id VARCHAR(50) PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    tags JSON
);

CREATE TABLE playbook_formations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    playbook_id VARCHAR(50) NOT NULL,
    formation_id VARCHAR(50) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,

    FOREIGN KEY (playbook_id) REFERENCES playbooks(playbook_id) ON DELETE CASCADE,
    FOREIGN KEY (formation_id) REFERENCES formations(formation_id) ON DELETE CASCADE,
    UNIQUE KEY unique_playbook_formation (playbook_id, formation_id)
);

CREATE TABLE formation_templates (
    template_id VARCHAR(50) PRIMARY KEY,
    formation_id VARCHAR(50) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    usage_count INT DEFAULT 0,
    avg_success_rate DECIMAL(5,4),

    FOREIGN KEY (formation_id) REFERENCES formations(formation_id)
);
```

---

## 5. Integration with Existing ML Models

```python
# backend/formation_ml_integration.py

import torch
import numpy as np
from models import create_model
import joblib
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent / "models"
DATA_DIR = Path(__file__).parent.parent / "data"

class FormationMLAnalyzer:
    """Integrate formation analysis with existing ML models"""

    def __init__(self):
        self.load_models()

    def load_models(self):
        """Load trained ML models"""
        # Load personnel model
        self.personnel_scaler = joblib.load(DATA_DIR / "scalers.pkl")['personnel']
        self.personnel_encoder = joblib.load(MODEL_DIR / "personnel_label_encoder.pkl")

        personnel_model = create_model('personnel',
                                      input_dim=6,
                                      num_personnel_groups=len(self.personnel_encoder.classes_))
        personnel_model.load_state_dict(
            torch.load(MODEL_DIR / 'personnel_model.pt', map_location='cpu')
        )
        personnel_model.eval()
        self.personnel_model = personnel_model

        # Load offensive model
        self.offensive_scaler = joblib.load(DATA_DIR / "scalers.pkl")['offensive']
        self.offensive_encoder = joblib.load(MODEL_DIR / "offensive_label_encoder.pkl")

        offensive_model = create_model('offensive',
                                      input_dim=12,
                                      num_classes=len(self.offensive_encoder.classes_))
        offensive_model.load_state_dict(
            torch.load(MODEL_DIR / 'offensive_model.pt', map_location='cpu')
        )
        offensive_model.eval()
        self.offensive_model = offensive_model

    def analyze_personnel_fit(self, formation: Formation, game_context: dict) -> float:
        """
        Analyze if personnel package fits game situation
        Returns: confidence score 0-1
        """
        # Features for personnel model: down, ydstogo, yardline_100,
        #                               score_differential, red_zone, goal_to_go
        features = np.array([[
            game_context.get('down', 1),
            game_context.get('distance', 10),
            formation.yard_line,
            game_context.get('score_differential', 0),
            1 if formation.yard_line <= 20 else 0,  # red_zone
            1 if formation.yard_line <= 10 else 0   # goal_to_go
        ]])

        features_scaled = self.personnel_scaler.transform(features)

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            probs = self.personnel_model.predict_proba(features_tensor).numpy()[0]

        # Find probability for current personnel package
        try:
            personnel_idx = list(self.personnel_encoder.classes_).index(
                formation.personnel_package.value + ' '
            )
            confidence = float(probs[personnel_idx])
        except ValueError:
            # Personnel package not in training data
            confidence = 0.5

        return confidence

    def predict_play_success(self, formation: Formation, game_context: dict) -> dict:
        """
        Predict success rates for different play types
        Returns: dict with play type probabilities and EPA
        """
        # Features for offensive model
        features = np.array([[
            game_context.get('down', 1),
            game_context.get('distance', 10),
            formation.yard_line,
            game_context.get('score_differential', 0),
            game_context.get('quarter', 2),
            game_context.get('time_remaining', 1800),
            game_context.get('half_seconds_remaining', 900),
            1 if formation.yard_line <= 20 else 0,
            1 if formation.yard_line <= 10 else 0,
            1 if game_context.get('time_remaining', 3600) <= 120 else 0,
            game_context.get('timeouts', 3),
            0  # team_encoded
        ]])

        features_scaled = self.offensive_scaler.transform(features)

        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_scaled)
            probs = self.offensive_model.predict_proba(features_tensor).numpy()[0]

        play_types = self.offensive_encoder.classes_
        play_probs = {play: float(prob) for play, prob in zip(play_types, probs)}

        # Estimate EPA based on play type and confidence
        best_play = play_types[np.argmax(probs)]
        estimated_epa = (max(probs) - 0.5) * 2.0  # Simple heuristic

        return {
            'play_probabilities': play_probs,
            'recommended_play': best_play,
            'expected_epa': estimated_epa,
            'success_probability': max(probs)
        }

    def evaluate_formation_balance(self, formation: Formation) -> dict:
        """
        Evaluate if formation is balanced for run/pass
        Returns: run_bias, pass_bias scores
        """
        # Count skill positions
        rb_count = sum(1 for p in formation.offensive_players
                      if p.position in ['RB', 'FB'])
        te_count = sum(1 for p in formation.offensive_players
                      if p.position == 'TE')
        wr_count = sum(1 for p in formation.offensive_players
                      if p.position == 'WR')

        # Analyze formation spread (WR alignment)
        wr_positions = [p.field_position.x for p in formation.offensive_players
                       if p.position == 'WR']

        if wr_positions:
            spread = max(wr_positions) - min(wr_positions)
        else:
            spread = 0

        # Run bias: More RBs/TEs, less spread
        run_bias = (rb_count * 0.25 + te_count * 0.15 - spread * 0.01)
        run_bias = max(0, min(1, run_bias))

        # Pass bias: More WRs, more spread
        pass_bias = (wr_count * 0.2 + spread * 0.015)
        pass_bias = max(0, min(1, pass_bias))

        return {
            'run_bias': run_bias,
            'pass_bias': pass_bias,
            'balance_score': 1 - abs(run_bias - pass_bias),
            'spread': spread,
            'personnel_breakdown': {
                'RB': rb_count,
                'TE': te_count,
                'WR': wr_count
            }
        }
```

---

## 6. Implementation Roadmap

### Phase 1: Core Foundation (Week 1-2)
- [ ] Implement data models (Pydantic schemas)
- [ ] Create database schema and migrations
- [ ] Build basic formation CRUD API endpoints
- [ ] Create formation validation logic

### Phase 2: ML Integration (Week 2-3)
- [ ] Integrate Personnel Optimizer model
- [ ] Integrate Offensive Play-Caller model
- [ ] Build formation simulation engine
- [ ] Implement formation effectiveness scoring

### Phase 3: Frontend - Visualization (Week 3-4)
- [ ] Build football field canvas component
- [ ] Implement player positioning visualization
- [ ] Add formation template library
- [ ] Create formation metadata editor

### Phase 4: Frontend - Interaction (Week 4-5)
- [ ] Implement drag-and-drop player positioning
- [ ] Add formation customization controls
- [ ] Build personnel package selector
- [ ] Create formation comparison view

### Phase 5: Simulation & Analysis (Week 5-6)
- [ ] Build simulation results visualization
- [ ] Add heat maps for blocking/receiving zones
- [ ] Implement real-time formation feedback
- [ ] Create adjustment recommendation system

### Phase 6: Playbook Management (Week 6-7)
- [ ] Build playbook CRUD operations
- [ ] Create formation approval workflow
- [ ] Add formation tagging and search
- [ ] Implement formation sharing

### Phase 7: Advanced Features (Week 7-8)
- [ ] Auto-generate formations from game context
- [ ] Add motion/shift animations
- [ ] Build formation comparison analytics
- [ ] Create coaching notes and annotations

### Phase 8: Polish & Testing (Week 8-9)
- [ ] Integration testing
- [ ] Performance optimization
- [ ] UI/UX refinement
- [ ] Documentation

---

## 7. Key Technical Decisions

### Why This Architecture?

1. **Pydantic Models**: Type-safe validation ensures formation integrity
2. **FastAPI**: Modern, async, auto-documented REST API
3. **React DnD**: Industry-standard drag-and-drop for player positioning
4. **ML Integration**: Leverages existing trained models for simulation
5. **Modular Design**: Each component (visualization, simulation, playbook) is independent

### Performance Considerations

- **Canvas Rendering**: Use HTML5 Canvas or WebGL for field visualization with 60fps
- **ML Inference**: Run on backend to leverage PyTorch models (< 100ms latency)
- **Caching**: Cache formation templates and simulation results
- **Real-time Updates**: WebSocket for live formation collaboration

### Security & Validation

- **Formation Rules**: Enforce NFL regulations (7 on line, eligible receivers)
- **Input Validation**: Pydantic validates all API inputs
- **User Permissions**: Role-based access (coach, coordinator, viewer)
- **Playbook Privacy**: Team-specific playbooks with access controls

---

## 8. Example Usage Flow

```
1. User selects game situation (3rd & 7, opponent 35, Q4, down 3)
   ↓
2. System recommends personnel package (11 personnel - 67% confidence)
   ↓
3. User selects "Shotgun Trips Right" formation template
   ↓
4. Field displays with 11 players in Shotgun Trips alignment
   ↓
5. User drags slot WR 2 yards deeper (edit mode)
   ↓
6. User clicks "Simulate"
   ↓
7. ML models analyze:
   - Personnel fit: 82%
   - Expected EPA: +0.34
   - Recommended plays: Mesh concept, Stick route, Bubble screen
   - Defensive response: Likely Cover 3 (weak against seam routes)
   ↓
8. User reviews simulation results
   ↓
9. User clicks "Approve & Save to Playbook"
   ↓
10. Formation saved as "3rd & Med - Shotgun Trips Mod" in playbook
```

---

This architecture provides a professional, scalable foundation for formation visualization and customization using proper NFL terminology throughout.
