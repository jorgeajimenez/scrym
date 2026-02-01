'use client';

import React, { useState, useEffect } from 'react';
import { useGame } from '@/context/GameContext';
import { api } from '@/lib/api';
import { Mic } from 'lucide-react';

export default function DynamicIsland() {
  const { state } = useGame();
  const [activeTab, setActiveTab] = useState('offensive');
  const [playData, setPlayData] = useState<any>(null);

  useEffect(() => {
    if (activeTab === 'offensive') {
      api.predictOffense(state).then(setPlayData).catch(console.error);
    } else if (activeTab === 'defensive') {
      api.predictDefense(state).then(setPlayData).catch(console.error);
    }
  }, [activeTab, state.down, state.ydstogo]);

  return (
    <div className="hud-bottom">
        <div className="dynamic-island">
            <div className="play-info">
                <span className="play-name">{playData?.recommendation || 'PA BOOT RIGHT'}</span>
                <div className="play-meta">
                    <span className="wristband-code">{activeTab === 'offensive' ? 'BLUE 42' : 'RED 99'}</span>
                    <span>• {activeTab === 'offensive' ? 'Success' : 'Stop'} {Math.round((playData?.probabilities?.[playData?.recommendation] || 0.78) * 100)}%</span>
                </div>
            </div>

            <div className="context-tabs">
                <button 
                  className={`tab-btn ${activeTab === 'offensive' ? 'active offense' : ''}`}
                  onClick={() => setActiveTab('offensive')}
                >OFFENSE</button>
                <button 
                  className={`tab-btn ${activeTab === 'defensive' ? 'active defense' : ''}`}
                  onClick={() => setActiveTab('defensive')}
                >DEFENSE</button>
                <button 
                  className={`tab-btn ${activeTab === 'personnel' ? 'active' : ''}`}
                  onClick={() => setActiveTab('personnel')}
                >PERSONNEL</button>
            </div>

            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                <button className="hud-btn"><Mic size={18} /></button>
            </div>
        </div>
    </div>
  );
}