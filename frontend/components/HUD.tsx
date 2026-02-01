'use client';

import React, { useState, useEffect } from 'react';
import { useGame } from '@/context/GameContext';
import { api } from '@/lib/api';
import { Settings, Eye, Bell } from 'lucide-react';

export default function HUD() {
  const { state } = useGame();
  const [winProb, setWinProb] = useState(67);

  const formatTime = (sec: number) => {
    const m = Math.floor(sec / 60).toString().padStart(2, '0');
    const s = (sec % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  useEffect(() => {
    // Periodically update win prob from backend
    if (state.down === 4) {
      api.predictFourthDown(state).then(res => {
        setWinProb(Math.round(res.win_probability * 100));
      }).catch(() => {});
    }
  }, [state.time_remaining]); // Update as clock ticks

  return (
    <div className="hud-top">
      {/* SCORE PILL */}
      <div className="score-pill">
          <span style={{ color: 'var(--blue-600)' }}>KC {state.score_home}</span>
          <div className="score-divider"></div>
          <span style={{ color: 'var(--red-600)' }}>BUF {state.score_away}</span>
          <div className="score-divider"></div>
          <span className="clock-display">
            {formatTime(state.time_remaining)}
          </span>
          <span style={{ fontSize: '0.7rem', color: 'var(--slate-400)', marginLeft: '0.5rem' }}>
            Q{state.qtr}
          </span>
      </div>

      {/* Win Prob Gauge V2 */}
      <div className="win-prob-widget">
          <div style={{ fontSize: '0.6rem', color: 'var(--slate-400)', letterSpacing: '1px', textTransform: 'uppercase' }}>
              Win Probability
          </div>
          <div className="prob-main" style={{ color: 'var(--white)' }}>{winProb}%</div>
          <div className="prob-bar">
              <div className="prob-fill" style={{ width: `${winProb}%` }}></div>
          </div>
          <div className="prob-stats">
              <span>MOMENTUM: +2.4</span>
              <span>COMEBACK: 12%</span>
          </div>
      </div>

      <div className="hud-controls">
          <button className="hud-btn" onClick={() => {
             const drawer = document.getElementById('config-drawer');
             drawer?.classList.toggle('open');
          }}><Settings size={18} /></button>
          <button className="hud-btn"><Eye size={18} /></button>
          <button className="hud-btn" style={{ position: 'relative' }}>
              <Bell size={18} />
              <div className="notification-dot"></div>
          </button>
      </div>
    </div>
  );
}