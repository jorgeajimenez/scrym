'use client';

import React, { useEffect, useState, useMemo } from 'react';
import FootballField, { Player, Formations } from '@/components/FootballField';
import RightSidebar from '@/components/RightSidebar';
import DataPanel from '@/components/DataPanel';
import { Dribbble, Settings } from 'lucide-react';

// --- MOCK DATA ---
const OFFENSIVE_FORMATIONS: Formations = {
    shotgun: [ { id: 'QB', x: 0.5, y: 0.8, team: 'offense', role: 'QB' }, { id: 'RB', x: 0.55, y: 0.7, team: 'offense', role: 'RB' }, { id: 'LT', x: 0.3, y: 0.6, team: 'offense', role: 'OL' }, { id: 'LG', x: 0.4, y: 0.6, team: 'offense', role: 'OL' }, { id: 'C', x: 0.5, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RG', x: 0.6, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RT', x: 0.7, y: 0.6, team: 'offense', role: 'OL' }, { id: 'WR1', x: 0.1, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR2', x: 0.9, y: 0.55, team: 'offense', role: 'WR' }, { id: 'TE', x: 0.75, y: 0.6, team: 'offense', role: 'TE' } ],
    iform: [ { id: 'QB', x: 0.5, y: 0.65, team: 'offense', role: 'QB' }, { id: 'FB', x: 0.5, y: 0.75, team: 'offense', role: 'FB' }, { id: 'RB', x: 0.5, y: 0.85, team: 'offense', role: 'RB' }, { id: 'LT', x: 0.3, y: 0.6, team: 'offense', role: 'OL' }, { id: 'LG', x: 0.4, y: 0.6, team: 'offense', role: 'OL' }, { id: 'C', x: 0.5, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RG', x: 0.6, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RT', x: 0.7, y: 0.6, team: 'offense', role: 'OL' }, { id: 'WR1', x: 0.1, y: 0.6, team: 'offense', role: 'WR' }, { id: 'TE', x: 0.75, y: 0.6, team: 'offense', role: 'TE' } ],
    empty: [ { id: 'QB', x: 0.5, y: 0.8, team: 'offense', role: 'QB' }, { id: 'LT', x: 0.3, y: 0.6, team: 'offense', role: 'OL' }, { id: 'LG', x: 0.4, y: 0.6, team: 'offense', role: 'OL' }, { id: 'C', x: 0.5, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RG', x: 0.6, y: 0.6, team: 'offense', role: 'OL' }, { id: 'RT', x: 0.7, y: 0.6, team: 'offense', role: 'OL' }, { id: 'WR1', x: 0.1, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR2', x: 0.9, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR3', x: 0.2, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR4', x: 0.8, y: 0.55, team: 'offense', role: 'WR' }, { id: 'WR5', x: 0.4, y: 0.55, team: 'offense', role: 'WR' } ],
};
const DEFENSIVE_FORMATIONS: Formations = {
    '4-3-under': [ { id: 'DE1', x: 0.3, y: 0.5, team: 'defense', role: 'DE' }, { id: 'DT1', x: 0.4, y: 0.5, team: 'defense', role: 'DT' }, { id: 'DT2', x: 0.5, y: 0.5, team: 'defense', role: 'DT' }, { id: 'DE2', x: 0.6, y: 0.5, team: 'defense', role: 'DE' }, { id: 'LB1', x: 0.35, y: 0.4, team: 'defense', role: 'LB' }, { id: 'LB2', x: 0.55, y: 0.4, team: 'defense', role: 'LB' }, { id: 'LB3', x: 0.7, y: 0.35, team: 'defense', role: 'LB' }, { id: 'CB1', x: 0.08, y: 0.45, team: 'defense', role: 'CB' }, { id: 'CB2', x: 0.92, y: 0.45, team: 'defense', role: 'CB' }, { id: 'FS', x: 0.5, y: 0.2, team: 'defense', role: 'FS' }, { id: 'SS', x: 0.6, y: 0.3, team: 'defense', role: 'SS' } ],
    'nickel': [ { id: 'DE1', x: 0.35, y: 0.5, team: 'defense', role: 'DE' }, { id: 'DT1', x: 0.48, y: 0.5, team: 'defense', role: 'DT' }, { id: 'DT2', x: 0.6, y: 0.5, team: 'defense', role: 'DT' }, { id: 'DE2', x: 0.7, y: 0.5, team: 'defense', role: 'DE' }, { id: 'LB1', x: 0.4, y: 0.4, team: 'defense', role: 'LB' }, { id: 'LB2', x: 0.6, y: 0.4, team: 'defense', role: 'LB' }, { id: 'CB1', x: 0.1, y: 0.45, team: 'defense', role: 'CB' }, { id: 'CB2', x: 0.9, y: 0.45, team: 'defense', role: 'CB' }, { id: 'CB3', x: 0.25, y: 0.45, team: 'defense', role: 'CB' }, { id: 'FS', x: 0.4, y: 0.2, team: 'defense', role: 'FS' }, { id: 'SS', x: 0.6, y: 0.25, team: 'defense', role: 'SS' } ],
    'dime': [ { id: 'DE1', x: 0.4, y: 0.5, team: 'defense', role: 'DE' }, { id: 'DE2', x: 0.6, y: 0.5, team: 'defense', role: 'DE' }, { id: 'LB1', x: 0.5, y: 0.4, team: 'defense', role: 'LB' }, { id: 'CB1', x: 0.1, y: 0.45, team: 'defense', role: 'CB' }, { id: 'CB2', x: 0.9, y: 0.45, team: 'defense', role: 'CB' }, { id: 'CB3', x: 0.25, y: 0.45, team: 'defense', role: 'CB' }, { id: 'CB4', x: 0.75, y: 0.45, team: 'defense', role: 'CB' }, { id: 'FS1', x: 0.3, y: 0.2, team: 'defense', role: 'FS' }, { id: 'FS2', x: 0.7, y: 0.2, team: 'defense', role: 'FS' } ],
};

// --- FINAL, REWRITTEN RECOMMENDATION ENGINE ---
const getRecommendation = (gameState: { qtr: number, clock: number, down: number, ydstogo: number }) => {
    let score = 0;
    if (gameState.down === 3) score += 15; if (gameState.down === 4) score += 40;
    if (gameState.ydstogo <= 2) score += 10; if (gameState.ydstogo > 7) score += 5;
    if (gameState.qtr === 4) score += 20; if (gameState.clock < 120 && gameState.qtr % 2 === 0) score += 25;

    if (score > 50) { // CRITICAL
        return {
            plays: { 'play_go': { name: 'Go For It (QB Sneak)', formation: 'iform', rationale: "Highest probability play for short yardage." }, 'play_deep': { name: 'Deep Post', formation: 'shotgun', rationale: "High risk, high reward to get back in the game." }, 'play_sideline': { name: 'Sideline Comeback', formation: 'shotgun', rationale: "Stop the clock and gain yards." } },
            recommendedPlay: 'play_go', defensiveFormation: 'nickel',
            sidebarData: { tendency: "Strategy: CRITICAL", alerts: [{ title: "MUST CONVERT", subtitle: "High urgency situation", tag: "Critical", tagColor: "red" }] }
        };
    }
    if (score > 30) { // AGGRESSIVE
        return {
            plays: { 'play_boot': { name: 'PA Boot Right', formation: 'shotgun', rationale: "Use run threat to create passing lanes." }, 'play_screen': { name: 'WR Screen', formation: 'shotgun', rationale: "Counters an aggressive pass rush." }, 'play_seam': { name: 'TE Seam', formation: 'shotgun', rationale: "Exploit linebacker coverage." } },
            recommendedPlay: 'play_boot', defensiveFormation: 'nickel',
            sidebarData: { tendency: "Strategy: AGGRESSIVE", alerts: [{ title: "BLITZ POSSIBLE", subtitle: "Defense may bring pressure", tag: "High Risk", tagColor: "yellow" }] }
        };
    }
    // BALANCED
    return {
        plays: { 'play_dive': { name: 'HB Dive', formation: 'iform', rationale: "Establish a physical run game." }, 'play_offtackle': { name: 'Off-Tackle Run', formation: 'iform', rationale: "Test the edges of the defense." }, 'play_boot_lite': { name: 'Lite Play Action', formation: 'iform', rationale: "Safe pass to test coverage." } },
        recommendedPlay: 'play_dive', defensiveFormation: '4-3-under',
        sidebarData: { tendency: "Strategy: BALANCED", alerts: [{ title: "PHYSICAL START", subtitle: "Probe the D-Line", tag: "Low Risk", tagColor: "green" }] }
    };
};

const DEMO_STATES = [
    { down: 1, ydstogo: 10, clock: 800, qtr: 1 },
    { down: 3, ydstogo: 8, clock: 500, qtr: 3 },
    { down: 4, ydstogo: 1, clock: 100, qtr: 4 },
];

export default function Dashboard() {
    const [isDemoMode, setDemoMode] = useState(false);
    const [gameState, setGameState] = useState(DEMO_STATES[0]);
    const [activePlayId, setActivePlayId] = useState('');

    const recommendation = useMemo(() => getRecommendation(gameState), [gameState]);
    
    useEffect(() => {
        setActivePlayId(recommendation.recommendedPlay);
    }, [recommendation]);

    useEffect(() => {
        let scenarioTimeout: NodeJS.Timeout;
        if (isDemoMode) {
            let demoIndex = 0;
            const runScenario = () => {
                setGameState(DEMO_STATES[demoIndex]);
                demoIndex = (demoIndex + 1) % DEMO_STATES.length;
                scenarioTimeout = setTimeout(runScenario, 4000);
            };
            runScenario();
        }
        return () => clearTimeout(scenarioTimeout);
    }, [isDemoMode]);
    
    const formatClock = (seconds: number) => `${Math.floor(seconds / 60).toString().padStart(2, '0')}:${(seconds % 60).toString().padStart(2, '0')}`;

    const handleControlChange = (field: string, value: number) => {
        setDemoMode(false);
        setGameState(gs => ({...gs, [field]: value}));
    };
    
    const offensiveFormation = OFFENSIVE_FORMATIONS[recommendation.plays[activePlayId]?.formation] || OFFENSIVE_FORMATIONS['shotgun'];
    const currentDefensiveFormation = DEFENSIVE_FORMATIONS[recommendation.defensiveFormation];

    return (
        <div className="app-grid">
            <div className="sidebar left-sidebar">
                <div className="widget">
                    <div className="widget-header">GAME SIMULATION</div>
                    <div className="sim-control"><label>Down</label><select value={gameState.down} onChange={e => handleControlChange('down', parseInt(e.target.value))}>{[1,2,3,4].map(d => <option key={d} value={d}>{d}</option>)}</select></div>
                    <div className="sim-control"><label>Yards to Go: {gameState.ydstogo}</label><input type="range" min="1" max="25" value={gameState.ydstogo} onChange={e => handleControlChange('ydstogo', parseInt(e.target.value))} /></div>
                    <div className="sim-control"><label>Quarter</label><select value={gameState.qtr} onChange={e => handleControlChange('qtr', parseInt(e.target.value))}>{[1,2,3,4].map(q => <option key={q} value={q}>{q}</option>)}</select></div>
                    <div className="sim-control"><label>Time Remaining: {formatClock(gameState.clock)}</label><input type="range" min="0" max="900" step="1" value={gameState.clock} onChange={e => handleControlChange('clock', parseInt(e.target.value))} /></div>
                </div>
            </div>

            <div className="app-stage">
                <div className="top-bar">
                    <div className="score-pill">KC 24 - 21 BUF</div>
                    <div className="game-state">{gameState.qtr}Q | {formatClock(gameState.clock)} | {gameState.down} & {gameState.ydstogo}</div>
                    <div className="hud-controls"><button className="hud-btn" onClick={() => setDemoMode(!isDemoMode)}>{isDemoMode ? 'STOP DEMO' : 'START DEMO'}</button></div>
                </div>
                <div className="football-field-container">
                    <FootballField offensiveFormation={offensiveFormation} defensiveFormation={currentDefensiveFormation} />
                </div>
            </div>

            <RightSidebar 
                plays={recommendation.plays}
                selectedPlay={activePlayId}
                recommendedPlay={recommendation.recommendedPlay}
                sidebarData={recommendation.sidebarData}
                onPlaySelect={(playId) => {
                    setDemoMode(false);
                    setActivePlayId(playId);
                }}
            />
        </div>
    );
}
