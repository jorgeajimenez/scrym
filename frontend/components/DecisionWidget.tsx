'use client';

import React, { useState, useEffect } from 'react';
import { useGame } from '@/context/GameContext';
import { api } from '@/lib/api';
import { FourthDownResponse } from '@/types/api';

export default function DecisionWidget() {
  const { state } = useGame();
  const [data, setData] = useState<FourthDownResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
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
       <div className="decision-card" style={{ opacity: 0.5 }}>
          <div className="decision-header">ANALYZING...</div>
       </div>
    );
  }

  return (
    <div className="decision-card">
        <div className="decision-header">
            <span>4th Down Decision</span>
            <span className="risk-tag">RISK: LOW</span>
        </div>
        <div className="recommendation-badge" style={{ 
            background: data?.recommendation === 'GO' ? 'var(--emerald-400)' : 'var(--amber-400)'
        }}>
            {data?.recommendation === 'GO' ? 'GO FOR IT' : 'PUNT / KICK'}
        </div>
        <div className="metric-row">
            <span>Conversion Prob</span>
            <span className="metric-val" style={{ color: 'var(--emerald-400)' }}>
                {Math.round((data?.conversion_probability || 0) * 100)}%
            </span>
        </div>
        <div className="metric-row">
            <span>Exp Points (EPA)</span>
            <span className="metric-val">{data?.expected_epa.toFixed(2)}</span>
        </div>
        <div className="metric-row" style={{ border: 'none' }}>
            <span>Model Confidence</span>
            <span className="metric-val">92%</span>
        </div>
    </div>
  );
}
