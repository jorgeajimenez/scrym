import React from 'react';
import type { WinProbabilityResponse } from '@/types';

interface Props {
  data: WinProbabilityResponse;
}

export default function WinProbabilityTab({ data }: Props) {
  const getLeverageColor = (leverage: string) => {
    switch (leverage.toLowerCase()) {
      case 'high':
        return 'text-red-400';
      case 'medium':
        return 'text-yellow-400';
      default:
        return 'text-green-400';
    }
  };

  const getWPColor = (wp: number) => {
    if (wp >= 70) return 'from-green-900 to-green-700';
    if (wp >= 55) return 'from-blue-900 to-blue-700';
    if (wp >= 45) return 'from-yellow-900 to-yellow-700';
    if (wp >= 30) return 'from-orange-900 to-orange-700';
    return 'from-red-900 to-red-700';
  };

  return (
    <div className="space-y-6">
      {/* Win Probability Gauge */}
      <div className={`bg-gradient-to-r ${getWPColor(data.possession_team_win_prob)} p-8 rounded-lg border-2 border-purple-600`}>
        <h3 className="text-sm uppercase tracking-wide text-purple-300 mb-2 text-center">Win Probability</h3>
        <div className="text-center">
          <p className="text-7xl font-bold text-white mb-2">
            {data.possession_team_win_prob.toFixed(1)}%
          </p>
          <p className="text-purple-200 text-lg">Possession Team</p>
        </div>
      </div>

      {/* Both Teams */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-green-900 p-5 rounded-lg text-center">
          <p className="text-sm text-green-300 mb-2">POSSESSION TEAM</p>
          <p className="text-4xl font-bold">{data.possession_team_win_prob.toFixed(1)}%</p>
        </div>
        <div className="bg-red-900 p-5 rounded-lg text-center">
          <p className="text-sm text-red-300 mb-2">OPPONENT</p>
          <p className="text-4xl font-bold">{data.opponent_win_prob.toFixed(1)}%</p>
        </div>
      </div>

      {/* Visual Win Probability Bar */}
      <div>
        <h4 className="text-lg font-semibold mb-3">Win Probability Distribution</h4>
        <div className="relative h-20 bg-gray-700 rounded-lg overflow-hidden">
          <div
            className="absolute left-0 top-0 h-full bg-green-600 flex items-center justify-center transition-all"
            style={{ width: `${data.possession_team_win_prob}%` }}
          >
            {data.possession_team_win_prob > 20 && (
              <span className="font-bold text-white">
                {data.possession_team_win_prob.toFixed(0)}%
              </span>
            )}
          </div>
          <div
            className="absolute right-0 top-0 h-full bg-red-600 flex items-center justify-center transition-all"
            style={{ width: `${data.opponent_win_prob}%` }}
          >
            {data.opponent_win_prob > 20 && (
              <span className="font-bold text-white">
                {data.opponent_win_prob.toFixed(0)}%
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Leverage Indicator */}
      <div className="bg-gray-700 p-5 rounded-lg">
        <div className="flex justify-between items-center">
          <h4 className="font-semibold">Play Leverage</h4>
          <span className={`text-2xl font-bold ${getLeverageColor(data.leverage)}`}>
            {data.leverage.toUpperCase()}
          </span>
        </div>
        <p className="text-sm text-gray-400 mt-2">
          {data.leverage === 'High' && 'This is a critical moment - the outcome of this play significantly impacts win probability.'}
          {data.leverage === 'Medium' && 'This play has moderate importance in determining the game outcome.'}
          {data.leverage === 'Low' && 'This play has minimal impact on the overall game outcome.'}
        </p>
      </div>

      {/* Win Probability Explanation */}
      <div className="bg-gray-700 p-4 rounded-lg">
        <h4 className="font-semibold mb-2">What This Means</h4>
        <div className="space-y-2 text-sm text-gray-300">
          {data.possession_team_win_prob >= 80 && (
            <p>• The possession team has a commanding advantage and should play conservatively to protect their lead.</p>
          )}
          {data.possession_team_win_prob >= 60 && data.possession_team_win_prob < 80 && (
            <p>• The possession team has a strong position but should remain aggressive to maintain control.</p>
          )}
          {data.possession_team_win_prob >= 40 && data.possession_team_win_prob < 60 && (
            <p>• This is a toss-up game - every decision matters. Consider high-value, aggressive plays.</p>
          )}
          {data.possession_team_win_prob < 40 && (
            <p>• The possession team is trailing and needs aggressive play-calling to shift momentum.</p>
          )}
          <p className="pt-2 border-t border-gray-600">
            <strong>AI Insight:</strong> With {data.possession_team_win_prob.toFixed(0)}% win probability,
            the possession team should{' '}
            {data.possession_team_win_prob > 55 ? 'focus on maintaining possession and running clock' :
             data.possession_team_win_prob < 45 ? 'be aggressive and take calculated risks' :
             'balance aggression with smart decision-making'}.
          </p>
        </div>
      </div>
    </div>
  );
}
