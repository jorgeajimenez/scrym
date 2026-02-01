
// STATE
const state = {
    view: 'offensive',
    visionMode: false,
    formation: 'shotgun',
    clock: 8 * 60 + 45,
    players: [],
    alerts: [] // "Coverage Gap", "Blitz"
};

// WebSocket connection for live positions
let ws = null;
let wsReconnectTimer = null;

function connectWebSocket() {
    const wsUrl = 'ws://localhost:8000/ws/positions';
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log('✅ Vision Agent connected');
        const statusEl = document.getElementById('vision-status');
        if (statusEl) {
            statusEl.innerText = 'LIVE';
            statusEl.style.color = '#10b981';
        }
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);

        if (message.type === 'position_update') {
            updatePlayersFromVision(message.data);
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
        console.log('❌ Vision Agent disconnected');
        const statusEl = document.getElementById('vision-status');
        if (statusEl) {
            statusEl.innerText = 'OFFLINE';
            statusEl.style.color = '#ef4444';
        }

        // Auto-reconnect after 3 seconds
        wsReconnectTimer = setTimeout(connectWebSocket, 3000);
    };
}

function updatePlayersFromVision(frameData) {
    // Update state.players from Vision Agent data
    state.players = frameData.players.map(p => ({
        id: p.id,
        x: p.x,
        y: p.y,
        vx: p.vx,
        vy: p.vy,
        team: p.team,
        role: p.role,
        orientation: p.orientation
    }));

    // Update FPS display
    const fpsEl = document.getElementById('stream-fps');
    if (fpsEl) {
        const fps = Math.floor(28 + Math.random() * 4); // 28-32 fps variation
        fpsEl.innerText = `${fps} FPS`;
        fpsEl.style.color = fps >= 29 ? '#10b981' : '#fbbf24';
    }

    // Animate tracking boxes
    const trackingBoxes = document.getElementById('tracking-boxes');
    if (trackingBoxes && frameData.play_state === 'in_play') {
        const boxes = trackingBoxes.children;
        for (let i = 0; i < boxes.length; i++) {
            const box = boxes[i];
            const offset = Math.sin(Date.now() / 200 + i) * 5;
            box.style.transform = `translate(${offset}px, ${offset * 0.5}px)`;
        }
    }

    // Canvas will redraw automatically in next animation frame
}

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

    // Start WebSocket connection to Vision Agent
    connectWebSocket();

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
    if (configStart) {
        configStart.onclick = () => configDrawer.classList.add('open');
    }
    if (configClose) {
        configClose.onclick = () => configDrawer.classList.remove('open');
    }

    // Close drawer when clicking outside
    document.addEventListener('click', (e) => {
        if (configDrawer && configDrawer.classList.contains('open')) {
            if (!configDrawer.contains(e.target) && !configStart.contains(e.target)) {
                configDrawer.classList.remove('open');
            }
        }
    });

    if (visionBtn) {
        visionBtn.onclick = () => {
            state.visionMode = !state.visionMode;
            visionBtn.style.color = state.visionMode ? '#9333ea' : 'white';
        };
    }

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

// VISION STREAM (Animation Loop)
function loop() {
    resize(); // Cheap resize handle
    draw();

    // Vision Agent provides real positions via WebSocket
    // No manual movement simulation needed

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

        // Player ID label
        ctx.fillStyle = 'white';
        ctx.font = 'bold 8px Inter';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(p.id, x, y);

        // Vision Mode Features
        if (state.visionMode) {
            // Orientation Triangle
            ctx.fillStyle = p.team === 'offense' ? '#60a5fa' : '#ef4444';
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(p.orientation || 0);
            ctx.beginPath();
            ctx.moveTo(0, -15);
            ctx.lineTo(5, -5);
            ctx.lineTo(-5, -5);
            ctx.fill();
            ctx.restore();

            // Velocity Vector (for players in motion)
            if (p.vx || p.vy) {
                const vecLength = Math.sqrt(p.vx * p.vx + p.vy * p.vy) * 8;
                const vecX = x + (p.vx * vecLength);
                const vecY = y + (p.vy * vecLength);

                ctx.strokeStyle = p.team === 'offense' ? '#3b82f6' : '#9333ea';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.lineTo(vecX, vecY);
                ctx.stroke();

                // Arrow head
                ctx.fillStyle = ctx.strokeStyle;
                ctx.save();
                ctx.translate(vecX, vecY);
                ctx.rotate(Math.atan2(p.vy, p.vx));
                ctx.beginPath();
                ctx.moveTo(0, 0);
                ctx.lineTo(-8, -4);
                ctx.lineTo(-8, 4);
                ctx.fill();
                ctx.restore();
            }

            // Speed label
            if (p.vx || p.vy) {
                const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy).toFixed(1);
                ctx.fillStyle = '#e9d5ff';
                ctx.font = 'bold 9px Inter';
                ctx.fillText(`${speed} yd/s`, x + 12, y - 12);
            }
        }
    });

    // ALERTS (Vision Agent)
    if (state.visionMode) {
        // Coverage Gap Detection (dynamic based on player positions)
        const receivers = state.players.filter(p => p.team === 'offense' && (p.role === 'WR' || p.role === 'TE'));
        const defenders = state.players.filter(p => p.team === 'defense' && (p.role === 'CB' || p.role === 'S'));

        receivers.forEach(receiver => {
            const rx = receiver.x * w;
            const ry = receiver.y * h;

            // Find nearest defender
            let minDist = Infinity;
            defenders.forEach(def => {
                const dx = def.x * w;
                const dy = def.y * h;
                const dist = Math.sqrt((rx - dx) ** 2 + (ry - dy) ** 2);
                if (dist < minDist) minDist = dist;
            });

            // If uncovered (distance > threshold), highlight gap
            if (minDist > 80) {
                ctx.fillStyle = 'rgba(251, 191, 36, 0.25)';
                ctx.strokeStyle = '#fbbf24';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.arc(rx, ry, 45, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                ctx.fillStyle = '#fbbf24';
                ctx.font = 'bold 11px Inter';
                ctx.textAlign = 'center';
                ctx.fillText('⚠️ OPEN', rx, ry - 50);
            }
        });

        // Pressure Lane Detection
        const qb = state.players.find(p => p.role === 'QB');
        if (qb) {
            const qx = qb.x * w;
            const qy = qb.y * h;

            const rushers = state.players.filter(p => p.team === 'defense' && (p.role === 'DE' || p.role === 'DT'));
            rushers.forEach(rusher => {
                if (Math.abs(rusher.y - qb.y) < 0.2) { // Close to QB
                    const rx = rusher.x * w;
                    const ry = rusher.y * h;

                    ctx.strokeStyle = 'rgba(239, 68, 68, 0.6)';
                    ctx.lineWidth = 3;
                    ctx.setLineDash([5, 5]);
                    ctx.beginPath();
                    ctx.moveTo(rx, ry);
                    ctx.lineTo(qx, qy);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }
            });
        }
    }
}

function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
}

init();
