
// STATE
const state = {
    view: 'offensive',
    visionMode: false,
    formation: 'shotgun',
    clock: 8 * 60 + 45,
    players: [],
    alerts: [] // "Coverage Gap", "Blitz"
};

// MOCK CONSTANTS
const FORMATIONS = {
    shotgun: [
        { id: 'QB', x: 0.5, y: 0.8, team: 'offense', role: 'QB' },
        { id: 'RB', x: 0.65, y: 0.8, team: 'offense', role: 'RB' },
        { id: 'LT', x: 0.3, y: 0.6, team: 'offense', role: 'OL' }, { id: 'LG', x: 0.4, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'C', x: 0.5, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'RG', x: 0.6, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RT', x: 0.7, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'WR1', x: 0.1, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR2', x: 0.9, y: 0.55, team: 'offense', role: 'WR' },
        { id: 'TE', x: 0.75, y: 0.6, team: 'offense', role: 'TE' }, { id: 'WR3', x: 0.2, y: 0.55, team: 'offense', role: 'WR' }
    ],
    empty: [
        { id: 'QB', x: 0.5, y: 0.8, team: 'offense', role: 'QB' },
        { id: 'LT', x: 0.3, y: 0.6, team: 'offense', role: 'OL' }, { id: 'LG', x: 0.4, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'C', x: 0.5, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'RG', x: 0.6, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RT', x: 0.7, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'WR1', x: 0.1, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR2', x: 0.9, y: 0.55, team: 'offense', role: 'WR' },
        { id: 'WR3', x: 0.2, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR4', x: 0.8, y: 0.55, team: 'offense', role: 'WR' },
        { id: 'RB', x: 0.6, y: 0.55, team: 'offense', role: 'RB' }
    ],
    iform: [
        { id: 'QB', x: 0.5, y: 0.65, team: 'offense', role: 'QB' },
        { id: 'FB', x: 0.5, y: 0.75, team: 'offense', role: 'FB' },
        { id: 'RB', x: 0.5, y: 0.85, team: 'offense', role: 'RB' },
        // OL...
        { id: 'LT', x: 0.3, y: 0.6, team: 'offense', role: 'OL' }, { id: 'LG', x: 0.4, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'C', x: 0.5, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'RG', x: 0.6, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RT', x: 0.7, y: 0.6, team: 'offense', role: 'OL' },
        { id: 'WR1', x: 0.1, y: 0.6, team: 'offense', role: 'WR' }, { id: 'TE', x: 0.75, y: 0.6, team: 'offense', role: 'TE' }
    ]
};

const DEFENSE = [
    { id: 'DE', x: 0.35, y: 0.5, team: 'defense' }, { id: 'DT', x: 0.45, y: 0.5, team: 'defense' },
    { id: 'DT', x: 0.55, y: 0.5, team: 'defense' }, { id: 'DE', x: 0.65, y: 0.5, team: 'defense' },
    { id: 'LB1', x: 0.4, y: 0.4, team: 'defense' }, { id: 'LB2', x: 0.6, y: 0.4, team: 'defense' }, { id: 'LB3', x: 0.5, y: 0.4, team: 'defense' },
    { id: 'CB1', x: 0.15, y: 0.45, team: 'defense' }, { id: 'CB2', x: 0.85, y: 0.45, team: 'defense' },
    { id: 'FS', x: 0.5, y: 0.25, team: 'defense' }, { id: 'SS', x: 0.6, y: 0.3, team: 'defense' }
];

// DOM
const canvas = document.getElementById('football-canvas');
const ctx = canvas.getContext('2d');
const configStart = document.getElementById('config-toggle');
const configDrawer = document.getElementById('config-drawer');
const configClose = document.querySelector('.close-config');
const visionBtn = document.getElementById('vision-toggle');
const formSelect = document.getElementById('formation-select');
const clockDisplay = document.getElementById('game-clock');
const radarWidget = document.getElementById('radar-widget');
const playName = document.getElementById('play-name');
const wristCode = document.querySelector('.wristband-code');

// LOOP
function init() {
    updatePlayers();
    setupEvents();
    resize();
    requestAnimationFrame(loop);
    setInterval(gameTick, 1000);
}

function updatePlayers() {
    let off = FORMATIONS[state.formation].map(p => ({ ...p }));
    // Fill generic OL if missing in mock
    // ... (simplified above)
    let def = DEFENSE.map(p => ({ ...p }));
    state.players = [...off, ...def];
}

function setupEvents() {
    configStart.onclick = () => configDrawer.classList.add('open');
    configClose.onclick = () => configDrawer.classList.remove('open');

    visionBtn.onclick = () => {
        state.visionMode = !state.visionMode;
        visionBtn.style.color = state.visionMode ? '#9333ea' : 'white';
    };

    formSelect.onchange = (e) => {
        state.formation = e.target.value;
        updatePlayers();
    };

    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active', 'offense', 'defense'));
            btn.classList.add('active');
            state.view = btn.dataset.view;
            if (state.view === 'offensive') btn.classList.add('offense');
            if (state.view === 'defensive') btn.classList.add('defense');

            // Logic Hooks
            if (state.view === 'defensive') {
                radarWidget.classList.add('visible');
                playName.innerText = "DEFENSE: NICKE BLITZ";
                wristCode.innerText = "RED 99";
            } else {
                radarWidget.classList.remove('visible');
                playName.innerText = "PA BOOT RIGHT";
                wristCode.innerText = "BLUE 42";
            }
        };
    });
}

function gameTick() {
    if (state.clock > 0) state.clock--;
    let m = Math.floor(state.clock / 60).toString().padStart(2, '0');
    let s = (state.clock % 60).toString().padStart(2, '0');
    clockDisplay.innerText = `${m}:${s}`;
}

// VISION STREAM SIMULATION (Animation Loop)
function loop() {
    resize(); // Cheap resize handle
    draw();

    // Simulate minor idle movement (breathing)
    state.players.forEach(p => {
        p.x += (Math.random() - 0.5) * 0.0005;
        p.y += (Math.random() - 0.5) * 0.0005;
        // Orientation Logic (always face LOS for now)
        p.orientation = p.team === 'offense' ? -Math.PI / 2 : Math.PI / 2;
    });

    requestAnimationFrame(loop);
}

function draw() {
    const w = canvas.width = canvas.parentElement.clientWidth;
    const h = canvas.height = canvas.parentElement.clientHeight;

    // FIELD
    let g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, '#020617'); g.addColorStop(0.3, '#064e3b'); g.addColorStop(1, '#065f46');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);

    // YARD LINES
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 2;
    for (let i = 1; i < 10; i++) {
        let y = (i / 10) * h;
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
        // Yard Numbers
        ctx.fillStyle = 'rgba(255,255,255,0.1)'; ctx.font = '20px Inter';
        ctx.fillText((50 - Math.abs(50 - i * 10)), 40, y - 5);
    }
    // LOS
    ctx.strokeStyle = '#3b82f6'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(0, h * 0.6); ctx.lineTo(w, h * 0.6); ctx.stroke();
    // First Down
    ctx.strokeStyle = '#fbbf24';
    ctx.beginPath(); ctx.moveTo(0, h * 0.5); ctx.lineTo(w, h * 0.5); ctx.stroke();

    // RENDER PLAYERS (Vision Stream)
    state.players.forEach(p => {
        let x = p.x * w;
        let y = p.y * h;

        // Shadow
        ctx.fillStyle = 'rgba(0,0,0,0.5)';
        ctx.beginPath(); ctx.ellipse(x, y + 10, 10, 5, 0, 0, Math.PI * 2); ctx.fill();

        // Base Dot
        ctx.fillStyle = p.team === 'offense' ? '#60a5fa' : '#ef4444';
        ctx.beginPath(); ctx.arc(x, y, 8, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = 'white'; ctx.lineWidth = 1.5; ctx.stroke();

        // Orientation Triangle (Vision Agent Feature)
        if (state.visionMode) {
            ctx.fillStyle = '#fff';
            ctx.save();
            ctx.translate(x, y);
            // ctx.rotate(p.orientation); // Mock rotation
            ctx.beginPath(); ctx.moveTo(0, -12); ctx.lineTo(4, -4); ctx.lineTo(-4, -4); ctx.fill();
            ctx.restore();

            // Velocity Vector
            if (p.team === 'defense') {
                ctx.strokeStyle = '#9333ea'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 15, y + 20); ctx.stroke(); // random vec
            }
        }
    });

    // ALERTS (Vision Agent)
    if (state.visionMode) {
        // Mock Coverage Gap
        ctx.fillStyle = 'rgba(251, 191, 36, 0.2)'; // Amber
        ctx.strokeStyle = '#fbbf24';
        ctx.beginPath(); ctx.ellipse(w * 0.2, h * 0.35, 60, 40, 0, 0, Math.PI * 2);
        ctx.fill(); ctx.stroke();

        ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 10px Inter';
        ctx.fillText('COVERAGE GAP', w * 0.2 - 40, h * 0.35);
    }
}

function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
}

init();
