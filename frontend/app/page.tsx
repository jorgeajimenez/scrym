'use client';

import React from 'react';
import { GameProvider } from '@/context/GameContext';
import Dashboard from '@/components/Dashboard';

export default function Home() {
  return (
    <GameProvider>
      <Dashboard />
    </GameProvider>
  );
}
