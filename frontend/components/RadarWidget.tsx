'use client';

import React from 'react';

export default function RadarWidget() {
  return (
    <div className="radar-widget">
        <svg viewBox="0 0 100 100" style={{ width: '100%', height: '100%' }}>
            <polygon points="50,10 90,40 70,80 30,80 10,40" fill="rgba(0,0,0,0.5)"
                stroke="rgba(255,255,255,0.2)" />
            <path d="M50 50 L50 10 M50 50 L90 40 M50 50 L70 80 M50 50 L30 80 M50 50 L10 40"
                stroke="rgba(255,255,255,0.1)" />
            <polygon points="50,15 80,45 65,75 35,70 20,45" fill="rgba(220,38,38,0.4)" stroke="#ef4444"
                strokeWidth="2" />
            <text x="50" y="55" fill="white" fontSize="8" textAnchor="middle" fontWeight="bold"
                opacity="0.5">DEF</text>
        </svg>
    </div>
  );
}