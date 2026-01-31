import React from 'react';
import type { FourthDownResponse } from '@/types';

interface Props {
  data: FourthDownResponse;
}

export default function FourthDownTab({ data }: Props) {
  const decisions = Object.entries(data.expected_values).sort(([, a], [, b]) => b - a);
  const bestDecision = decisions[0];

  return (
    <div className="space-y-6">
      {/* Main Recommendation */}
      <div className="bg-gradient-to-r from-yellow-900 to-yellow-800 p-6 rounded-lg border-2 border-yellow-600">
        <h3 className="text-sm uppercase tracking-wide text-yellow-300 mb-2">4th Down Decision</h3>
        <p className="text-4xl font-bold text-white">{data.recommendation.toUpperCase().replace('_', ' ')}</p>
        <p className="text-yellow-200 mt-2">
          Expected Value: <span className="text-2xl font-bold">{bestDecision[1].toFixed(2)}</span> points
        </p>
      </div>

      {/* Decision Comparison */}
      <div>
        <h4 className="text-lg font-semibold mb-4">Decision Expected Values</h4>
        <div className="space-y-3">
          {decisions.map(([decision, value]) => {
            const isRecommended = decision === data.recommendation;
            return (
              <div key={decision}>
                <div className="flex justify-between mb-1">
                  <span className="font-medium">
                    {decision.replace('_', ' ').toUpperCase()}
                    {isRecommended && <span className="ml-2 text-yellow-400">★ RECOMMENDED</span>}
                  </span>
                  <span className="text-gray-400">{value.toFixed(2)} pts</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-4">
                  <div
                    className={`h-4 rounded-full transition-all ${
                      isRecommended ? 'bg-yellow-500' : 'bg-gray-500'
                    }`}
                    style={{ width: `${(value / Math.max(...decisions.map(([, v]) => v))) * 100}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Probabilities */}
      {(data.go_for_it_prob !== undefined || data.field_goal_prob !== undefined) && (
        <div className="grid grid-cols-2 gap-4">
          {data.go_for_it_prob !== undefined && (
            <div className="bg-green-900 p-4 rounded-lg text-center">
              <p className="text-sm text-green-300 mb-1">Conversion Probability</p>
              <p className="text-3xl font-bold">{(data.go_for_it_prob * 100).toFixed(1)}%</p>
            </div>
          )}
          {data.field_goal_prob !== undefined && (
            <div className="bg-blue-900 p-4 rounded-lg text-center">
              <p className="text-sm text-blue-300 mb-1">FG Success Probability</p>
              <p className="text-3xl font-bold">{(data.field_goal_prob * 100).toFixed(1)}%</p>
            </div>
          )}
        </div>
      )}

      {/* Insight Box */}
      <div className="bg-gray-700 p-4 rounded-lg">
        <p className="text-sm text-gray-300">
          <strong>AI Insight:</strong> The recommended decision is to{' '}
          <strong>{data.recommendation.replace('_', ' ')}</strong> with an expected value of{' '}
          <strong>{bestDecision[1].toFixed(2)}</strong> points. This maximizes your scoring opportunity
          while considering conversion probability and field position.
        </p>
      </div>

      {/* Decision Tree Visual */}
      <div className="bg-gray-700 p-4 rounded-lg">
        <h4 className="font-semibold mb-3 text-center">Decision Tree</h4>
        <div className="flex justify-around items-center text-center">
          {decisions.map(([decision, value]) => (
            <div
              key={decision}
              className={`p-3 rounded-lg ${
                decision === data.recommendation
                  ? 'bg-yellow-600 ring-2 ring-yellow-400'
                  : 'bg-gray-600'
              }`}
            >
              <p className="text-xs uppercase">{decision.replace('_', ' ')}</p>
              <p className="text-lg font-bold">{value.toFixed(2)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
