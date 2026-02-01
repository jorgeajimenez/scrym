'use client';

import React from 'react';
import { Player } from './FootballField'; // Assuming Player type is exported from FootballField

interface DataPanelProps {
  players: Player[];
}

export default function DataPanel({ players }: DataPanelProps) {
  return (
    <div className="data-panel">
      <div className="data-panel-header">LIVE ENTITY DATA STREAM</div>
      <div className="data-table">
        <div className="data-table-header">
          <span>PLAYER</span>
          <span>TEAM</span>
          <span>X</span>
          <span>Y</span>
        </div>
        <div className="data-table-body">
          {players.map(p => (
            <div key={p.id} className="data-table-row">
              <span>{p.role || p.id}</span>
              <span className={p.team === 'offense' ? 'text-blue' : 'text-red'}>{p.team.toUpperCase()}</span>
              <span>{p.x.toFixed(2)}</span>
              <span>{p.y.toFixed(2)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
