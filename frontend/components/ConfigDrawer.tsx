'use client';

import React from 'react';
import { X } from 'lucide-react';

export default function ConfigDrawer() {
  const closeDrawer = () => {
    const drawer = document.getElementById('config-drawer');
    drawer?.classList.remove('open');
  };

  return (
    <div className="config-drawer" id="config-drawer">
        <div className="drawer-header">
            <span>SETTINGS</span>
            <X className="close-config" style={{ cursor: 'pointer' }} size={20} onClick={closeDrawer} />
        </div>
        <div className="config-group">
            <label>Offensive Formation</label>
            <select id="formation-select">
                <option value="shotgun">Shotgun</option>
                <option value="empty">Empty</option>
                <option value="iform">I-Form</option>
                <option value="singleback">Singleback</option>
            </select>
        </div>
        <div className="config-group">
            <label>Risk Profile</label>
            <select>
                <option>Standard</option>
                <option>Aggressive (Go for 4th)</option>
                <option>Conservative</option>
            </select>
        </div>
        <div className="config-group">
            <label>Vision Sensitivity</label>
            <input type="range" className="slider" />
        </div>
    </div>
  );
}