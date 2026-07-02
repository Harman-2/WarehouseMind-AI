const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const BASE_URL = `${API_BASE}/warehouse`;
const AUTH_URL = `${API_BASE}/auth`;

function getAuthHeaders() {
  const token = localStorage.getItem('wm_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function parseError(res) {
  const data = await res.json().catch(() => ({}));
  const detail = data.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) return detail.map((item) => item.msg || item).join(', ');
  return 'Request failed';
}

export async function login(email, password) {
  const res = await fetch(`${AUTH_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function register(userData) {
  const res = await fetch(`${AUTH_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getMe() {
  const res = await fetch(`${AUTH_URL}/me`, { headers: getAuthHeaders() });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getWorkers() {
  const res = await fetch(`${BASE_URL}/workers`);
  if (!res.ok) throw new Error('Failed to fetch workers');
  return res.json();
}

export async function toggleWorker(id) {
  const res = await fetch(`${BASE_URL}/workers/${id}/toggle`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getRobots() {
  const res = await fetch(`${BASE_URL}/robots`);
  if (!res.ok) throw new Error('Failed to fetch robots');
  return res.json();
}

export async function chargeRobot(id) {
  const res = await fetch(`${BASE_URL}/robots/${id}/charge`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getInventory() {
  const res = await fetch(`${BASE_URL}/inventory`);
  if (!res.ok) throw new Error('Failed to fetch inventory');
  return res.json();
}

export async function restockInventory(id, amount = 50) {
  const res = await fetch(`${BASE_URL}/inventory/${id}/restock`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
    body: JSON.stringify({ amount }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getOrders() {
  const res = await fetch(`${BASE_URL}/orders`);
  if (!res.ok) throw new Error('Failed to fetch orders');
  return res.json();
}

export async function createOrder(orderData) {
  const res = await fetch(`${BASE_URL}/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
    body: JSON.stringify(orderData),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getEvents() {
  const res = await fetch(`${BASE_URL}/events`);
  if (!res.ok) throw new Error('Failed to fetch events');
  return res.json();
}

export async function addEvent(eventData) {
  const res = await fetch(`${BASE_URL}/events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(eventData),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function askAgent(message, sessionId = null) {
  const res = await fetch(`${BASE_URL}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAuthHeaders() },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function createSession() {
  const res = await fetch(`${BASE_URL}/sessions/`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getAnalyticsKpis() {
  const res = await fetch(`${BASE_URL}/analytics/kpis`);
  if (!res.ok) throw new Error('Failed to fetch KPIs');
  return res.json();
}

export async function getInventoryAnalytics() {
  const res = await fetch(`${BASE_URL}/analytics/inventory`);
  if (!res.ok) throw new Error('Failed to fetch inventory analytics');
  return res.json();
}

export async function getWorkerUtilization() {
  const res = await fetch(`${BASE_URL}/analytics/worker-utilization`);
  if (!res.ok) throw new Error('Failed to fetch worker utilization');
  return res.json();
}

export async function getOrderAnalytics() {
  const res = await fetch(`${BASE_URL}/analytics/orders`);
  if (!res.ok) throw new Error('Failed to fetch order analytics');
  return res.json();
}

export async function getPredictions() {
  const res = await fetch(`${BASE_URL}/analytics/predictions`);
  if (!res.ok) throw new Error('Failed to fetch predictions');
  return res.json();
}

export async function getRecommendations() {
  const res = await fetch(`${BASE_URL}/analytics/recommendations`);
  if (!res.ok) throw new Error('Failed to fetch recommendations');
  return res.json();
}

export async function searchDocuments(query) {
  const res = await fetch(`${BASE_URL}/documents/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}
