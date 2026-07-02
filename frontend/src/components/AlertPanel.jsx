import React, { useState } from 'react';

export default function AlertPanel({ events, onAddEvent }) {
  const [eventType, setEventType] = useState('Robot Error');
  const [entityId, setEntityId] = useState('101');
  const [description, setDescription] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!description.trim()) return;

    onAddEvent({
      event_type: eventType,
      entity_id: parseInt(entityId) || 0,
      description: description.trim(),
      timestamp: new Date().toISOString()
    });

    setDescription('');
  };

  return (
    <div className="dashboard-card glass-panel flex-column-card">
      <div className="card-header">
        <div className="card-title-container">
          <svg className="card-icon text-alert" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          <h3>Incident Logger & Event Feed</h3>
        </div>
        <span className="card-badge pulse-text">{events.length} Events</span>
      </div>

      <div className="card-body event-logs-body">
        <div className="events-terminal">
          {events.length === 0 ? (
            <div className="terminal-line placeholder">Listening for operational logs...</div>
          ) : (
            [...events].reverse().map((evt, idx) => (
              <div key={idx} className="terminal-line">
                <span className="log-time">[{new Date(evt.timestamp).toLocaleTimeString()}]</span>{' '}
                <span className="log-type">[{evt.event_type}]</span>{' '}
                <span className="log-entity">ID: {evt.entity_id}</span> -{' '}
                <span className="log-desc">{evt.description}</span>
              </div>
            ))
          )}
        </div>

        <form onSubmit={handleSubmit} className="simulator-form">
          <div className="form-title">Simulate Warehouse Incident</div>
          <div className="input-group-row">
            <div className="form-control">
              <label>Event Type</label>
              <select value={eventType} onChange={(e) => setEventType(e.target.value)}>
                <option value="Robot Error">Robot Error</option>
                <option value="Staffing Alert">Staffing Alert</option>
                <option value="Inventory Depleted">Inventory Depleted</option>
                <option value="Logistics Delay">Logistics Delay</option>
                <option value="Order Surge">Order Surge</option>
              </select>
            </div>

            <div className="form-control">
              <label>Entity ID</label>
              <input 
                type="number" 
                value={entityId} 
                onChange={(e) => setEntityId(e.target.value)} 
                placeholder="e.g. 101"
              />
            </div>
          </div>

          <div className="form-control">
            <label>Incident Details</label>
            <div className="input-with-button">
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the incident (e.g. Robot-103 battery critical...)"
                required
              />
              <button type="submit" className="btn-primary">Inject</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
