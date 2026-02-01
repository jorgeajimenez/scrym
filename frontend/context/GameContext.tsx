'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { GameState } from '@/types';

interface GameContextType {
  state: GameState;
  updateState: (newState: Partial<GameState>) => void;
  resetClock: () => void;
  toggleClock: () => void;
}

const DEFAULT_STATE: GameState = {
  game_id: 'demo_001',
  qtr: 3,
  time_remaining: 8 * 60 + 45, // 08:45
  play_clock: 40,
  clock_running: true,
  score_home: 24,
  score_away: 21,
  possession: 'home',
  down: 4,
  ydstogo: 2,
  yardline_100: 42,
  red_zone: false,
  goal_to_go: false,
  two_min_drill: false,
  timeouts_home: 3,
  timeouts_away: 3
};

const GameContext = createContext<GameContextType | undefined>(undefined);

export function GameProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<GameState>(DEFAULT_STATE);

  const updateState = (updates: Partial<GameState>) => {
    setState(prev => ({ ...prev, ...updates }));
  };

  const toggleClock = () => {
    updateState({ clock_running: !state.clock_running });
  };

  const resetClock = () => {
    updateState({ play_clock: 40 });
  };

  // The Heartbeat
  useEffect(() => {
    if (!state.clock_running) return;

    const interval = setInterval(() => {
      setState(prev => {
        const newTime = Math.max(0, prev.time_remaining - 1);
        const newPlayClock = Math.max(0, prev.play_clock - 1);
        
        // Auto-stop at 0
        if (newTime === 0) return { ...prev, time_remaining: 0, clock_running: false };
        
        return {
          ...prev,
          time_remaining: newTime,
          play_clock: newPlayClock
        };
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [state.clock_running]);

  return (
    <GameContext.Provider value={{ state, updateState, resetClock, toggleClock }}>
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  const context = useContext(GameContext);
  if (context === undefined) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
}
