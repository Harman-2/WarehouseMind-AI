import React from 'react';

export default function RobotCard({ robots, onChargeRobot }) {
  const getBatteryClass = (lvl) => {
    if (lvl > 50) return 'battery-high';
    if (lvl > 20) return 'battery-medium';
    return 'battery-low pulsing-text';
  };

  return (
    <div className="dashboard-card glass-panel">
      <div className="card-header">
        <div className="card-title-container">
          <svg className="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="11" width="18" height="10" rx="2" />
            <path d="M12 2v9" />
            <path d="M8 5h8" />
          </svg>
          <h3>Autonomous Robot Fleet</h3>
        </div>
        <span className="card-badge">{robots.length} Units</span>
      </div>

      <div className="card-body">
        <div className="robots-grid">
          {robots.map((robot) => (
            <div key={robot.id} className="robot-pill">
              <div className="robot-info">
                <span className="robot-name">{robot.name}</span>
                <span className={`robot-status-badge status-${robot.status.toLowerCase()}`}>
                  {robot.status}
                </span>
              </div>

              <div className="battery-container">
                <div className="battery-label">
                  <span>Battery</span>
                  <span className={getBatteryClass(robot.battery_level)}>{robot.battery_level}%</span>
                </div>
                <div className="battery-bar-bg">
                  <div 
                    className={`battery-bar-fill ${getBatteryClass(robot.battery_level)}`} 
                    style={{ width: `${robot.battery_level}%` }}
                  ></div>
                </div>
              </div>

              <div className="robot-actions">
                <button 
                  className="btn-mini btn-charge"
                  onClick={() => onChargeRobot(robot.id)}
                  disabled={robot.battery_level === 100}
                >
                  {robot.battery_level === 100 ? 'Charged' : 'Charge / Dock'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
