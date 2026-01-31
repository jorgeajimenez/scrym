import React from 'react';
import type { OffensivePlayResponse } from '@/types';

interface Props {
  data: OffensivePlayResponse;
}

export default function OffensiveTab({ data }: Props) {
  const sortedPlays = Object.entries(data.probabilities)
    .sort(([, a], [, b]) => b - a);

  return (
    <div className="space-y-6">
      {/* Main Recommendation */}
      <div className="bg-gradient-to-r from-green-900 to-green-800 p-6 rounded-lg border-2 border-green-600">
        <h3 className="text-sm uppercase tracking-wide text-green-300 mb-2">Recommended Play</h3>
        <p className="text-4xl font-bold text-white">{data.recommended_play.toUpperCase()}</p>
        <div className="mt-4 flex items-center gap-4">
          <div>
            <span className="text-green-300 text-sm">Confidence:</span>
            <span className="text-2xl font-bold ml-2">{(data.confidence * 100).toFixed(1)}%</span>
          </div>
          <div>
            <span className="text-green-300 text-sm">Expected EPA:</span>
            <span className="text-2xl font-bold ml-2">+{data.expected_epa.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Play Probabilities Chart */}
      <div>
        <h4 className="text-lg font-semibold mb-4">Play Type Probabilities</h4>
        <div className="space-y-3">
          {sortedPlays.map(([play, prob]) => (
            <div key={play}>
              <div className="flex justify-between mb-1">
                <span className="font-medium">{play.charAt(0).toUpperCase() + play.slice(1)}</span>
                <span className="text-gray-400">{(prob * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-3">
                <div
                  className={`h-3 rounded-full transition-all ${
                    play === data.recommended_play ? 'bg-green-500' : 'bg-gray-500'
                  }`}
                  style={{ width: `${prob * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Insight Box */}
      <div className="bg-gray-700 p-4 rounded-lg">
        <p className="text-sm text-gray-300">
          <strong>AI Insight:</strong> Based on the current game situation,
          a {data.recommended_play} play has the highest success probability
          ({(data.confidence * 100).toFixed(0)}%) and is expected to gain{' '}
          {data.expected_epa.toFixed(2)} expected points added.
        </p>
      </div>
    </div>
  );
}
