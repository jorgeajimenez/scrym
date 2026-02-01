'use client';

import React from 'react';
import { PlayCircle } from 'lucide-react';

export default function ChallengePanel() {
  return (
    <div className="challenge-panel">
        <div className="challenge-left">
            {/* Live Video Stream Mock */}
            <video 
              autoPlay 
              muted 
              loop 
              playsInline
              style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.8 }}
            >
              <source src="https://assets.mixkit.co/videos/preview/mixkit-american-football-players-playing-a-match-4643-large.mp4" type="video/mp4" />
            </video>
            <div style={{ position: 'absolute', top: '5px', left: '5px', background: 'red', color: 'white', fontSize: '8px', padding: '2px 4px', fontWeight: 'bold' }}>LIVE REPLAY</div>
            <PlayCircle className="replay-icon" size={24} style={{ opacity: 0.5 }} />
        </div>
        <div className="challenge-center">
            <div className="challenge-title">Challenge Assistant • Spot of Ball</div>
            <div className="challenge-decision">
                <button className="decision-btn challenge">CHALLENGE</button>
                <button className="decision-btn no">DO NOT CHALLENGE</button>
            </div>
        </div>
        <div className="challenge-stats">
            <div className="stat-row">
                <span>Overturn Prob</span>
                <span className="metric-val" style={{ color: 'var(--emerald-400)' }}>84%</span>
            </div>
            <div className="confidence-bar">
                <div className="confidence-fill" style={{ width: '84%' }}></div>
            </div>
            <div className="stat-row" style={{ marginTop: '8px' }}>
                <span>Timeout Cost</span>
                <span className="metric-val" style={{ color: 'var(--red-600)' }}>-1 TO</span>
            </div>
            <div className="stat-row">
                <span>Exp Value</span>
                <span className="metric-val">+2.4 pts</span>
            </div>
        </div>
    </div>
  );
}
