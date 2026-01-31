"""
Generate NFL AI Coach Architecture Diagram
Creates a professional, detailed architectural diagram as an image file
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Set up figure
fig = plt.figure(figsize=(24, 16))
ax = fig.add_subplot(111)
ax.set_xlim(0, 24)
ax.set_ylim(0, 16)
ax.axis('off')

# Color scheme
COLORS = {
    'data': '#ADD8E6',      # Light blue
    'process': '#E6E6FA',   # Light purple
    'ml': '#90EE90',        # Light green
    'api': '#FFDAB9',       # Light orange
    'frontend': '#D3D3D3',  # Light gray
    'training': '#FFFFE0',  # Light yellow
    'testing': '#B0E2FF'    # Light blue
}

def create_box(ax, x, y, width, height, text, color, fontsize=8, linewidth=1.5):
    """Create a rounded box with text"""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.05",
                         edgecolor='black',
                         facecolor=color,
                         linewidth=linewidth,
                         zorder=2)
    ax.add_patch(box)

    # Add text
    ax.text(x + width/2, y + height/2, text,
           ha='center', va='center',
           fontsize=fontsize, fontweight='normal',
           wrap=True, zorder=3)
    return box

def create_arrow(ax, x1, y1, x2, y2, label='', color='black'):
    """Create an arrow between boxes"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->,head_width=0.15,head_length=0.15',
                           color=color,
                           linewidth=1.5,
                           zorder=1)
    ax.add_patch(arrow)

    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y, label,
               fontsize=6, ha='center', va='bottom',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.8))

# Title
ax.text(12, 15.5, 'NFL AI Coach - System Architecture',
       ha='center', va='center',
       fontsize=20, fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#4169E1', edgecolor='black', linewidth=2),
       color='white')

# ==================== LAYER 1: DATA SOURCES ====================
y_data = 13.5
box_width = 2.8
box_height = 0.8

create_box(ax, 2, y_data, box_width, box_height,
          'nflfastR API\n340,587 plays\n(2018-2024)',
          COLORS['data'], fontsize=7)

create_box(ax, 5.2, y_data, box_width, box_height,
          'FTN Charting\n137,899 plays\n(2022-2024)',
          COLORS['data'], fontsize=7)

create_box(ax, 8.4, y_data, box_width, box_height,
          'Roster Data\n2022-2024',
          COLORS['data'], fontsize=7)

create_box(ax, 11.6, y_data, box_width, box_height,
          'ESPN Live API\nReal-time data',
          COLORS['data'], fontsize=7)

# Label
ax.text(1, y_data + 0.4, 'DATA SOURCES',
       ha='right', va='center', fontsize=10, fontweight='bold', color='#1E90FF')

# ==================== LAYER 2: DATA PROCESSING ====================
y_process = 11.5

create_box(ax, 2, y_process, 3.5, 1,
          'NFLDataLoader\n━━━━━━━━━━━━━━━\npbp_2018_2024.parquet (128MB)\nftn_2022_2024.parquet (2MB)\nrosters_2022_2024.parquet (1MB)',
          COLORS['process'], fontsize=6.5)

create_box(ax, 5.8, y_process, 2.8, 1,
          'NFLFeatureEngineer\n━━━━━━━━━━━━━━━\nFeature extraction\n& transformation',
          COLORS['process'], fontsize=7)

create_box(ax, 9, y_process, 2.5, 1,
          'StandardScaler\n━━━━━━━━━━━━━━━\n5 scalers:\noffensive, defensive,\nfourth_down,\nwin_prob, personnel',
          COLORS['process'], fontsize=6)

create_box(ax, 11.8, y_process, 2.5, 1,
          'LabelEncoders\n━━━━━━━━━━━━━━━\nTeam encoder\nOffensive (4 classes)\nPersonnel (10 classes)',
          COLORS['process'], fontsize=6)

ax.text(1, y_process + 0.5, 'DATA\nPROCESSING',
       ha='right', va='center', fontsize=10, fontweight='bold', color='#8B008B')

# Arrows from data sources to data processing
create_arrow(ax, 3.4, y_data, 3.5, y_process + 1, 'raw\ndata', '#555')
create_arrow(ax, 6.6, y_data, 5.5, y_process + 1, '', '#555')
create_arrow(ax, 9.8, y_data, 7, y_process + 1, '', '#555')
create_arrow(ax, 13, y_data, 13, y_process + 1, '', '#555')

# ==================== LAYER 3: ML MODELS ====================
y_ml = 8
ml_width = 2.4
ml_height = 2.2

# Model 1: Offensive
create_box(ax, 2, y_ml, ml_width, ml_height,
          '1. OFFENSIVE\nPLAY-CALLER\n━━━━━━━━━━━━━━━\nInput: 12 features\n━━━━━━━━━━━━━━━\nArchitecture:\nFC(128)→BN→Drop\nFC(64)→BN→Drop\nFC(32)→BN\nFC(4)\n━━━━━━━━━━━━━━━\nOutput: 4 classes\npass, run, screen,\nplay_action\n━━━━━━━━━━━━━━━\n229,345 plays\nAcc: 69.4%',
          COLORS['ml'], fontsize=5.5)

# Model 2: Defensive
create_box(ax, 4.6, y_ml, ml_width, ml_height,
          '2. DEFENSIVE\nCOORDINATOR\n━━━━━━━━━━━━━━━\nInput: 11 features\n━━━━━━━━━━━━━━━\nArchitecture:\nFC(96)→BN→Drop\nFC(48)→BN→Drop\nFC(24)→BN\nFC(1)\n━━━━━━━━━━━━━━━\nOutput: Binary\nrun/pass prediction\n━━━━━━━━━━━━━━━\n229,345 plays\nAcc: 69.4%',
          COLORS['ml'], fontsize=5.5)

# Model 3: 4th Down
create_box(ax, 7.2, y_ml, ml_width, ml_height,
          '3. 4TH DOWN\nDECISION ENGINE\n━━━━━━━━━━━━━━━\nInput: 6 features\n━━━━━━━━━━━━━━━\nArchitecture:\nFC(64)→BN→Drop\nFC(32)→BN\n3 output heads\n━━━━━━━━━━━━━━━\nOutput:\nConversion prob\nFG prob\nExpected EPA\n━━━━━━━━━━━━━━━\n27,518 plays',
          COLORS['ml'], fontsize=5.5)

# Model 4: Win Prob
create_box(ax, 9.8, y_ml, ml_width, ml_height,
          '4. WIN PROB\nCALCULATOR\n━━━━━━━━━━━━━━━\nInput: 8 features\n━━━━━━━━━━━━━━━\nArchitecture:\nFC(128)→BN→Drop\nFC(64)→BN→Drop\nFC(32)→BN→Drop\nFC(16)→BN\nFC(1)\n━━━━━━━━━━━━━━━\nOutput:\nWin prob (0-1)\n━━━━━━━━━━━━━━━\n271,397 plays\nAcc: 73.2%',
          COLORS['ml'], fontsize=5.5)

# Model 5: Personnel
create_box(ax, 12.4, y_ml, ml_width, ml_height,
          '5. PERSONNEL\nOPTIMIZER\n━━━━━━━━━━━━━━━\nInput: 6 features\n━━━━━━━━━━━━━━━\nArchitecture:\nFC(96)→BN→Drop\nFC(48)→BN→Drop\nFC(24)→BN\nFC(10)\n━━━━━━━━━━━━━━━\nOutput: 10 groups\n11, 12, 13, 21,\n22, etc.\n━━━━━━━━━━━━━━━\n253,995 plays\nAcc: 82.9%',
          COLORS['ml'], fontsize=5.5)

ax.text(1, y_ml + 1.1, 'ML MODELS\n(PyTorch)',
       ha='right', va='center', fontsize=10, fontweight='bold', color='#228B22')

# Arrows from processing to models
create_arrow(ax, 7, y_process, 3.2, y_ml + ml_height, 'features', '#555')
create_arrow(ax, 8.5, y_process, 5.8, y_ml + ml_height, '', '#555')
create_arrow(ax, 10.25, y_process, 8.4, y_ml + ml_height, '', '#555')
create_arrow(ax, 11, y_process, 11, y_ml + ml_height, '', '#555')
create_arrow(ax, 12.5, y_process, 13.6, y_ml + ml_height, '', '#555')

# ==================== LAYER 4: BACKEND API ====================
y_api = 5.5

create_box(ax, 4, y_api, 7, 1.5,
          'FastAPI Server (port 8000)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nREST API Endpoints:\nPOST /predict/offensive  |  POST /predict/defensive  |  POST /predict/fourth-down\nPOST /predict/win-probability  |  POST /predict/personnel  |  POST /predict/all\nGET /live-games  |  GET /game/{game_id}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nCORS enabled | PyTorch inference | JSON request/response',
          COLORS['api'], fontsize=6.5)

ax.text(1, y_api + 0.75, 'BACKEND\nAPI',
       ha='right', va='center', fontsize=10, fontweight='bold', color='#FF8C00')

# Arrows from models to API
for x_pos in [3.2, 5.8, 8.4, 11, 13.6]:
    create_arrow(ax, x_pos, y_ml, 7.5, y_api + 1.5, 'predictions', '#555')

# ==================== LAYER 5: FRONTEND ====================
y_frontend = 3.5

create_box(ax, 5.5, y_frontend, 4, 1,
          'Next.js Application\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nReal-time game visualization\nInteractive coaching interface\nLive prediction display',
          COLORS['frontend'], fontsize=7)

ax.text(1, y_frontend + 0.5, 'FRONTEND',
       ha='right', va='center', fontsize=10, fontweight='bold', color='#696969')

# Arrow from API to Frontend
create_arrow(ax, 7.5, y_api, 7.5, y_frontend + 1, 'JSON\nresponses', '#555')

# ==================== RIGHT PANEL: TRAINING ====================
x_training = 15.5
y_training = 9

create_box(ax, x_training, y_training, 3.2, 2.5,
          'TRAINING PIPELINE\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\ntrain.py\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nHyperparameters:\n• Batch size: 512\n• Epochs: 50\n  (early stopping: 10)\n• Learning rate: 0.001\n• Optimizer: Adam\n• Scheduler: ReduceLR\n• Train/Val: 80/20\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nFeature engineering\nModel architectures\nCheckpoint saving',
          COLORS['training'], fontsize=6)

ax.text(x_training + 1.6, y_training + 2.8, 'TRAINING',
       ha='center', va='bottom', fontsize=10, fontweight='bold', color='#DAA520')

# Arrow from training to models
create_arrow(ax, x_training, y_training + 1.25, 14.8, y_ml + 1.1, 'train', '#8B4513')

# ==================== LEFT PANEL: TESTING ====================
x_testing = 15.5
y_testing = 5

create_box(ax, x_testing, y_testing, 3.2, 2.5,
          'VALIDATION & TESTING\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\ntest_models.py\n✓ Model loading (5/5)\n✓ Architecture matching\n✓ Inference testing\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\ndemo_scenarios.py\n✓ 6 game scenarios\n✓ All model predictions\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nvalidate_historical.py\n✓ Historical accuracy\n✓ Real game outcomes\n✓ Performance metrics',
          COLORS['testing'], fontsize=6)

ax.text(x_testing + 1.6, y_testing + 2.8, 'VALIDATION',
       ha='center', va='bottom', fontsize=10, fontweight='bold', color='#4682B4')

# Arrow from models to testing
create_arrow(ax, 14.8, y_ml + 0.5, x_testing, y_testing + 1.25, 'validate', '#4682B4')

# ==================== BOTTOM SECTION: DATA FLOW SUMMARY ====================
y_flow = 1.5

create_box(ax, 2, y_flow, 12, 1.2,
          'DATA FLOW SUMMARY\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n1. Raw Data → DataLoader → Cached Parquet  |  2. Cached Data → FeatureEngineer → Normalized Features  |  3. Features → 5 ML Models → Predictions\n4. Predictions → FastAPI → JSON  |  5. FastAPI ↔ Next.js (bidirectional)  |  6. ESPN Live API → FastAPI → Models (live games)',
          '#F0F8FF', fontsize=6.5)

# ==================== VERSION INFO ====================
ax.text(12, 0.5, 'PyTorch Neural Networks | FastAPI REST | Next.js Frontend | nflfastR Data (2018-2024)',
       ha='center', va='center', fontsize=7, style='italic', color='#555')

ax.text(12, 0.2, 'All 5 models retrained with complete class coverage (229K+ plays per model)',
       ha='center', va='center', fontsize=6, style='italic', color='#228B22', fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/dr.gretchenboria/nfl/arch_diag.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/Users/dr.gretchenboria/nfl/arch_diag.svg', bbox_inches='tight', facecolor='white')
print("Architecture diagram saved as:")
print("  - arch_diag.png (high-resolution raster)")
print("  - arch_diag.svg (scalable vector)")
