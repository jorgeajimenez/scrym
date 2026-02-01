export interface FourthDownResponse {
  recommendation: 'GO' | 'PUNT/KICK';
  conversion_probability: number;
  fg_probability: number;
  expected_epa: number;
  win_probability: number;
}

export interface OffensiveResponse {
  recommendation: string;
  probabilities: Record<string, number>;
}

export interface DefensiveResponse {
  recommendation: 'Pass Defense' | 'Run Defense';
  pass_probability: number;
}

export interface PersonnelResponse {
  recommendation: string;
  probabilities: Record<string, number>;
}

export interface FormationResponse {
  formation_name: string;
  players: Array<{
    role: string;
    x: number;
    y: number;
    color: string;
  }>;
}

export interface AnalysisResponse {
  analysis: string;
}
