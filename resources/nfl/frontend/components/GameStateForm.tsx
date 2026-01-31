import React, { useState } from 'react';
import type { GameState } from '@/types';
import { apiClient } from '@/lib/api';

interface Props {
  gameState: GameState;
  setGameState: (state: GameState) => void;
  onPredict: () => void;
  loading: boolean;
}

const NFL_TEAMS = [
  'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
  'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
  'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
  'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS'
];

export default function GameStateForm({ gameState, setGameState, onPredict, loading }: Props) {
  const handleChange = (field: keyof GameState, value: string | number) => {
    setGameState({ ...gameState, [field]: value });
  };

  return (
    <div className="space-y-4">
      {/* Teams */}
      <div>
        <label className="block text-sm font-medium mb-1">Home Team</label>
        <select
          value={gameState.home_team}
          onChange={(e) => handleChange('home_team', e.target.value)}
          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
        >
          {NFL_TEAMS.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Away Team</label>
        <select
          value={gameState.away_team}
          onChange={(e) => handleChange('away_team', e.target.value)}
          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
        >
          {NFL_TEAMS.map((team) => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Possession</label>
        <select
          value={gameState.possession}
          onChange={(e) => handleChange('possession', e.target.value)}
          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
        >
          <option value={gameState.home_team}>{gameState.home_team}</option>
          <option value={gameState.away_team}>{gameState.away_team}</option>
        </select>
      </div>

      {/* Score */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">{gameState.home_team} Score</label>
          <input
            type="number"
            value={gameState.home_score}
            onChange={(e) => handleChange('home_score', parseInt(e.target.value) || 0)}
            min="0"
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">{gameState.away_team} Score</label>
          <input
            type="number"
            value={gameState.away_score}
            onChange={(e) => handleChange('away_score', parseInt(e.target.value) || 0)}
            min="0"
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          />
        </div>
      </div>

      {/* Quarter & Time */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Quarter</label>
          <select
            value={gameState.quarter}
            onChange={(e) => handleChange('quarter', parseInt(e.target.value))}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          >
            <option value={1}>Q1</option>
            <option value={2}>Q2</option>
            <option value={3}>Q3</option>
            <option value={4}>Q4</option>
            <option value={5}>OT</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Time (seconds)</label>
          <input
            type="number"
            value={gameState.time_remaining}
            onChange={(e) => handleChange('time_remaining', parseInt(e.target.value) || 0)}
            min="0"
            max="3600"
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          />
        </div>
      </div>

      {/* Down & Distance */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Down</label>
          <select
            value={gameState.down}
            onChange={(e) => handleChange('down', parseInt(e.target.value))}
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          >
            <option value={1}>1st</option>
            <option value={2}>2nd</option>
            <option value={3}>3rd</option>
            <option value={4}>4th</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Distance</label>
          <input
            type="number"
            value={gameState.distance}
            onChange={(e) => handleChange('distance', parseInt(e.target.value) || 1)}
            min="1"
            max="99"
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          />
        </div>
      </div>

      {/* Field Position */}
      <div>
        <label className="block text-sm font-medium mb-1">Yards from Opponent Goal</label>
        <input
          type="number"
          value={gameState.yard_line}
          onChange={(e) => handleChange('yard_line', parseInt(e.target.value) || 1)}
          min="1"
          max="99"
          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
        />
      </div>

      {/* Timeouts */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Home TOs</label>
          <input
            type="number"
            value={gameState.home_timeouts}
            onChange={(e) => handleChange('home_timeouts', parseInt(e.target.value) || 0)}
            min="0"
            max="3"
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Away TOs</label>
          <input
            type="number"
            value={gameState.away_timeouts}
            onChange={(e) => handleChange('away_timeouts', parseInt(e.target.value) || 0)}
            min="0"
            max="3"
            className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 text-white"
          />
        </div>
      </div>

      {/* Analyze Button */}
      <button
        onClick={onPredict}
        disabled={loading}
        className={`w-full py-3 rounded-lg font-bold text-sm uppercase tracking-wide transition ${
          loading
            ? 'bg-gray-600 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 active:scale-95 shadow-lg'
        }`}
      >
        {loading ? 'Processing Analytics...' : 'Analyze Situation'}
      </button>
    </div>
  );
}
