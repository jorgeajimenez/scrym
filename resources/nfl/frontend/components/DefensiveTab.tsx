import React from 'react';
import type { DefensiveResponse } from '@/types';

interface Props {
  data: DefensiveResponse;
}

export default function DefensiveTab({ data }: Props) {
  return (
    <div className="space-y-6">
      {/* Main Recommendation */}
      <div className="bg-gradient-to-r from-red-900 to-red-800 p-6 rounded-lg border-2 border-red-600">
        <h3 className="text-sm uppercase tracking-wide text-red-300 mb-2">Recommended Defense</h3>
        <p className="text-3xl font-bold text-white">{data.recommended_defense}</p>
      </div>

      {/* Play Type Prediction */}
      <div>
        <h4 className="text-lg font-semibold mb-4">Opponent Play Type Prediction</h4>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-blue-900 p-4 rounded-lg text-center">
            <p className="text-sm text-blue-300 mb-1">PASS Probability</p>
            <p className="text-4xl font-bold">{(data.pass_probability * 100).toFixed(1)}%</p>
          </div>
          <div className="bg-yellow-900 p-4 rounded-lg text-center">
            <p className="text-sm text-yellow-300 mb-1">RUN Probability</p>
            <p className="text-4xl font-bold">{(data.run_probability * 100).toFixed(1)}%</p>
          </div>
        </div>

        {/* Visual Indicator */}
        <div className="relative h-16 bg-gray-700 rounded-lg overflow-hidden">
          <div
            className="absolute left-0 top-0 h-full bg-blue-600 flex items-center justify-center transition-all"
            style={{ width: `${data.pass_probability * 100}%` }}
          >
            {data.pass_probability > 0.3 && (
              <span className="font-bold text-white">PASS</span>
            )}
          </div>
          <div
            className="absolute right-0 top-0 h-full bg-yellow-600 flex items-center justify-center transition-all"
            style={{ width: `${data.run_probability * 100}%` }}
          >
            {data.run_probability > 0.3 && (
              <span className="font-bold text-white">RUN</span>
            )}
          </div>
        </div>
      </div>

      {/* Defensive Strategy */}
      <div className="bg-gray-700 p-5 rounded-lg">
        <h4 className="font-semibold mb-3">Defensive Strategy</h4>
        <div className="space-y-2 text-sm">
          {data.pass_probability > 0.65 && (
            <div className="flex items-start gap-2">
              <span className="text-blue-400">▸</span>
              <p>High pass probability - consider extra DBs in nickel/dime packages</p>
            </div>
          )}
          {data.run_probability > 0.65 && (
            <div className="flex items-start gap-2">
              <span className="text-yellow-400">▸</span>
              <p>High run probability - stack the box with additional linebackers</p>
            </div>
          )}
          {data.pass_probability >= 0.35 && data.pass_probability <= 0.65 && (
            <div className="flex items-start gap-2">
              <span className="text-gray-400">▸</span>
              <p>Balanced situation - use base defense and read the play</p>
            </div>
          )}
        </div>
      </div>

      {/* Insight Box */}
      <div className="bg-gray-700 p-4 rounded-lg">
        <p className="text-sm text-gray-300">
          <strong>AI Insight:</strong> The opponent is predicted to run a{' '}
          <strong>{data.predicted_play_type}</strong> play with{' '}
          {(Math.max(data.pass_probability, data.run_probability) * 100).toFixed(0)}% confidence.
          Deploy <strong>{data.recommended_defense}</strong> to counter.
        </p>
      </div>
    </div>
  );
}
