'use client';

import { useState } from 'react';
import GameStateForm from '@/components/GameStateForm';
import OffensiveTab from '@/components/OffensiveTab';
import DefensiveTab from '@/components/DefensiveTab';
import FourthDownTab from '@/components/FourthDownTab';
import WinProbabilityTab from '@/components/WinProbabilityTab';
import PersonnelTab from '@/components/PersonnelTab';
import type { GameState, AllPredictionsResponse } from '@/types';
import { apiClient } from '@/lib/api';

export default function Home() {
  const [gameState, setGameState] = useState<GameState>({
    home_team: 'KC',
    away_team: 'SF',
    possession: 'KC',
    quarter: 2,
    time_remaining: 120,
    down: 2,
    distance: 10,
    yard_line: 50,
    home_score: 14,
    away_score: 17,
    home_timeouts: 3,
    away_timeouts: 2,
  });

  const [predictions, setPredictions] = useState<AllPredictionsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'offensive' | 'defensive' | 'fourth-down' | 'win-prob' | 'personnel'>('offensive');

  const handlePredict = async () => {
    setLoading(true);
    setError(null);

    try {
      const results = await apiClient.predictAll(gameState);
      setPredictions(results);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get predictions. Make sure the backend is running.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const scoreInfo = `${gameState.home_team} ${gameState.home_score} - ${gameState.away_score} ${gameState.away_team}`;
  const situation = `${getOrdinal(gameState.down)} & ${gameState.distance}`;

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 via-slate-900 to-gray-900">
      {/* Professional Header */}
      <header className="bg-gradient-to-r from-blue-900 to-blue-800 border-b-4 border-blue-600 shadow-2xl">
        <div className="max-w-7xl mx-auto py-8 px-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-black text-white tracking-tight uppercase">
                AI Coach Decision System
              </h1>
              <p className="text-blue-200 mt-2 font-semibold">Advanced Analytics & Real-Time Strategy</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-white">{scoreInfo}</div>
              <div className="text-xl text-blue-200 mt-1">Q{gameState.quarter} | {situation}</div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Sidebar: Game State Input */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 rounded-lg shadow-2xl border border-gray-700 sticky top-6">
              <div className="bg-gradient-to-r from-gray-700 to-gray-800 px-6 py-4 border-b border-gray-600">
                <h2 className="text-xl font-bold text-white uppercase tracking-wide">Game Situation</h2>
              </div>
              <div className="p-6">
                <GameStateForm
                  gameState={gameState}
                  setGameState={setGameState}
                  onPredict={handlePredict}
                  loading={loading}
                />

                {error && (
                  <div className="mt-4 p-4 bg-red-900/50 border border-red-700 rounded-lg">
                    <p className="text-red-200 text-sm font-medium">{error}</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Main Panel: Predictions */}
          <div className="lg:col-span-3">
            <div className="bg-gray-800 rounded-lg shadow-2xl border border-gray-700">
              {/* Professional Tab Navigation */}
              <div className="bg-gradient-to-r from-gray-700 to-gray-800 px-6 py-2 border-b border-gray-600">
                <div className="flex flex-wrap gap-1">
                  <TabButton
                    active={activeTab === 'offensive'}
                    onClick={() => setActiveTab('offensive')}
                    color="green"
                  >
                    Offensive Strategy
                  </TabButton>
                  <TabButton
                    active={activeTab === 'defensive'}
                    onClick={() => setActiveTab('defensive')}
                    color="red"
                  >
                    Defensive Analysis
                  </TabButton>
                  {gameState.down === 4 && (
                    <TabButton
                      active={activeTab === 'fourth-down'}
                      onClick={() => setActiveTab('fourth-down')}
                      color="yellow"
                    >
                      4th Down Decision
                    </TabButton>
                  )}
                  <TabButton
                    active={activeTab === 'win-prob'}
                    onClick={() => setActiveTab('win-prob')}
                    color="purple"
                  >
                    Win Probability
                  </TabButton>
                  <TabButton
                    active={activeTab === 'personnel'}
                    onClick={() => setActiveTab('personnel')}
                    color="blue"
                  >
                    Personnel Package
                  </TabButton>
                </div>
              </div>

              {/* Tab Content */}
              <div className="p-8">
                {!predictions && !loading && (
                  <div className="text-center py-16">
                    <div className="text-gray-500 mb-4">
                      <svg className="w-20 h-20 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <p className="text-gray-400 text-lg font-medium">
                      Configure game situation and click "Analyze" to receive AI-powered coaching recommendations
                    </p>
                  </div>
                )}

                {loading && (
                  <div className="text-center py-16">
                    <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-blue-500 border-t-transparent"></div>
                    <p className="text-gray-400 mt-6 text-lg font-medium">Processing game analytics...</p>
                  </div>
                )}

                {predictions && !loading && (
                  <>
                    {activeTab === 'offensive' && predictions.offensive && (
                      <OffensiveTab data={predictions.offensive} />
                    )}
                    {activeTab === 'defensive' && predictions.defensive && (
                      <DefensiveTab data={predictions.defensive} />
                    )}
                    {activeTab === 'fourth-down' && predictions.fourth_down && (
                      <FourthDownTab data={predictions.fourth_down} />
                    )}
                    {activeTab === 'win-prob' && predictions.win_probability && (
                      <WinProbabilityTab data={predictions.win_probability} />
                    )}
                    {activeTab === 'personnel' && predictions.personnel && (
                      <PersonnelTab data={predictions.personnel} />
                    )}
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

// Professional Tab Button Component
function TabButton({
  active,
  onClick,
  children,
  color
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
  color: 'green' | 'red' | 'yellow' | 'purple' | 'blue';
}) {
  const colorClasses = {
    green: active ? 'bg-green-700 text-white border-green-500' : 'bg-gray-700 text-gray-300 border-gray-600 hover:bg-gray-600',
    red: active ? 'bg-red-700 text-white border-red-500' : 'bg-gray-700 text-gray-300 border-gray-600 hover:bg-gray-600',
    yellow: active ? 'bg-yellow-700 text-white border-yellow-500' : 'bg-gray-700 text-gray-300 border-gray-600 hover:bg-gray-600',
    purple: active ? 'bg-purple-700 text-white border-purple-500' : 'bg-gray-700 text-gray-300 border-gray-600 hover:bg-gray-600',
    blue: active ? 'bg-blue-700 text-white border-blue-500' : 'bg-gray-700 text-gray-300 border-gray-600 hover:bg-gray-600',
  };

  return (
    <button
      onClick={onClick}
      className={`px-4 py-3 font-bold text-sm uppercase tracking-wide transition-all border-b-4 ${colorClasses[color]} ${active ? 'shadow-lg' : ''}`}
    >
      {children}
    </button>
  );
}

function getOrdinal(n: number): string {
  const s = ['th', 'st', 'nd', 'rd'];
  const v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}
