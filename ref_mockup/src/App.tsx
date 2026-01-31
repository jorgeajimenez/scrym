import { FootballField } from './components/FootballField';
import { CommandWidget } from './components/CommandWidget';
import { FlagSystem } from './components/FlagSystem';
import { Play, Shield, Users, AlertTriangle, Radio, Video, Settings } from 'lucide-react';
import { useState } from 'react';

type ViewMode = 'offensive' | 'defensive' | 'fourth-down' | 'personnel';

export default function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('offensive');
  const [winProbability, setWinProbability] = useState(67);
  const [fourthDownDecision, setFourthDownDecision] = useState<'go' | 'punt' | 'fg'>('go');
  const [flagStatus, setFlagStatus] = useState<'none' | 'yellow' | 'red-prelim' | 'red-final'>('red-prelim');

  return (
    <div className="h-screen w-screen bg-slate-950 overflow-hidden flex flex-col">
      {/* Top Bar - Score */}
      <div className="bg-slate-900 border-b-2 border-slate-800 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded"></div>
            <div>
              <div className="text-xs text-slate-500 uppercase tracking-wide">Home</div>
              <div className="text-white font-bold">Kansas City Chiefs</div>
            </div>
            <div className="text-4xl font-bold text-white ml-4">24</div>
          </div>
          <div className="text-slate-600 text-2xl">-</div>
          <div className="flex items-center gap-3">
            <div className="text-4xl font-bold text-white mr-4">21</div>
            <div>
              <div className="text-xs text-slate-500 uppercase tracking-wide">Away</div>
              <div className="text-white font-bold">Buffalo Bills</div>
            </div>
            <div className="w-10 h-10 bg-red-600 rounded"></div>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <div className="text-right">
            <div className="text-slate-500 text-xs uppercase tracking-wide">Quarter</div>
            <div className="text-white font-bold text-lg">3rd</div>
          </div>
          <div className="text-right">
            <div className="text-slate-500 text-xs uppercase tracking-wide">Time</div>
            <div className="text-white font-bold text-lg font-mono">8:45</div>
          </div>
          <div className="text-right">
            <div className="text-slate-500 text-xs uppercase tracking-wide">Down</div>
            <div className="text-white font-bold text-lg">2nd & 7</div>
          </div>
        </div>
        
        {/* QB Comm Channel - Inconspicuous */}
        <button className="flex items-center gap-2 px-3 py-1 bg-slate-800 hover:bg-slate-700 rounded border border-slate-700 transition-colors">
          <Radio size={14} className="text-green-500" />
          <span className="text-slate-400 text-xs font-mono">QB COMM</span>
        </button>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - 1/3 width */}
        <div className="w-1/3 flex flex-col gap-4 p-4 border-r-2 border-slate-800">
          {/* Video Stream */}
          <div className="bg-black rounded border-2 border-slate-700 overflow-hidden shadow-xl h-64">
            <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 relative">
              <Video className="text-slate-600 mb-2" size={40} strokeWidth={1.5} />
              <span className="text-slate-500 font-semibold text-sm tracking-wide">LIVE GAME FEED</span>
              <div className="absolute top-3 right-3 bg-red-600 text-white text-xs px-3 py-1 rounded-sm font-bold flex items-center gap-1">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                LIVE
              </div>
            </div>
          </div>

          {/* Win Probability - Compact */}
          <div className="bg-slate-900 rounded border-2 border-slate-700 p-4">
            <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-3">Win Probability</div>
            <div className="flex items-center gap-4">
              <div className="relative w-24 h-24">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="35" fill="none" stroke="#1e293b" strokeWidth="10" />
                  <circle
                    cx="50" cy="50" r="35" fill="none"
                    stroke={winProbability >= 60 ? '#10b981' : '#f59e0b'}
                    strokeWidth="10"
                    strokeDasharray={`${winProbability * 2.2} 220`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <div className={`text-3xl font-bold ${winProbability >= 60 ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {winProbability}
                  </div>
                  <div className="text-slate-500 text-[10px] font-semibold">PERCENT</div>
                </div>
              </div>
              <div className="flex-1">
                <div className="text-xs text-slate-500 mb-1">YDS/PLAY</div>
                <div className="text-white font-bold text-xl mb-2">6.2</div>
                <div className="text-xs text-slate-500 mb-1">3RD DOWN CONV</div>
                <div className="text-emerald-400 font-bold">8/13 <span className="text-slate-500">62%</span></div>
              </div>
            </div>
          </div>

          {/* Configuration */}
          <div className="flex-1 bg-slate-900 rounded border-2 border-slate-700 overflow-hidden">
            <div className="border-b-2 border-slate-800 px-4 py-2 bg-slate-900/50">
              <div className="flex items-center gap-2">
                <Settings className="text-slate-400" size={16} />
                <h2 className="font-bold text-white uppercase tracking-wide text-xs">Configuration</h2>
              </div>
            </div>
            
            <div className="p-4 overflow-y-auto" style={{ maxHeight: 'calc(100% - 42px)' }}>
              {/* Game Context */}
              <div className="mb-4 pb-4 border-b border-slate-800">
                <h3 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2">Game Context</h3>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Season</span>
                    <span className="text-white font-semibold">2025-2026</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Week</span>
                    <span className="text-white font-semibold">Week 12</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Game Type</span>
                    <span className="text-white font-semibold">Regular Season</span>
                  </div>
                </div>
              </div>

              {/* Conditions */}
              <div className="mb-4 pb-4 border-b border-slate-800">
                <h3 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2">Conditions</h3>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Weather</span>
                    <span className="text-white">Clear, 68°F</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Wind</span>
                    <span className="text-white">5 mph SW</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Field</span>
                    <span className="text-white">Turf (Indoor)</span>
                  </div>
                </div>
              </div>

              {/* AI Settings */}
              <div className="mb-4 pb-4 border-b border-slate-800">
                <h3 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2">AI Parameters</h3>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between mb-1">
                      <label className="text-slate-400 text-xs">Confidence</label>
                      <span className="text-white font-mono text-xs">75%</span>
                    </div>
                    <input 
                      type="range" 
                      min="0" max="100" defaultValue="75" 
                      className="w-full h-1 bg-slate-700 rounded appearance-none cursor-pointer accent-blue-600"
                    />
                  </div>

                  <div>
                    <label className="text-slate-400 text-xs block mb-1">Risk Tolerance</label>
                    <div className="grid grid-cols-3 gap-1">
                      <button className="bg-slate-800 text-slate-400 py-1 rounded text-[10px] font-semibold border border-slate-700">Low</button>
                      <button className="bg-blue-900 border-2 border-blue-600 text-white py-1 rounded text-[10px] font-bold">Med</button>
                      <button className="bg-slate-800 text-slate-400 py-1 rounded text-[10px] font-semibold border border-slate-700">High</button>
                    </div>
                  </div>
                </div>
              </div>

              {/* System Features */}
              <div>
                <h3 className="text-slate-400 text-[10px] font-bold uppercase tracking-wider mb-2">System Features</h3>
                <div className="space-y-1">
                  <label className="flex items-center gap-2 text-slate-300 text-xs py-1 px-2 hover:bg-slate-800/50 rounded cursor-pointer">
                    <input type="checkbox" className="w-3 h-3 accent-blue-600" defaultChecked />
                    <span>Auto-suggest plays</span>
                  </label>
                  <label className="flex items-center gap-2 text-slate-300 text-xs py-1 px-2 hover:bg-slate-800/50 rounded cursor-pointer">
                    <input type="checkbox" className="w-3 h-3 accent-blue-600" defaultChecked />
                    <span>Real-time probability</span>
                  </label>
                  <label className="flex items-center gap-2 text-slate-300 text-xs py-1 px-2 hover:bg-slate-800/50 rounded cursor-pointer">
                    <input type="checkbox" className="w-3 h-3 accent-blue-600" />
                    <span>Voice commands</span>
                  </label>
                  <label className="flex items-center gap-2 text-slate-300 text-xs py-1 px-2 hover:bg-slate-800/50 rounded cursor-pointer">
                    <input type="checkbox" className="w-3 h-3 accent-blue-600" defaultChecked />
                    <span>Opposition analysis</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel - 2/3 width */}
        <div className="w-2/3 flex flex-col p-4 gap-3">
          {/* Tab Navigation */}
          <div className="flex gap-2">
            <button
              onClick={() => setViewMode('offensive')}
              className={`px-6 py-3 rounded-t font-bold text-sm uppercase tracking-wide transition-all ${
                viewMode === 'offensive'
                  ? 'bg-blue-600 text-white border-2 border-blue-500'
                  : 'bg-slate-800 text-slate-400 border-2 border-slate-700 hover:bg-slate-700'
              }`}
            >
              Offensive Coordinator
            </button>
            <button
              onClick={() => setViewMode('defensive')}
              className={`px-6 py-3 rounded-t font-bold text-sm uppercase tracking-wide transition-all ${
                viewMode === 'defensive'
                  ? 'bg-red-600 text-white border-2 border-red-500'
                  : 'bg-slate-800 text-slate-400 border-2 border-slate-700 hover:bg-slate-700'
              }`}
            >
              Defensive Coordinator
            </button>
            <button
              onClick={() => setViewMode('fourth-down')}
              className={`px-6 py-3 rounded-t font-bold text-sm uppercase tracking-wide transition-all ${
                viewMode === 'fourth-down'
                  ? 'bg-orange-600 text-white border-2 border-orange-500'
                  : 'bg-slate-800 text-slate-400 border-2 border-slate-700 hover:bg-slate-700'
              }`}
            >
              4th Down
            </button>
            <button
              onClick={() => setViewMode('personnel')}
              className={`px-6 py-3 rounded-t font-bold text-sm uppercase tracking-wide transition-all ${
                viewMode === 'personnel'
                  ? 'bg-purple-600 text-white border-2 border-purple-500'
                  : 'bg-slate-800 text-slate-400 border-2 border-slate-700 hover:bg-slate-700'
              }`}
            >
              Personnel & Formation
            </button>
          </div>

          {/* Content Area */}
          <div className="flex-1 flex gap-3 overflow-hidden">
            {/* Coordinator Widget */}
            <div className="w-80 flex-shrink-0">
              {viewMode === 'offensive' && (
                <CommandWidget title="Offensive Play Call">
                  <div className="space-y-4">
                    <div className="bg-blue-900/40 border border-blue-700 rounded p-3">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-white font-bold">PA BOOT RT</span>
                        <Play size={16} className="text-blue-400" />
                      </div>
                      <div className="text-xs text-slate-400 mb-3">Shotgun - 11 Personnel</div>
                      <div className="grid grid-cols-3 gap-3 text-xs mb-3">
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">Success</div>
                          <div className="text-emerald-400 font-bold text-lg">78%</div>
                        </div>
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">Exp Yds</div>
                          <div className="text-white font-bold text-lg">8.3</div>
                        </div>
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">TD</div>
                          <div className="text-amber-400 font-bold text-lg">12%</div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button className="flex-1 bg-emerald-700 hover:bg-emerald-600 text-white text-sm py-2 rounded font-bold uppercase tracking-wide">
                          Approve
                        </button>
                        <button className="px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm py-2 rounded font-semibold uppercase border border-slate-700">
                          Alt
                        </button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Alternative Plays</div>
                      <div className="bg-slate-800/50 border border-slate-700 rounded p-2 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="text-white font-semibold">Slant Concept</span>
                          <span className="text-slate-400">72%</span>
                        </div>
                      </div>
                      <div className="bg-slate-800/50 border border-slate-700 rounded p-2 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="text-white font-semibold">Draw Play</span>
                          <span className="text-slate-400">68%</span>
                        </div>
                      </div>
                      <div className="bg-slate-800/50 border border-slate-700 rounded p-2 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="text-white font-semibold">Screen Left</span>
                          <span className="text-slate-400">65%</span>
                        </div>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-700">
                      <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Matchup Advantages</div>
                      <div className="text-xs text-slate-300 space-y-1">
                        <div>• WR1 vs CB2 (Speed mismatch)</div>
                        <div>• TE vs LB (Size advantage)</div>
                        <div>• OL vs DL (Run blocking +2)</div>
                      </div>
                    </div>
                  </div>
                </CommandWidget>
              )}

              {viewMode === 'defensive' && (
                <CommandWidget title="Defensive Play Call">
                  <div className="space-y-4">
                    <div className="bg-red-900/40 border border-red-700 rounded p-3">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-white font-bold">COVER 3</span>
                        <Shield size={16} className="text-red-400" />
                      </div>
                      <div className="text-xs text-slate-400 mb-3">4-3 Base - Zone Blitz</div>
                      <div className="grid grid-cols-3 gap-3 text-xs mb-3">
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">vs Pass</div>
                          <div className="text-emerald-400 font-bold text-lg">82%</div>
                        </div>
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">vs Run</div>
                          <div className="text-amber-400 font-bold text-lg">64%</div>
                        </div>
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">Pressure</div>
                          <div className="text-white font-bold text-lg">28%</div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button className="flex-1 bg-emerald-700 hover:bg-emerald-600 text-white text-sm py-2 rounded font-bold uppercase tracking-wide">
                          Approve
                        </button>
                        <button className="px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm py-2 rounded font-semibold uppercase border border-slate-700">
                          Alt
                        </button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Alternative Defenses</div>
                      <div className="bg-slate-800/50 border border-slate-700 rounded p-2 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="text-white font-semibold">Cover 2 Man</span>
                          <span className="text-slate-400">79%</span>
                        </div>
                      </div>
                      <div className="bg-slate-800/50 border border-slate-700 rounded p-2 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="text-white font-semibold">Nickel Blitz</span>
                          <span className="text-slate-400">74%</span>
                        </div>
                      </div>
                      <div className="bg-slate-800/50 border border-slate-700 rounded p-2 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="text-white font-semibold">Prevent Defense</span>
                          <span className="text-slate-400">71%</span>
                        </div>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-700">
                      <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Tendency Analysis</div>
                      <div className="text-xs text-slate-300 space-y-1">
                        <div>• QB prefers quick throws (68%)</div>
                        <div>• Run likely on 2nd & short (72%)</div>
                        <div>• TE targeted in red zone (45%)</div>
                      </div>
                    </div>
                  </div>
                </CommandWidget>
              )}

              {viewMode === 'fourth-down' && (
                <CommandWidget title="4th Down Decision" type="critical">
                  <div className="space-y-4">
                    <div className="flex gap-2">
                      <button 
                        onClick={() => setFourthDownDecision('go')}
                        className={`flex-1 py-3 rounded font-bold text-sm uppercase tracking-wide transition-all ${
                          fourthDownDecision === 'go' 
                            ? 'bg-emerald-700 text-white border-2 border-emerald-500' 
                            : 'bg-slate-800 text-slate-400 border-2 border-slate-700 hover:bg-slate-700'
                        }`}
                      >
                        Go
                      </button>
                      <button 
                        onClick={() => setFourthDownDecision('punt')}
                        className={`flex-1 py-3 rounded font-bold text-sm uppercase tracking-wide transition-all ${
                          fourthDownDecision === 'punt' 
                            ? 'bg-amber-700 text-white border-2 border-amber-500' 
                            : 'bg-slate-800 text-slate-400 border-2 border-slate-700 hover:bg-slate-700'
                        }`}
                      >
                        Punt
                      </button>
                      <button 
                        onClick={() => setFourthDownDecision('fg')}
                        className={`flex-1 py-3 rounded font-bold text-sm uppercase tracking-wide transition-all ${
                          fourthDownDecision === 'fg' 
                            ? 'bg-blue-700 text-white border-2 border-blue-500' 
                            : 'bg-slate-800 text-slate-400 border-2 border-slate-700 hover:bg-slate-700'
                        }`}
                      >
                        FG
                      </button>
                    </div>

                    <div className="bg-slate-900/50 border border-slate-700 rounded p-4">
                      {fourthDownDecision === 'go' && (
                        <>
                          <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="text-center">
                              <div className="text-slate-500 text-xs mb-1">Convert %</div>
                              <div className="text-emerald-400 font-bold text-3xl">64%</div>
                            </div>
                            <div className="text-center">
                              <div className="text-slate-500 text-xs mb-1">Exp Points</div>
                              <div className="text-white font-bold text-3xl">+2.8</div>
                            </div>
                          </div>
                          <div className="text-xs text-slate-400 space-y-1">
                            <div>• Avg yards to gain: 2.1</div>
                            <div>• Defense allows 3.8 YPC</div>
                            <div>• O-line push rate: 71%</div>
                          </div>
                        </>
                      )}
                      {fourthDownDecision === 'punt' && (
                        <>
                          <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="text-center">
                              <div className="text-slate-500 text-xs mb-1">Net Yards</div>
                              <div className="text-amber-400 font-bold text-3xl">42</div>
                            </div>
                            <div className="text-center">
                              <div className="text-slate-500 text-xs mb-1">Exp Points</div>
                              <div className="text-white font-bold text-3xl">-0.3</div>
                            </div>
                          </div>
                          <div className="text-xs text-slate-400 space-y-1">
                            <div>• Pin inside 20: 38%</div>
                            <div>• Touchback risk: 12%</div>
                            <div>• Avg return: 8.2 yards</div>
                          </div>
                        </>
                      )}
                      {fourthDownDecision === 'fg' && (
                        <>
                          <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="text-center">
                              <div className="text-slate-500 text-xs mb-1">Make %</div>
                              <div className="text-blue-400 font-bold text-3xl">88%</div>
                            </div>
                            <div className="text-center">
                              <div className="text-slate-500 text-xs mb-1">Exp Points</div>
                              <div className="text-white font-bold text-3xl">+2.6</div>
                            </div>
                          </div>
                          <div className="text-xs text-slate-400 space-y-1">
                            <div>• Distance: 47 yards</div>
                            <div>• Kicker: 12/15 from 40-49</div>
                            <div>• Wind factor: Minimal</div>
                          </div>
                        </>
                      )}
                    </div>

                    <div className="bg-emerald-900/30 border border-emerald-700 rounded p-3">
                      <div className="text-xs font-bold text-emerald-400 mb-1">AI RECOMMENDATION</div>
                      <div className="text-white font-bold text-lg">GO FOR IT</div>
                      <div className="text-xs text-slate-400 mt-1">Win probability increases 4.2% on conversion</div>
                    </div>
                  </div>
                </CommandWidget>
              )}

              {viewMode === 'personnel' && (
                <CommandWidget title="Personnel & Formation">
                  <div className="space-y-4">
                    <div className="bg-purple-900/40 border border-purple-700 rounded p-3">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-white font-bold">SHOTGUN</span>
                        <Users size={16} className="text-purple-400" />
                      </div>
                      <div className="text-xs text-slate-400 mb-3">1 RB, 1 TE, 3 WR</div>
                      <div className="grid grid-cols-2 gap-3 text-xs mb-3">
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">Personnel</div>
                          <div className="text-white font-bold text-lg">11</div>
                        </div>
                        <div className="text-center">
                          <div className="text-slate-500 mb-1">Success</div>
                          <div className="text-emerald-400 font-bold text-lg">71%</div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button className="flex-1 bg-emerald-700 hover:bg-emerald-600 text-white text-sm py-2 rounded font-bold uppercase tracking-wide">
                          Set
                        </button>
                        <button className="px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm py-2 rounded font-semibold uppercase border border-slate-700">
                          Edit
                        </button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Quick Select</div>
                      <div className="grid grid-cols-2 gap-2">
                        <button className="bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded p-2 text-xs text-white font-semibold">
                          I-Formation
                        </button>
                        <button className="bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded p-2 text-xs text-white font-semibold">
                          Spread
                        </button>
                        <button className="bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded p-2 text-xs text-white font-semibold">
                          Ace
                        </button>
                        <button className="bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded p-2 text-xs text-white font-semibold">
                          Trips
                        </button>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-700">
                      <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Active Personnel</div>
                      <div className="space-y-1 text-xs">
                        <div className="flex justify-between p-2 bg-slate-800/50 rounded">
                          <span className="text-slate-300">QB - P. Mahomes</span>
                          <span className="text-emerald-400">98 OVR</span>
                        </div>
                        <div className="flex justify-between p-2 bg-slate-800/50 rounded">
                          <span className="text-slate-300">RB - I. Pacheco</span>
                          <span className="text-blue-400">84 OVR</span>
                        </div>
                        <div className="flex justify-between p-2 bg-slate-800/50 rounded">
                          <span className="text-slate-300">WR - T. Hill</span>
                          <span className="text-emerald-400">96 OVR</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CommandWidget>
              )}
            </div>

            {/* Football Field - FULL SIZE */}
            <div className="flex-1 min-w-0 flex flex-col gap-3">
              <div className="flex-1 bg-slate-900 rounded border-2 border-slate-700 p-3 shadow-2xl overflow-hidden">
                <FootballField />
              </div>

              {/* Flag System */}
              <FlagSystem 
                status={{
                  type: flagStatus,
                  call: flagStatus !== 'none' ? 'Offensive Pass Interference' : '',
                  reviewable: flagStatus === 'red-prelim'
                }}
                onRequestReview={() => {
                  setFlagStatus('red-final');
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}