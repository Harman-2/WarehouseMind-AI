import React, { useState } from 'react';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import './App.css';

function App() {
  const [authenticated, setAuthenticated] = useState(
    () => localStorage.getItem('wm_skip_login') === '1' || !!localStorage.getItem('wm_token')
  );
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('wm_user');
    return stored ? JSON.parse(stored) : null;
  });

  const handleLoginSuccess = () => {
    if (!localStorage.getItem('wm_token')) {
      localStorage.setItem('wm_skip_login', '1');
    } else {
      localStorage.removeItem('wm_skip_login');
      const stored = localStorage.getItem('wm_user');
      setUser(stored ? JSON.parse(stored) : null);
    }
    setAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('wm_token');
    localStorage.removeItem('wm_user');
    localStorage.removeItem('wm_skip_login');
    setUser(null);
    setAuthenticated(false);
  };

  if (!authenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return <Dashboard user={user} onLogout={handleLogout} />;
}

export default App;
