"""
Generate Formation Feature Architecture Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = plt.figure(figsize=(20, 14))
ax = fig.add_subplot(111)
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

COLORS = {
    'frontend': '#E3F2FD',
    'api': '#FFF3E0',
    'ml': '#E8F5E9',
    'data': '#F3E5F5',
    'db': '#FFF9C4'
}

def create_box(ax, x, y, width, height, text, color, fontsize=8):
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.05",
                         edgecolor='black',
                         facecolor=color,
                         linewidth=2,
                         zorder=2)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
           ha='center', va='center',
           fontsize=fontsize, fontweight='normal',
           wrap=True, zorder=3)

def create_arrow(ax, x1, y1, x2, y2, label='', color='black'):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->,head_width=0.2,head_length=0.2',
                           color=color,
                           linewidth=2,
                           zorder=1)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y, label,
               fontsize=7, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', linewidth=1))

# Title
ax.text(10, 13.5, 'Formation Visualization & Customization - Architecture',
       ha='center', va='center',
       fontsize=18, fontweight='bold',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#1976D2', edgecolor='black', linewidth=2),
       color='white')

# ==================== FRONTEND LAYER ====================
y_frontend = 11

create_box(ax, 1, y_frontend, 3.5, 1.5,
          'Formation Editor\n━━━━━━━━━━━━━━━\n• Drag & drop players\n• Formation templates\n• Real-time validation\n• Edit/View modes',
          COLORS['frontend'], fontsize=7)

create_box(ax, 5, y_frontend, 3.5, 1.5,
          'Football Field Canvas\n━━━━━━━━━━━━━━━\n• Interactive field\n• Player positioning\n• Hash marks & LOS\n• Visual feedback',
          COLORS['frontend'], fontsize=7)

create_box(ax, 9, y_frontend, 3.5, 1.5,
          'Simulation Display\n━━━━━━━━━━━━━━━\n• Success metrics\n• Heat maps\n• Play recommendations\n• Adjustments',
          COLORS['frontend'], fontsize=7)

create_box(ax, 13, y_frontend, 3.5, 1.5,
          'Playbook Manager\n━━━━━━━━━━━━━━━\n• Save formations\n• Browse playbook\n• Compare formations\n• Share & approve',
          COLORS['frontend'], fontsize=7)

ax.text(0.5, y_frontend + 0.75, 'FRONTEND\n(React/Next.js)',
       ha='right', va='center', fontsize=9, fontweight='bold', color='#1976D2')

# ==================== API LAYER ====================
y_api = 8.5

create_box(ax, 2, y_api, 3, 1.2,
          'Formation API\n━━━━━━━━━━━━━━━\nPOST /create\nPOST /validate\nGET /templates\nPOST /simulate',
          COLORS['api'], fontsize=7)

create_box(ax, 5.5, y_api, 3, 1.2,
          'Playbook API\n━━━━━━━━━━━━━━━\nPOST /playbook/save\nGET /playbook/{id}\nPOST /compare\nPOST /auto-generate',
          COLORS['api'], fontsize=7)

create_box(ax, 9, y_api, 3.5, 1.2,
          'Personnel Validation\n━━━━━━━━━━━━━━━\n• 11 players check\n• Personnel count validation\n• Line of scrimmage rules\n• Eligible receivers',
          COLORS['api'], fontsize=7)

create_box(ax, 13, y_api, 3, 1.2,
          'Formation Generator\n━━━━━━━━━━━━━━━\n• Auto-generate\n• Template library\n• Situation-based\n• ML-optimized',
          COLORS['api'], fontsize=7)

ax.text(0.5, y_api + 0.6, 'API LAYER\n(FastAPI)',
       ha='right', va='center', fontsize=9, fontweight='bold', color='#F57C00')

# Arrows from frontend to API
create_arrow(ax, 2.75, y_frontend, 3.5, y_api + 1.2, 'create/edit', '#555')
create_arrow(ax, 6.75, y_frontend, 5.5, y_api + 1.2, '', '#555')
create_arrow(ax, 10.75, y_frontend, 7, y_api + 1.2, 'simulate', '#555')
create_arrow(ax, 14.75, y_frontend, 14.5, y_api + 1.2, 'save', '#555')

# ==================== ML INTEGRATION LAYER ====================
y_ml = 6

create_box(ax, 1, y_ml, 3.5, 1.5,
          'Personnel Optimizer\n━━━━━━━━━━━━━━━\nInput: 6 features\nOutput: 10 personnel groups\n━━━━━━━━━━━━━━━\nEvaluates if personnel\nmatches game situation\n━━━━━━━━━━━━━━━\nConfidence: 82.9%',
          COLORS['ml'], fontsize=6.5)

create_box(ax, 5, y_ml, 3.5, 1.5,
          'Offensive Play-Caller\n━━━━━━━━━━━━━━━\nInput: 12 features\nOutput: 4 play types\n━━━━━━━━━━━━━━━\nPredicts optimal plays\nfor formation\n━━━━━━━━━━━━━━━\nEPA estimation',
          COLORS['ml'], fontsize=6.5)

create_box(ax, 9, y_ml, 3.5, 1.5,
          'Defensive Coordinator\n━━━━━━━━━━━━━━━\nInput: 11 features\nOutput: Run/Pass prob\n━━━━━━━━━━━━━━━\nPredicts defensive\nresponse to formation\n━━━━━━━━━━━━━━━\nIdentifies weaknesses',
          COLORS['ml'], fontsize=6.5)

create_box(ax, 13, y_ml, 3.5, 1.5,
          'Formation Analyzer\n━━━━━━━━━━━━━━━\n• Balance evaluation\n• Spread calculation\n• Run/Pass bias\n• Efficiency scoring\n━━━━━━━━━━━━━━━\nCombines all models',
          COLORS['ml'], fontsize=6.5)

ax.text(0.5, y_ml + 0.75, 'ML MODELS\n(PyTorch)',
       ha='right', va='center', fontsize=9, fontweight='bold', color='#388E3C')

# Arrows from API to ML
create_arrow(ax, 5.5, y_api, 2.75, y_ml + 1.5, 'validate\npersonnel', '#2E7D32')
create_arrow(ax, 7, y_api, 6.75, y_ml + 1.5, 'predict\nplays', '#2E7D32')
create_arrow(ax, 10.75, y_api, 10.75, y_ml + 1.5, 'simulate', '#2E7D32')
create_arrow(ax, 14.5, y_api, 14.75, y_ml + 1.5, 'analyze', '#2E7D32')

# ==================== DATA MODELS LAYER ====================
y_data = 3.5

create_box(ax, 1.5, y_data, 3, 1.3,
          'Formation Model\n━━━━━━━━━━━━━━━\n• formation_id\n• personnel_package\n• formation_type\n• 11 PlayerOnField\n• yard_line, down',
          COLORS['data'], fontsize=6.5)

create_box(ax, 5, y_data, 3, 1.3,
          'PlayerOnField\n━━━━━━━━━━━━━━━\n• position (QB/RB/WR)\n• field_position (x,y)\n• jersey_number\n• alignment\n• depth from LOS',
          COLORS['data'], fontsize=6.5)

create_box(ax, 8.5, y_data, 3.5, 1.3,
          'SimulationResult\n━━━━━━━━━━━━━━━\n• personnel_match_score\n• expected_epa\n• success_probability\n• run/pass efficiency\n• recommendations',
          COLORS['data'], fontsize=6.5)

create_box(ax, 12.5, y_data, 3.5, 1.3,
          'Playbook Model\n━━━━━━━━━━━━━━━\n• playbook_id\n• team_name\n• formations[]\n• tags\n• created_at',
          COLORS['data'], fontsize=6.5)

ax.text(0.5, y_data + 0.65, 'DATA\nMODELS\n(Pydantic)',
       ha='right', va='center', fontsize=9, fontweight='bold', color='#7B1FA2')

# Arrows from ML to Data
create_arrow(ax, 2.75, y_ml, 3, y_data + 1.3, '', '#7B1FA2')
create_arrow(ax, 6.75, y_ml, 6.5, y_data + 1.3, '', '#7B1FA2')
create_arrow(ax, 10.75, y_ml, 10.25, y_data + 1.3, '', '#7B1FA2')
create_arrow(ax, 14.75, y_ml, 14.25, y_data + 1.3, '', '#7B1FA2')

# ==================== DATABASE LAYER ====================
y_db = 1.5

create_box(ax, 2, y_db, 3.5, 1,
          'formations table\n━━━━━━━━━━━━━━━\nformation_id (PK)\nname, personnel_package\nformation_type, yard_line\npredicted_success_rate',
          COLORS['db'], fontsize=6.5)

create_box(ax, 6, y_db, 3.5, 1,
          'formation_players table\n━━━━━━━━━━━━━━━\nformation_id (FK)\nplayer_id, position\nx_position, y_position\nalignment, depth',
          COLORS['db'], fontsize=6.5)

create_box(ax, 10, y_db, 3, 1,
          'playbooks table\n━━━━━━━━━━━━━━━\nplaybook_id (PK)\nteam_name\ncreated_at\ntags (JSON)',
          COLORS['db'], fontsize=6.5)

create_box(ax, 13.5, y_db, 3, 1,
          'formation_templates\n━━━━━━━━━━━━━━━\ntemplate_id (PK)\nis_default\navg_success_rate\nusage_count',
          COLORS['db'], fontsize=6.5)

ax.text(0.5, y_db + 0.5, 'DATABASE\n(PostgreSQL)',
       ha='right', va='center', fontsize=9, fontweight='bold', color='#F9A825')

# Arrows from Data to DB
create_arrow(ax, 3, y_data, 3.75, y_db + 1, 'persist', '#F57F17')
create_arrow(ax, 6.5, y_data, 7.75, y_db + 1, '', '#F57F17')
create_arrow(ax, 10.25, y_data, 11.5, y_db + 1, '', '#F57F17')
create_box(ax, 14.25, y_data, 15, y_db + 1, '', '#F57F17')

# ==================== KEY FEATURES BOX ====================
create_box(ax, 17.5, 10, 2, 3,
          'KEY FEATURES\n━━━━━━━━━━━━━━━\n✓ Drag & drop\n   player positions\n\n✓ Real-time\n   ML simulation\n\n✓ Personnel\n   validation\n\n✓ Formation\n   templates\n\n✓ Playbook\n   management\n\n✓ Heat maps\n\n✓ Auto-generate\n   formations',
          '#E0F7FA', fontsize=6.5)

# ==================== DATA FLOW BOX ====================
create_box(ax, 0.5, 0.2, 16, 0.8,
          'DATA FLOW: User drags player → Validation → ML Simulation (Personnel + Play-Caller + Defensive) → Results Display → Approve → Save to Playbook → Database',
          '#ECEFF1', fontsize=7)

# ==================== NFL TERMINOLOGY BOX ====================
create_box(ax, 17.5, 6.5, 2, 2.5,
          'NFL TERMINOLOGY\n━━━━━━━━━━━━━━━\nPersonnel:\n  11 = 1RB,1TE,3WR\n  12 = 1RB,2TE,2WR\n  21 = 2RB,1TE,2WR\n\nFormation:\n  Shotgun\n  I-Formation\n  Bunch\n\nAlignment:\n  Trips Right\n  Twins',
          '#FFF8E1', fontsize=6)

# Version info
ax.text(10, 0.1, 'Integrated with existing Personnel Optimizer (83% acc), Offensive Play-Caller (69% acc), Defensive Coordinator (69% acc)',
       ha='center', va='bottom', fontsize=6, style='italic', color='#555')

plt.tight_layout()
plt.savefig('/Users/dr.gretchenboria/nfl/formation_feature_architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/Users/dr.gretchenboria/nfl/formation_feature_architecture.svg', bbox_inches='tight', facecolor='white')
print("Formation feature architecture diagram saved!")
