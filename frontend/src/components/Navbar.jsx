import React from 'react';

export default function Navbar({ stats, apiHealthy, user, onLogout }) {
  return (
    <header className="control-navbar">
      <div className="nav-brand">
        <div className="brand-glow-dot"></div>
        <span className="brand-text">WarehouseMind AI</span>
        <span className="brand-badge">Control Tower</span>
      </div>

      <div className="nav-stats">
        <div className="stat-pill">
          <span className="stat-label">Workers</span>
          <span className="stat-value">{stats.activeWorkers}/{stats.totalWorkers}</span>
        </div>
        <div className="stat-pill">
          <span className="stat-label">Robots Active</span>
          <span className="stat-value">{stats.activeRobots}/{stats.totalRobots}</span>
        </div>
        <div className="stat-pill warning">
          <span className="stat-label">Stock Alerts</span>
          <span className="stat-value">{stats.stockAlerts}</span>
        </div>
        <div className="stat-pill error">
          <span className="stat-label">High Priority</span>
          <span className="stat-value">{stats.highPriorityOrders}</span>
        </div>
      </div>

      <div className="nav-status">
        {user && (
          <span className="user-badge">{user.full_name} ({user.role})</span>
        )}
        <div className={`status-dot ${apiHealthy ? 'healthy' : 'disconnected'}`}></div>
        <span className="status-text">{apiHealthy ? 'CONNECTED TO CLOUD' : 'DISCONNECTED'}</span>
        <span className="model-badge">Gemini 2.5 Flash</span>
        {onLogout && (
          <button type="button" className="logout-btn" onClick={onLogout}>
            Logout
          </button>
        )}
      </div>
    </header>
  );
}
