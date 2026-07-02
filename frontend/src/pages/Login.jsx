import React, { useState } from 'react';
import * as api from '../services/api';

export default function Login({ onLoginSuccess }) {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({
    email: 'admin@warehousemind.ai',
    password: 'admin123',
    full_name: '',
    role: 'viewer',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (mode === 'login') {
        const data = await api.login(form.email, form.password);
        localStorage.setItem('wm_token', data.access_token);
        localStorage.setItem('wm_user', JSON.stringify({
          full_name: data.full_name,
          role: data.role,
          email: form.email,
        }));
      } else {
        await api.register(form);
        const data = await api.login(form.email, form.password);
        localStorage.setItem('wm_token', data.access_token);
        localStorage.setItem('wm_user', JSON.stringify({
          full_name: data.full_name,
          role: data.role,
          email: form.email,
        }));
      }
      onLoginSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card glass-panel">
        <h1>WarehouseMind AI</h1>
        <p className="login-subtitle">Operations Control Tower</p>

        <div className="login-tabs">
          <button
            type="button"
            className={mode === 'login' ? 'active' : ''}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            type="button"
            className={mode === 'register' ? 'active' : ''}
            onClick={() => setMode('register')}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {mode === 'register' && (
            <>
              <input
                type="text"
                placeholder="Full name"
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                required
              />
              <select
                value={form.role}
                onChange={(e) => setForm({ ...form, role: e.target.value })}
              >
                <option value="viewer">Viewer</option>
                <option value="manager">Manager</option>
              </select>
            </>
          )}

          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />

          {error && <div className="login-error">{error}</div>}

          <button type="submit" className="btn-primary-purple" disabled={loading}>
            {loading ? 'Signing in...' : mode === 'login' ? 'Enter Control Tower' : 'Create Account'}
          </button>
        </form>

        <button type="button" className="demo-link" onClick={onLoginSuccess}>
          Continue in demo mode without login
        </button>
      </div>
    </div>
  );
}
