import React from 'react';
import type { PersonnelResponse } from '@/types';

interface Props {
  data: PersonnelResponse;
}

export default function PersonnelTab({ data }: Props) {
  const sortedPersonnel = Object.entries(data.probabilities)
    .sort(([, a], [, b]) => b - a);

  const getPersonnelDescription = (code: string) => {
    const descriptions: Record<string, string> = {
      '11': '1 RB, 1 TE, 3 WR - Spread offense',
      '12': '1 RB, 2 TE, 2 WR - Balanced attack',
      '21': '2 RB, 1 TE, 2 WR - Power running',
      '13': '1 RB, 3 TE, 1 WR - Goal line / Short yardage',
      '22': '2 RB, 2 TE, 1 WR - Heavy run formation',
      '10': '1 RB, 0 TE, 4 WR - Maximum spread',
    };
    return descriptions[code] || 'Custom personnel package';
  };

  return (
    <div className="space-y-6">
      {/* Main Recommendation */}
      <div className="bg-gradient-to-r from-blue-900 to-blue-800 p-6 rounded-lg border-2 border-blue-600">
        <h3 className="text-sm uppercase tracking-wide text-blue-300 mb-2">Recommended Personnel</h3>
        <p className="text-5xl font-bold text-white mb-2">{data.recommended_personnel} PERSONNEL</p>
        <p className="text-blue-200 text-lg">{getPersonnelDescription(data.recommended_personnel)}</p>
      </div>

      {/* Reasoning */}
      <div className="bg-gray-700 p-5 rounded-lg">
        <h4 className="font-semibold mb-2">Why This Personnel?</h4>
        <p className="text-gray-300">{data.reasoning}</p>
      </div>

      {/* Personnel Probabilities */}
      <div>
        <h4 className="text-lg font-semibold mb-4">Personnel Package Analysis</h4>
        <div className="space-y-3">
          {sortedPersonnel.map(([personnel, prob]) => {
            const isRecommended = personnel === data.recommended_personnel;
            return (
              <div key={personnel} className={isRecommended ? 'bg-blue-900/30 p-3 rounded-lg' : ''}>
                <div className="flex justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-lg">{personnel}</span>
                    <span className="text-sm text-gray-400">{getPersonnelDescription(personnel)}</span>
                    {isRecommended && <span className="text-blue-400 text-xs">★ BEST</span>}
                  </div>
                  <span className="text-gray-400">{(prob * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all ${
                      isRecommended ? 'bg-blue-500' : 'bg-gray-500'
                    }`}
                    style={{ width: `${prob * 100}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Personnel Guide */}
      <div className="bg-gray-700 p-5 rounded-lg">
        <h4 className="font-semibold mb-3">Personnel Package Guide</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div className="bg-gray-800 p-3 rounded">
            <p className="font-bold text-blue-400">11 Personnel</p>
            <p className="text-gray-400">Best for: Passing situations, spread offense</p>
          </div>
          <div className="bg-gray-800 p-3 rounded">
            <p className="font-bold text-blue-400">12 Personnel</p>
            <p className="text-gray-400">Best for: Balanced offense, play-action</p>
          </div>
          <div className="bg-gray-800 p-3 rounded">
            <p className="font-bold text-blue-400">21 Personnel</p>
            <p className="text-gray-400">Best for: Power running, short yardage</p>
          </div>
          <div className="bg-gray-800 p-3 rounded">
            <p className="font-bold text-blue-400">13 Personnel</p>
            <p className="text-gray-400">Best for: Goal line, heavy formations</p>
          </div>
        </div>
      </div>

      {/* Insight Box */}
      <div className="bg-gray-700 p-4 rounded-lg">
        <p className="text-sm text-gray-300">
          <strong>AI Insight:</strong> The <strong>{data.recommended_personnel} personnel</strong> package
          is optimal for this situation with{' '}
          {(sortedPersonnel[0][1] * 100).toFixed(0)}% confidence. This formation provides
          the best matchup advantage based on down, distance, and field position.
        </p>
      </div>
    </div>
  );
}
