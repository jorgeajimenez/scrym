export interface GameState {
  game_id: string;
  // Context
  qtr: number; // 1-4, 5 (OT)
  time_remaining: number; // Seconds (e.g., 900 for 15:00)
  play_clock: number; // Seconds (e.g., 40 or 25)
  clock_running: boolean; // Is the game clock currently ticking?
  score_home: number;
  score_away: number;
  possession: 'home' | 'away';
  
  // Field State
  down: number; // 1-4
  ydstogo: number; // Distance to 1st down
  yardline_100: number; // 0-100 (100 = Own Endzone, 0 = Opponent Endzone)
  
  // Logic Flags
  red_zone: boolean; // Calculated property (yardline_100 <= 20)
  goal_to_go: boolean;
  two_min_drill: boolean; // Calculated (time < 120 && qtrIsEnd)
  
  // Timeouts
  timeouts_home: number;
  timeouts_away: number;
  
  // For backend compatibility
  game_seconds_remaining?: number; 
  score_differential?: number;
  posteam_timeouts_remaining?: number;
  defteam_timeouts_remaining?: number;
}
