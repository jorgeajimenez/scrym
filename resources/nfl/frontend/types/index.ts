// TypeScript types for NFL AI Coach frontend

export interface GameState {
  home_team: string;
  away_team: string;
  possession: string;
  quarter: number;
  time_remaining: number;
  down: number;
  distance: number;
  yard_line: number;
  home_score: number;
  away_score: number;
  home_timeouts: number;
  away_timeouts: number;
}

export interface OffensivePlayResponse {
  recommended_play: string;
  probabilities: Record<string, number>;
  expected_epa: number;
  confidence: number;
}

export interface DefensiveResponse {
  predicted_play_type: string;
  pass_probability: number;
  run_probability: number;
  recommended_defense: string;
}

export interface FourthDownResponse {
  recommendation: string;
  go_for_it_prob?: number;
  field_goal_prob?: number;
  expected_values: Record<string, number>;
}

export interface WinProbabilityResponse {
  possession_team_win_prob: number;
  opponent_win_prob: number;
  leverage: string;
}

export interface PersonnelResponse {
  recommended_personnel: string;
  probabilities: Record<string, number>;
  reasoning: string;
}

export interface AllPredictionsResponse {
  offensive?: OffensivePlayResponse;
  defensive?: DefensiveResponse;
  fourth_down?: FourthDownResponse;
  win_probability?: WinProbabilityResponse;
  personnel?: PersonnelResponse;
}
