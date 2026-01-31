"""
Generate Professional Formation Feature Architecture Diagram V2
Clean, modern design with clear visual hierarchy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.lines as mlines

fig = plt.figure(figsize=(28, 18))
ax = fig.add_subplot(111)
ax.set_xlim(0, 28)
ax.set_ylim(0, 18)
ax.axis('off')

# Modern color palette
COLORS = {
    'primary': '#2196F3',
    'secondary': '#FF9800',
    'success': '#4CAF50',
    'warning': '#FFC107',
    'info': '#00BCD4',
    'purple': '#9C27B0',
    'gray': '#607D8B',

    'box_frontend': '#E3F2FD',
    'box_api': '#FFF3E0',
    'box_ml': '#E8F5E9',
    'box_data': '#F3E5F5',
    'box_db': '#FFF9C4'
}

def create_modern_box(ax, x, y, width, height, title, items, color, title_color='white'):
    """Create a modern card-style box"""
    # Main box
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.02",
                         edgecolor='#333',
                         facecolor=color,
                         linewidth=2.5,
                         zorder=2)
    ax.add_patch(box)

    # Title bar
    title_bar = FancyBboxPatch((x, y + height - 0.35), width, 0.35,
                              boxstyle="round,pad=0.01",
                              edgecolor='none',
                              facecolor=COLORS['primary'],
                              zorder=3)
    ax.add_patch(title_bar)

    # Title text
    ax.text(x + width/2, y + height - 0.175, title,
           ha='center', va='center',
           fontsize=10, fontweight='bold',
           color=title_color, zorder=4)

    # Items
    if isinstance(items, str):
        ax.text(x + width/2, y + height/2 - 0.2, items,
               ha='center', va='center',
               fontsize=8, zorder=3,
               linespacing=1.6)
    else:
        y_offset = y + height - 0.5
        for item in items:
            ax.text(x + 0.15, y_offset, f"• {item}",
                   ha='left', va='top',
                   fontsize=7.5, zorder=3)
            y_offset -= 0.25

def create_flow_arrow(ax, x1, y1, x2, y2, label='', color='#2196F3', style='solid'):
    """Create a modern flow arrow"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->,head_width=0.25,head_length=0.3',
                           color=color,
                           linewidth=3,
                           linestyle=style,
                           zorder=1,
                           alpha=0.8)
    ax.add_patch(arrow)

    if label:
        # Calculate angle for text rotation
        dx, dy = x2 - x1, y2 - y1
        angle = 0  # Keep horizontal for readability

        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y, label,
               fontsize=8, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.4',
                        facecolor='white',
                        edgecolor=color,
                        linewidth=2,
                        alpha=0.95),
               fontweight='bold',
               color=color,
               rotation=angle)

def create_section_header(ax, x, y, text, color):
    """Create a section header"""
    ax.text(x, y, text,
           fontsize=13, fontweight='bold',
           color=color,
           bbox=dict(boxstyle='round,pad=0.6',
                    facecolor='white',
                    edgecolor=color,
                    linewidth=3))

# ==================== TITLE ====================
title_box = FancyBboxPatch((2, 16.5), 24, 1.2,
                          boxstyle="round,pad=0.1",
                          edgecolor='#1565C0',
                          facecolor='#1976D2',
                          linewidth=4,
                          zorder=5)
ax.add_patch(title_box)

ax.text(14, 17.1, 'Formation Visualization & Customization System',
       ha='center', va='center',
       fontsize=22, fontweight='bold',
       color='white', zorder=6)

ax.text(14, 16.7, 'Interactive NFL Personnel & Formation Management with AI-Powered Analysis',
       ha='center', va='center',
       fontsize=11, style='italic',
       color='white', zorder=6, alpha=0.9)

# ==================== SECTION 1: USER INTERFACE ====================
y_ui = 14

create_section_header(ax, 1, y_ui + 0.5, '1. USER INTERFACE', COLORS['primary'])

# Formation Editor
create_modern_box(ax, 2, y_ui - 1.5, 4.5, 2,
                 'Formation Editor',
                 ['Drag & drop player positioning',
                  'Real-time field validation',
                  'Edit/View mode toggle',
                  'Undo/Redo support',
                  'Formation templates library'],
                 COLORS['box_frontend'])

# Interactive Field
create_modern_box(ax, 7, y_ui - 1.5, 4.5, 2,
                 'Interactive Football Field',
                 ['53.3 yard width rendering',
                  'Hash marks & yard lines',
                  'Line of scrimmage marker',
                  'Player position indicators',
                  'Snap animation preview'],
                 COLORS['box_frontend'])

# Results Dashboard
create_modern_box(ax, 12, y_ui - 1.5, 4.5, 2,
                 'Simulation Dashboard',
                 ['Success probability metrics',
                  'EPA calculation display',
                  'Heat map visualization',
                  'Play recommendations',
                  'Defensive weakness overlay'],
                 COLORS['box_frontend'])

# Playbook Management
create_modern_box(ax, 17, y_ui - 1.5, 4.5, 2,
                 'Playbook Manager',
                 ['Save/Load formations',
                  'Compare multiple setups',
                  'Share with coaching staff',
                  'Tag & categorize plays',
                  'Export to PDF/Print'],
                 COLORS['box_frontend'])

# Technology badge
ax.text(22, y_ui - 1.8, 'React + Next.js\nReact DnD\nCanvas API',
       ha='center', va='center',
       fontsize=7, style='italic',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD', edgecolor='#2196F3', linewidth=2),
       color='#1976D2')

# ==================== SECTION 2: API LAYER ====================
y_api = 10.5

create_section_header(ax, 1, y_api + 0.5, '2. REST API LAYER', COLORS['secondary'])

# Formation Endpoints
create_modern_box(ax, 2, y_api - 1.5, 5, 2,
                 'Formation API',
                 'POST /formations/create\nPOST /formations/validate\nGET /formations/templates\nPOST /formations/simulate\nPOST /formations/compare\nPUT /formations/{id}',
                 COLORS['box_api'])

# Validation Service
create_modern_box(ax, 7.5, y_api - 1.5, 5, 2,
                 'Validation Service',
                 '✓ 11 players on field\n✓ Personnel package accuracy\n✓ 7+ on line of scrimmage\n✓ Eligible receiver rules\n✓ Formation legality check',
                 COLORS['box_api'])

# Playbook Endpoints
create_modern_box(ax, 13, y_api - 1.5, 4.5, 2,
                 'Playbook API',
                 'GET /playbooks/{id}\nPOST /playbooks/save\nPOST /playbooks/share\nDELETE /playbooks/{id}/formation',
                 COLORS['box_api'])

# Auto-Generate
create_modern_box(ax, 18, y_api - 1.5, 3.5, 2,
                 'AI Generator',
                 'Context-aware\nformation creation\n\nML-optimized\nplayer positioning',
                 COLORS['box_api'])

# Technology badge
ax.text(22, y_api - 1.8, 'FastAPI\nPydantic\nAsync/Await',
       ha='center', va='center',
       fontsize=7, style='italic',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=2),
       color='#F57C00')

# Arrows UI -> API
create_flow_arrow(ax, 4.25, y_ui - 1.5, 4.5, y_api + 0.5, 'Create/Edit', COLORS['primary'])
create_flow_arrow(ax, 9.25, y_ui - 1.5, 10, y_api + 0.5, 'Validate', COLORS['primary'])
create_flow_arrow(ax, 14.25, y_ui - 1.5, 10, y_api + 0.5, 'Simulate', COLORS['primary'])
create_flow_arrow(ax, 19.25, y_ui - 1.5, 15, y_api + 0.5, 'Save', COLORS['primary'])

# ==================== SECTION 3: ML INTELLIGENCE ====================
y_ml = 6.5

create_section_header(ax, 1, y_ml + 0.5, '3. ML INTELLIGENCE LAYER', COLORS['success'])

# Personnel Optimizer
create_modern_box(ax, 2, y_ml - 1.8, 4.2, 2.3,
                 'Personnel Optimizer',
                 '📊 INPUT: 6 features\n   (down, distance, yard line,\n    score diff, red zone, goal)\n\n🧠 ARCHITECTURE:\n   FC(96→48→24) + BatchNorm\n\n📈 OUTPUT: 10 personnel groups\n   (11, 12, 13, 21, 22, etc.)\n\n✓ Accuracy: 82.9%\n✓ Training: 254K plays',
                 COLORS['box_ml'])

# Offensive Play-Caller
create_modern_box(ax, 6.7, y_ml - 1.8, 4.2, 2.3,
                 'Offensive Play-Caller',
                 '📊 INPUT: 12 features\n   (situation + field position)\n\n🧠 ARCHITECTURE:\n   FC(128→64→32) + Dropout\n\n📈 OUTPUT: 4 play types\n   (pass, run, screen, play action)\n\n✓ Accuracy: 69.4%\n✓ Training: 229K plays',
                 COLORS['box_ml'])

# Defensive Coordinator
create_modern_box(ax, 11.4, y_ml - 1.8, 4.2, 2.3,
                 'Defensive Coordinator',
                 '📊 INPUT: 11 features\n   (situation + tendencies)\n\n🧠 ARCHITECTURE:\n   FC(96→48→24) + BatchNorm\n\n📈 OUTPUT: Run/Pass prob\n   (binary classification)\n\n✓ Accuracy: 69.4%\n✓ Training: 229K plays',
                 COLORS['box_ml'])

# Formation Analyzer
create_modern_box(ax, 16.1, y_ml - 1.8, 5.4, 2.3,
                 'Formation Analyzer',
                 '🎯 COMBINES ALL MODELS:\n\n• Personnel match scoring\n• Play success prediction\n• Defensive response forecast\n• EPA calculation\n• Run/Pass efficiency\n• Spread analysis\n• Balance evaluation\n\n→ Comprehensive formation grade',
                 COLORS['box_ml'])

# Technology badge
ax.text(22.5, y_ml - 1.8, 'PyTorch\nScikit-learn\nNumPy',
       ha='center', va='center',
       fontsize=7, style='italic',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F5E9', edgecolor='#4CAF50', linewidth=2),
       color='#2E7D32')

# Arrows API -> ML
create_flow_arrow(ax, 4.5, y_api - 1.5, 4.1, y_ml + 0.5, 'Personnel\nValidation', COLORS['success'])
create_flow_arrow(ax, 10, y_api - 1.5, 8.8, y_ml + 0.5, 'Play\nPrediction', COLORS['success'])
create_flow_arrow(ax, 15, y_api - 1.5, 13.5, y_ml + 0.5, 'Defense\nAnalysis', COLORS['success'])
create_flow_arrow(ax, 19.75, y_api - 1.5, 18.7, y_ml + 0.5, 'Full\nSimulation', COLORS['success'])

# ==================== SECTION 4: DATA & PERSISTENCE ====================
y_data = 2.5

create_section_header(ax, 1, y_data + 0.5, '4. DATA & PERSISTENCE', COLORS['purple'])

# Data Models
create_modern_box(ax, 2, y_data - 1.5, 4.5, 2,
                 'Pydantic Models',
                 '📦 Formation\n   • formation_id, name\n   • personnel_package\n   • formation_type\n   • 11 PlayerOnField objects\n\n📦 PlayerOnField\n   • position (QB/RB/WR/TE)\n   • field_position (x, y)\n   • jersey_number, alignment',
                 COLORS['box_data'])

# Database
create_modern_box(ax, 7, y_data - 1.5, 5, 2,
                 'PostgreSQL Database',
                 '🗄️ formations table\n   ├─ formation metadata\n   ├─ personnel package\n   └─ predicted_success_rate\n\n🗄️ formation_players table\n   ├─ player positions (FK)\n   └─ x/y coordinates',
                 COLORS['box_db'])

# Playbook Storage
create_modern_box(ax, 12.5, y_data - 1.5, 4.5, 2,
                 'Playbook Storage',
                 '📚 playbooks table\n   • team_name, tags\n   • created_at, updated_at\n\n📚 playbook_formations\n   • formation references\n   • notes, categories',
                 COLORS['box_db'])

# Template Library
create_modern_box(ax, 17.5, y_data - 1.5, 4, 2,
                 'Template Library',
                 '📋 Pre-built formations:\n   • Shotgun Trips\n   • I-Formation\n   • Bunch\n   • Empty\n   • Pistol\n\n✓ 50+ templates\n✓ Usage statistics',
                 COLORS['box_data'])

# Arrows ML -> Data
create_flow_arrow(ax, 4.1, y_ml - 1.8, 4.25, y_data + 0.5, 'Persist', COLORS['purple'])
create_flow_arrow(ax, 8.8, y_ml - 1.8, 9.5, y_data + 0.5, 'Store', COLORS['purple'])
create_flow_arrow(ax, 13.5, y_ml - 1.8, 14.75, y_data + 0.5, 'Save', COLORS['purple'])
create_flow_arrow(ax, 18.7, y_ml - 1.8, 19.5, y_data + 0.5, 'Archive', COLORS['purple'])

# ==================== SIDE PANEL: KEY FEATURES ====================
create_modern_box(ax, 23, 13, 4.5, 4.5,
                 'KEY FEATURES',
                 ['✓ Drag & drop interface',
                  '✓ Real-time ML analysis',
                  '✓ NFL rules validation',
                  '✓ 50+ formation templates',
                  '✓ Heat map visualization',
                  '✓ Multi-formation compare',
                  '✓ AI auto-generation',
                  '✓ Playbook management',
                  '✓ Export & share',
                  '✓ Mobile responsive'],
                 '#E1F5FE')

# ==================== SIDE PANEL: NFL TERMINOLOGY ====================
create_modern_box(ax, 23, 7.5, 4.5, 5,
                 'NFL TERMINOLOGY',
                 '📋 PERSONNEL PACKAGES:\n\n11 = 1 RB, 1 TE, 3 WR\n   (Spread passing)\n\n12 = 1 RB, 2 TE, 2 WR\n   (Balanced attack)\n\n21 = 2 RB, 1 TE, 2 WR\n   (Power running)\n\n13 = 1 RB, 3 TE, 1 WR\n   (Goal line/Heavy)\n\n00 = 0 RB, 0 TE, 5 WR\n   (5-wide shotgun)\n\n━━━━━━━━━━━━━━━━━\n\n📋 FORMATIONS:\n• Shotgun, Pistol\n• I-Formation, Singleback\n• Bunch, Trips, Spread\n• Empty, Wildcat',
                 '#FFF8E1')

# ==================== DATA FLOW DIAGRAM ====================
flow_box = FancyBboxPatch((1.5, 0.2), 20, 1,
                         boxstyle="round,pad=0.05",
                         edgecolor=COLORS['info'],
                         facecolor='#E0F7FA',
                         linewidth=3,
                         zorder=2)
ax.add_patch(flow_box)

ax.text(11.5, 0.9, 'END-TO-END DATA FLOW',
       ha='center', va='center',
       fontsize=11, fontweight='bold',
       color=COLORS['info'])

ax.text(11.5, 0.5, 'User Drags Player → Validation (11 players, LOS rules) → ML Simulation (Personnel + Play-Caller + Defense) → '
       'Results (EPA, Success %, Heat Maps) → User Approves → Save to Playbook → Database Storage',
       ha='center', va='center',
       fontsize=7.5, linespacing=1.4,
       color='#006064')

# ==================== FOOTER ====================
ax.text(14, 0.05, '© NFL AI Coach System  |  Integrated with existing PyTorch models  |  Production-ready architecture',
       ha='center', va='bottom',
       fontsize=7, style='italic',
       color='#666')

plt.tight_layout()
plt.savefig('/Users/dr.gretchenboria/nfl/formation_arch_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('/Users/dr.gretchenboria/nfl/formation_arch_diagram.svg', bbox_inches='tight', facecolor='white')
print("\n✓ Formation architecture diagram saved!")
print("  - formation_arch_diagram.png (high-res)")
print("  - formation_arch_diagram.svg (scalable)\n")
