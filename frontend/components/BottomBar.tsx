'use client';

import React from 'react';
import { Mic } from 'lucide-react';

export default function BottomBar() {
  return (
    <div className="absolute bottom-[140px] left-0 w-full flex justify-center pointer-events-none z-20">
      <div className="pointer-events-auto bg-slate-900/95 border border-white/10 rounded-2xl w-[640px] h-[60px] flex items-center justify-between px-4 shadow-2xl backdrop-blur-xl">
        
        {/* PLAY INFO */}
        <div className="flex flex-col">
          <span className="font-extrabold text-white text-base">PA BOOT RIGHT</span>
          <div className="flex gap-2 text-xs text-slate-400">
            <span className="font-mono text-blue-400 tracking-wider">BLUE 42</span>
            <span>• Success 78%</span>
          </div>
        </div>

        {/* TABS */}
        <div className="bg-white/5 rounded-full p-1 flex gap-1">
          <button className="px-3 py-1 rounded-full bg-blue-600 text-white text-xs font-bold transition-all">
            OFFENSE
          </button>
          <button className="px-3 py-1 rounded-full text-slate-400 hover:text-white text-xs font-bold transition-all">
            DEFENSE
          </button>
          <button className="px-3 py-1 rounded-full text-slate-400 hover:text-white text-xs font-bold transition-all">
            PERSONNEL
          </button>
        </div>

        {/* ACTIONS */}
        <div className="flex gap-2">
          <button className="w-9 h-9 rounded-lg bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors">
            <Mic size={18} className="text-white" />
          </button>
        </div>

      </div>
    </div>
  );
}