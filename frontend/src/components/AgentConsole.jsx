import React, { useState, useRef, useEffect } from 'react';

const PRESET_SCENARIOS = [
  { label: '🔋 Robot Battery Dead', prompt: 'A robot battery has died in Zone A (Robot-103 battery is at 5%). Give me a quick status and coordination recommendations.' },
  { label: '⚙️ Conveyor Belt Stopped', prompt: 'The conveyor belt in packing Zone B has stopped running. Analyze the operational risk and suggest coordination instructions.' },
  { label: '📉 Inventory Low Alert', prompt: 'Check current inventory risk for Keyboard and Monitor stock. Provide quantity analysis and actions.' },
  { label: '🚛 Late Truck Delivery', prompt: 'A supplier delivery truck containing 150 monitors has reported a 3-hour traffic delay. Suggest mitigation plan.' },
  { label: '⚡ Prime Order Surge', prompt: 'An unexpected surge of 3,000 Prime orders has arrived. Suggest worker shift adjustments and robot coordination.' },
  { label: '🤒 Worker Reported Sick', prompt: 'Forklift driver John has reported sick for the morning shift. Suggest staffing adjustments and coverage.' },
  { label: '📋 Safety Policy Check', prompt: 'What is the warehouse policy when robot battery falls below 20 percent?' },
];

export default function AgentConsole({ onAskAgent, sessionId, onSessionChange }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'WarehouseMind Operations Control Tower Active. Select a preset scenario below or type a query to coordinate the multi-agent system. Conversation memory is enabled for follow-up questions.',
    },
  ]);
  const [inputVal, setInputVal] = useState('');
  const [loading, setLoading] = useState(false);
  const consoleBottomRef = useRef(null);

  useEffect(() => {
    if (consoleBottomRef.current) {
      consoleBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  const handleSubmit = async (text) => {
    if (!text.trim() || loading) return;

    setMessages((prev) => [...prev, { role: 'user', text }]);
    setLoading(true);
    setInputVal('');

    try {
      const data = await onAskAgent(text, sessionId);
      if (data.session_id && data.session_id !== sessionId) {
        onSessionChange?.(data.session_id);
      }
      setMessages((prev) => [...prev, { role: 'assistant', text: data.response || 'No response returned.' }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', text: `Error coordinating agents: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewSession = () => {
    onSessionChange?.(null);
    setMessages([
      {
        role: 'assistant',
        text: 'Started a new conversation session. Ask about inventory, workers, or warehouse policies.',
      },
    ]);
  };

  return (
    <div className="dashboard-card glass-panel agent-console-card">
      <div className="card-header">
        <div className="card-title-container">
          <div className="pulse-indicator-purple"></div>
          <h3>AI Control Tower Agent Console</h3>
        </div>
        <div className="console-header-actions">
          {sessionId && <span className="card-badge bg-purple">Session #{sessionId}</span>}
          <button type="button" className="preset-btn" onClick={handleNewSession} disabled={loading}>
            New Session
          </button>
          <span className="card-badge bg-purple">Multi-Agent Orchestrator</span>
        </div>
      </div>

      <div className="card-body console-body">
        <div className="presets-container">
          {PRESET_SCENARIOS.map((scenario, index) => (
            <button
              key={index}
              className="preset-btn"
              onClick={() => handleSubmit(scenario.prompt)}
              disabled={loading}
            >
              {scenario.label}
            </button>
          ))}
        </div>

        <div className="terminal-screen">
          <div className="terminal-welcome">
            SYSTEM STATUS: ONLINE | AGENTS: COORDINATOR, INVENTORY, WORKER, KNOWLEDGE
          </div>

          {messages.map((msg, index) => (
            <div key={index} className={`terminal-message ${msg.role === 'user' ? 'user-query' : 'agent-reply'}`}>
              <span className="message-prefix">{msg.role === 'user' ? '> USER: ' : '> WAREHOUSE_MIND: '}</span>
              <span className="message-text">{msg.text}</span>
            </div>
          ))}

          {loading && (
            <div className="terminal-message agent-reply thinking-state">
              <span className="message-prefix">&gt; WAREHOUSE_MIND: </span>
              <span className="thinking-dots">Coordinating agents & analyzing DB metrics</span>
            </div>
          )}
          <div ref={consoleBottomRef}></div>
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit(inputVal);
          }}
          className="console-input-row"
        >
          <span className="input-prompt-symbol">&gt;</span>
          <input
            type="text"
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            placeholder="Type custom command or operational issue (e.g. Check low stock items)..."
            disabled={loading}
          />
          <button type="submit" className="btn-primary-purple" disabled={loading || !inputVal.trim()}>
            Send Query
          </button>
        </form>
      </div>
    </div>
  );
}
