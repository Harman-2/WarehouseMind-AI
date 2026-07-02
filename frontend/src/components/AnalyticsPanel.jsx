import React, { useEffect, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import * as api from '../services/api';

const STATUS_COLORS = {
  healthy: '#22c55e',
  low: '#f59e0b',
  critical: '#ef4444',
};

export default function AnalyticsPanel() {
  const [inventory, setInventory] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [
          inventoryData,
          workerData,
          orderData,
          predictionData,
          recommendationData,
          kpiData,
        ] = await Promise.all([
          api.getInventoryAnalytics(),
          api.getWorkerUtilization(),
          api.getOrderAnalytics(),
          api.getPredictions(),
          api.getRecommendations(),
          api.getAnalyticsKpis(),
        ]);

        setInventory(inventoryData);
        setWorkers(workerData);
        setOrders(orderData);
        setPredictions(predictionData);
        setRecommendations(recommendationData.recommendations || []);
        setKpis(kpiData);
      } catch (err) {
        console.error('Analytics load failed:', err);
      }
    };

    load();
    const interval = setInterval(load, 10000);
    return () => clearInterval(interval);
  }, []);

  const workerChartData = workers.flatMap((zone) => ([
    { name: `${zone.zone} Active`, value: zone.active, fill: '#8b5cf6' },
    { name: `${zone.zone} Inactive`, value: zone.inactive, fill: '#64748b' },
  ])).filter((item) => item.value > 0);

  return (
    <div className="dashboard-card glass-panel analytics-panel">
      <div className="card-header">
        <div className="card-title-container">
          <div className="pulse-indicator-purple"></div>
          <h3>Analytics & Predictive Intelligence</h3>
        </div>
        <span className="card-badge bg-purple">Phase 11 + 13</span>
      </div>

      <div className="card-body analytics-body">
        {kpis && (
          <div className="analytics-kpi-row">
            <div className="analytics-kpi">Utilization {kpis.worker_utilization_pct}%</div>
            <div className="analytics-kpi">Stock Alerts {kpis.stock_alerts}</div>
            <div className="analytics-kpi">High Priority Orders {kpis.high_priority_orders}</div>
            <div className="analytics-kpi">Robot Alerts {kpis.robots_needing_attention}</div>
          </div>
        )}

        <div className="analytics-grid">
          <div className="chart-card">
            <h4>Inventory vs Threshold</h4>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={inventory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="product" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Legend />
                <Bar dataKey="quantity" fill="#8b5cf6" name="Quantity" />
                <Bar dataKey="threshold" fill="#38bdf8" name="Threshold" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h4>Stock Health</h4>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={inventory}
                  dataKey="quantity"
                  nameKey="product"
                  cx="50%"
                  cy="50%"
                  outerRadius={70}
                  label
                >
                  {inventory.map((entry) => (
                    <Cell key={entry.product} fill={STATUS_COLORS[entry.status] || '#8b5cf6'} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h4>Worker Utilization by Zone</h4>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={workers}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="zone" stroke="#94a3b8" hide />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Legend />
                <Bar dataKey="active" stackId="a" fill="#22c55e" name="Active" />
                <Bar dataKey="inactive" stackId="a" fill="#ef4444" name="Inactive" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h4>Order Priority Mix</h4>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={orders}
                  dataKey="count"
                  nameKey="priority"
                  cx="50%"
                  cy="50%"
                  outerRadius={70}
                  label
                >
                  {orders.map((entry, index) => (
                    <Cell key={entry.priority} fill={['#8b5cf6', '#f59e0b', '#ef4444'][index % 3]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="analytics-lists">
          <div className="prediction-list">
            <h4>Predictive Alerts</h4>
            {predictions.length === 0 ? (
              <p>No active predictive alerts.</p>
            ) : (
              predictions.map((alert, index) => (
                <div key={index} className={`prediction-item severity-${alert.severity}`}>
                  <strong>{alert.title}</strong>
                  <span>{alert.message}</span>
                </div>
              ))
            )}
          </div>

          <div className="prediction-list">
            <h4>AI Recommendations</h4>
            {recommendations.map((item, index) => (
              <div key={index} className="recommendation-item">{item}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
