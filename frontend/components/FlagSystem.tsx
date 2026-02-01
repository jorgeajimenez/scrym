'use client';

import React from 'react';
import { AlertTriangle } from 'lucide-react';

interface FlagSystemProps {
  status: {
    type: 'none' | 'yellow' | 'red-prelim' | 'red-final';
    call: string;
    reviewable: boolean;
  };
  onRequestReview: () => void;
}

export function FlagSystem({ status, onRequestReview }: FlagSystemProps) {
  if (status.type === 'none') return null;

  const isRed = status.type.startsWith('red');

  return (
    <div className={`p-4 rounded border-2 flex items-center justify-between animate-in fade-in slide-in-from-bottom-4 duration-500 ${
      isRed ? 'bg-red-950/30 border-red-500/50' : 'bg-yellow-950/30 border-yellow-500/50'
    }`}>
      <div className="flex items-center gap-4">
        <div className={`p-2 rounded-full ${isRed ? 'bg-red-500 text-white' : 'bg-yellow-500 text-black'}`}>
          <AlertTriangle size={20} />
        </div>
        <div>
          <div className={`text-[10px] font-bold uppercase tracking-widest ${isRed ? 'text-red-400' : 'text-yellow-400'}`}>
            {isRed ? 'Challenge Recommendation' : 'Penalty Flag'}
          </div>
          <div className="text-white font-bold text-lg leading-tight">{status.call}</div>
        </div>
      </div>
      
      {status.reviewable && (
        <button 
          onClick={onRequestReview}
          className="bg-white text-black font-black px-6 py-2 rounded text-xs uppercase tracking-tight hover:bg-slate-200 transition-colors"
        >
          Request AI Review
        </button>
      )}
    </div>
  );
}
