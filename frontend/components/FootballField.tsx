'use client';

import React, { useEffect, useRef } from 'react';

// --- TYPE DEFINITIONS ---
export interface Player {
  id: string;
  x: number;
  y: number;
  team: 'offense' | 'defense';
  role?: string;
}

export type Formations = {
  [key: string]: Player[];
};

interface FootballFieldProps {
  offensiveFormation: Player[];
  defensiveFormation: Player[];
}

// --- COMPONENT ---
export default function FootballField({ offensiveFormation, defensiveFormation }: FootballFieldProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const players = [...offensiveFormation, ...defensiveFormation];

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const container = canvas.parentElement;
        if (!container) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const draw = (width: number, height: number) => {
            ctx.clearRect(0, 0, width, height);

            // Field Background
            let g = ctx.createLinearGradient(0, 0, 0, height);
            g.addColorStop(0, '#020617'); g.addColorStop(0.3, '#064e3b'); g.addColorStop(1, '#065f46');
            ctx.fillStyle = g; ctx.fillRect(0, 0, width, height);

            // Yard Lines
            ctx.strokeStyle = 'rgba(255,255,255,0.1)';
            ctx.lineWidth = 2;
            for (let i = 1; i < 10; i++) {
                let y = (i / 10) * height;
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
            }
            // Line of Scrimmage & First Down
            ctx.strokeStyle = '#3b82f6'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(0, height * 0.6); ctx.lineTo(width, height * 0.6); ctx.stroke();
            ctx.strokeStyle = '#fbbf24';
            ctx.beginPath(); ctx.moveTo(0, height * 0.5); ctx.lineTo(width, height * 0.5); ctx.stroke();
            
            // Render Players (Statically)
            players.forEach(p => {
                let x = p.x * width;
                let y = p.y * height;
                ctx.fillStyle = p.team === 'offense' ? '#60a5fa' : '#ef4444';
                ctx.beginPath(); ctx.arc(x, y, 8, 0, Math.PI * 2); ctx.fill();
                ctx.strokeStyle = 'white'; ctx.lineWidth = 1.5; ctx.stroke();
            });
        };
        
        const resizeObserver = new ResizeObserver(entries => {
            if (!entries || entries.length === 0) return;
            const { width, height } = entries[0].contentRect;
            canvas.width = width;
            canvas.height = height;
            draw(width, height);
        });

        resizeObserver.observe(container);

        // Initial Draw
        const { width, height } = container.getBoundingClientRect();
        draw(width, height);

        return () => {
            resizeObserver.disconnect();
        };
    }, [offensiveFormation, defensiveFormation, players]);

    return <canvas ref={canvasRef} />;
}