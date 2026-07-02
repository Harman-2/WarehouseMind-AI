import React from 'react';

export default function WorkerCard({ workers, onToggleWorker }) {
  return (
    <div className="dashboard-card glass-panel">
      <div className="card-header">
        <div className="card-title-container">
          <svg className="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
          <h3>Staffing & Shift Roster</h3>
        </div>
        <span className="card-badge">{workers.length} Total</span>
      </div>

      <div className="card-body">
        <div className="table-responsive">
          <table className="control-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Zone</th>
                <th>Shift</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {workers.map((worker) => (
                <tr key={worker.id} className={!worker.active ? 'row-inactive' : ''}>
                  <td className="worker-name">{worker.name}</td>
                  <td><span className="role-tag">{worker.role}</span></td>
                  <td><span className="zone-tag">{worker.zone}</span></td>
                  <td className="shift-time">{worker.shift_start} - {worker.shift_end}</td>
                  <td>
                    <button
                      className={`status-toggle-btn ${worker.active ? 'active' : 'inactive'}`}
                      onClick={() => onToggleWorker(worker.id)}
                      title={`Click to toggle active status`}
                    >
                      <span className="toggle-dot"></span>
                      {worker.active ? 'Active' : 'Sick / Out'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
