'use client';

import React from 'react';

interface CommandWidgetProps {
  title: string;
  children: React.ReactNode;
  type?: 'default' | 'critical';
}

export function CommandWidget({ title, children, type = 'default' }: CommandWidgetProps) {
  return (
    <div className={`h-full flex flex-col bg-slate-900 rounded border-2 ${type === 'critical' ? 'border-orange-500/50' : 'border-slate-800'} overflow-hidden shadow-2xl`}>
      <div className={`px-4 py-2 border-b-2 ${type === 'critical' ? 'bg-orange-950/20 border-orange-900/50' : 'bg-slate-900/50 border-slate-800'}`}>
        <h2 className={`font-bold uppercase tracking-wider text-xs ${type === 'critical' ? 'text-orange-400' : 'text-slate-400'}`}>
          {title}
        </h2>
      </div>
      <div className="p-4 flex-1 overflow-y-auto">
        {children}
      </div>
    </div>
  );
}
