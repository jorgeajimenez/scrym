'use client';

import { CheckCircle } from 'lucide-react';

// --- TYPE DEFINITIONS ---
interface Play { name: string; formation: string; rationale: string; }
interface Alert { title: string; subtitle: string; tag: string; tagColor: string; }
interface SidebarData { tendency: string; alerts: Alert[]; }
interface RightSidebarProps {
    plays: { [key: string]: Play };
    selectedPlay: string;
    recommendedPlay: string;
    sidebarData: SidebarData;
    onPlaySelect: (playId: string) => void;
}

// --- COMPONENT ---
export default function RightSidebar({ plays, selectedPlay, recommendedPlay, sidebarData, onPlaySelect }: RightSidebarProps) {
    const getTagColor = (color: string) => {
        if (color === 'green') return 'bg-emerald-400 text-emerald-900';
        if (color === 'yellow') return 'bg-amber-400 text-amber-900';
        if (color === 'red') return 'bg-red-600 text-white';
        if (color === 'blue') return 'bg-blue-600 text-white';
        return 'bg-slate-400 text-slate-900';
    }

    return (
        <div className="sidebar right-sidebar">
            <div className="widget">
                <div className="widget-header">COACH'S RADAR</div>
                <div className="tendency-alert">
                    <div className="alert-title">Tendency Alert</div>
                    <p>{sidebarData.tendency}</p>
                </div>
                {sidebarData.alerts.map((alert, index) => (
                    <div key={index} className="play-card">
                        <div>
                            <div className="play-title">{alert.title}</div>
                            <div className="play-subtitle">{alert.subtitle}</div>
                        </div>
                        <div className={`play-tag ${getTagColor(alert.tagColor)}`}>{alert.tag}</div>
                    </div>
                ))}
            </div>

            <div className="widget">
                <div className="widget-header">MODEL RECOMMENDATIONS</div>
                <div className="play-options-container">
                    {Object.entries(plays).map(([playId, playData]) => (
                        <div
                            key={playId}
                            className={`play-select-item ${selectedPlay === playId ? 'selected' : ''}`}
                            onClick={() => onPlaySelect(playId)}
                        >
                            {playData.name}
                            {recommendedPlay === playId && (
                                <span className="suggested-tag">SUGGESTED</span>
                            )}
                        </div>
                    ))}
                </div>
                {selectedPlay && plays[selectedPlay] && (
                    <div className="confirmation-message">
                        <CheckCircle size={24} className="check-icon" />
                        <div>
                            <span className="confirmation-subtitle">Why "{plays[selectedPlay].name}" Works:</span>
                            <p className="rationale">{plays[selectedPlay].rationale}</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
