'use client';

import React, { useState, useEffect } from 'react';
import { useGame } from '@/context/GameContext';
import { api } from '@/lib/api';
import { FourthDownResponse } from '@/types/api';

export default function TrafficLight() {
  const { state } = useGame();
  const [data, setData] = useState<FourthDownResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Only fetch on 4th down
    if (state.down === 4) {
      setLoading(true);
      api.predictFourthDown(state)
        .then(res => {
          setData(res);
          setLoading(false);
        })
        .catch(err => {
          console.error(err);
          setLoading(false);
        });
    } else {
      setData(null);
    }
  }, [state.down, state.ydstogo, state.yardline_100]);

  if (!data && !loading) return null;

  if (loading) {
    return (
      <div className="absolute top-24 left-4 bg-slate-900/90 border border-white/10 rounded-lg p-4 w-56 animate-pulse pointer-events-auto">
        <div className="text-xs font-bold text-slate-400 mb-2">CALCULATING...</div>
        <div className="h-8 bg-slate-700 rounded mb-2"></div>
        <div className="h-4 bg-slate-700 rounded w-1/2"></div>
      </div>
    );
  }

  // Determine color based on recommendation
  const getTheme = () => {
    if (data?.recommendation === 'GO') return {
      bg: 'bg-emerald-500',
      text: 'text-emerald-950',
      border: 'border-emerald-400/30',
      glow: 'shadow-[0_0_20px_rgba(16,185,129,0.4)]',
      iconColor: 'text-emerald-400'
    };
    if (data?.recommendation === 'PUNT/KICK') return {
      bg: 'bg-amber-500',
      text: 'text-amber-950',
      border: 'border-amber-400/30',
      glow: 'shadow-[0_0_20px_rgba(245,158,11,0.4)]',
      iconColor: 'text-amber-400'
    };
    return {
      bg: 'bg-blue-500',
      text: 'text-white',
      border: 'border-blue-400/30',
      glow: 'shadow-[0_0_20px_rgba(59,130,246,0.4)]',
      iconColor: 'text-blue-400'
    };
  };

  const theme = getTheme();

  return (
    <div className="absolute top-36 left-6 pointer-events-auto z-20 group">
      <div className="bg-slate-900/95 backdrop-blur-2xl border border-white/10 rounded-2xl p-5 w-64 shadow-[0_20px_50px_rgba(0,0,0,0.5)] transition-all duration-500 group-hover:border-white/20 group-hover:translate-y-[-2px]">
        <div className="flex justify-between items-center mb-4">
          <div className="flex flex-col">
            <span className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Strategy Engine</span>
            <span className="text-xs font-bold text-white">4th Down Decision</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-[8px] font-bold text-slate-500 uppercase mb-1">Risk Profile</span>
            <span className="bg-amber-500/10 text-amber-500 border border-amber-500/20 text-[9px] font-black px-2 py-0.5 rounded-full uppercase tracking-tighter">Medium</span>
          </div>
        </div>
        
        <div className={`relative overflow-hidden ${theme.bg} ${theme.text} ${theme.glow} rounded-xl py-4 mb-5 text-center transition-all duration-500`}>
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-white/20 to-transparent pointer-events-none"></div>
          <span className="relative z-10 text-2xl font-black italic tracking-tighter uppercase">{data?.recommendation}</span>
        </div>

        <div className="space-y-3">
          <div className="flex flex-col">
            <div className="flex justify-between items-end mb-1">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Success Probability</span>
              <span className={`text-sm font-black ${theme.iconColor}`}>{(data!.conversion_probability * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
               <div 
                 className={`h-full ${theme.bg} transition-all duration-1000 ease-out`}
                 style={{ width: `${data!.conversion_probability * 100}%` }}
               ></div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-white/5">
            <div className="flex flex-col">
              <span className="text-[9px] font-bold text-slate-500 uppercase mb-1">Expected EPA</span>
              <span className="text-xs font-bold text-white">{data?.expected_epa.toFixed(2)}</span>
            </div>
            <div className="flex flex-col items-end">
              <span className="text-[9px] font-bold text-slate-500 uppercase mb-1">WP Impact</span>
              <span className="text-xs font-bold text-blue-400">+{((data!.win_probability - 0.5)*10).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-center gap-2 opacity-50">
           <div className="w-1 h-1 rounded-full bg-slate-500"></div>
           <span className="text-[8px] font-bold text-slate-500 uppercase tracking-widest">Model: neural_4d_v2.1</span>
           <div className="w-1 h-1 rounded-full bg-slate-500"></div>
        </div>
      </div>
      
      {/* DECORATIVE CORNER */}
      <div className="absolute -top-1 -left-1 w-4 h-4 border-t-2 border-l-2 border-white/20 rounded-tl-lg pointer-events-none"></div>
    </div>
  );
}
