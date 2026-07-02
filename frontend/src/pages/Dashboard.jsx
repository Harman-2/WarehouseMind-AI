import React, { useState, useEffect, useCallback } from 'react';
import Navbar from '../components/Navbar';
import WorkerCard from '../components/WorkerCard';
import RobotCard from '../components/RobotCard';
import InventoryCard from '../components/InventoryCard';
import OrderList from '../components/OrderList';
import AlertPanel from '../components/AlertPanel';
import AgentConsole from '../components/AgentConsole';
import AnalyticsPanel from '../components/AnalyticsPanel';
import * as api from '../services/api';

export default function Dashboard({ user, onLogout }) {
  const [workers, setWorkers] = useState([]);
  const [robots, setRobots] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [orders, setOrders] = useState([]);
  const [events, setEvents] = useState([]);
  const [apiHealthy, setApiHealthy] = useState(true);
  const [sessionId, setSessionId] = useState(null);
  const [stats, setStats] = useState({
    activeWorkers: 0,
    totalWorkers: 0,
    activeRobots: 0,
    totalRobots: 0,
    stockAlerts: 0,
    highPriorityOrders: 0,
  });

  const fetchData = useCallback(async () => {
    try {
      const [workersData, robotsData, inventoryData, ordersData, eventsData] = await Promise.all([
        api.getWorkers(),
        api.getRobots(),
        api.getInventory(),
        api.getOrders(),
        api.getEvents(),
      ]);

      setWorkers(workersData);
      setRobots(robotsData);
      setInventory(inventoryData);
      setOrders(ordersData);
      setEvents(eventsData);
      setApiHealthy(true);

      const activeWorkers = workersData.filter((w) => w.active).length;
      const activeRobots = robotsData.filter((r) => r.status.toLowerCase() !== 'maintenance').length;
      const stockAlerts = inventoryData.filter((i) => i.quantity < i.threshold).length;
      const highPriorityOrders = ordersData.filter(
        (o) => o.priority.toLowerCase() === 'high' && o.status.toLowerCase() !== 'completed'
      ).length;

      setStats({
        activeWorkers,
        totalWorkers: workersData.length,
        activeRobots,
        totalRobots: robotsData.length,
        stockAlerts,
        highPriorityOrders,
      });
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setApiHealthy(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const handleToggleWorker = async (id) => {
    try {
      const updated = await api.toggleWorker(id);
      await api.addEvent({
        event_type: 'Staffing Alert',
        entity_id: id,
        description: `Worker ${updated.name} toggled to ${updated.active ? 'Active' : 'Inactive (Sick/Out)'}`,
        timestamp: new Date().toISOString(),
      });
      fetchData();
    } catch (err) {
      alert(`Failed to update worker: ${err.message}`);
    }
  };

  const handleChargeRobot = async (id) => {
    try {
      const robot = robots.find((r) => r.id === id);
      await api.chargeRobot(id);
      await api.addEvent({
        event_type: 'Robot Error',
        entity_id: id,
        description: `${robot ? robot.name : `Robot #${id}`} docked to charging station`,
        timestamp: new Date().toISOString(),
      });
      fetchData();
    } catch (err) {
      alert(`Failed to dock robot: ${err.message}`);
    }
  };

  const handleRestockItem = async (id) => {
    try {
      const item = inventory.find((i) => i.id === id);
      await api.restockInventory(id, 50);
      await api.addEvent({
        event_type: 'Inventory Depleted',
        entity_id: id,
        description: `Restocked 50 units for ${item ? item.product_name : `Item #${id}`}`,
        timestamp: new Date().toISOString(),
      });
      fetchData();
    } catch (err) {
      alert(`Failed to restock item: ${err.message}`);
    }
  };

  const handleAddEvent = async (eventData) => {
    try {
      await api.addEvent(eventData);

      if (eventData.event_type === 'Order Surge') {
        await api.createOrder({ product: 'Laptop', priority: 'High', status: 'Pending' });
        await api.createOrder({ product: 'Keyboard', priority: 'High', status: 'Pending' });
      }

      fetchData();
    } catch (err) {
      alert(`Failed to simulate event: ${err.message}`);
    }
  };

  const handleAskAgent = async (message, currentSessionId) => {
    return api.askAgent(message, currentSessionId);
  };

  return (
    <div className="control-tower-dashboard">
      <Navbar stats={stats} apiHealthy={apiHealthy} user={user} onLogout={onLogout} />

      {!apiHealthy && (
        <div className="alert-banner-error">
          <strong>CRITICAL STATUS WARNING:</strong> Control Tower backend disconnected. Check connection to the FastAPI cloud service on port 8000.
        </div>
      )}

      <div className="dashboard-grid">
        <div className="dashboard-column flex-column">
          <WorkerCard workers={workers} onToggleWorker={handleToggleWorker} />
          <RobotCard robots={robots} onChargeRobot={handleChargeRobot} />
        </div>

        <div className="dashboard-column flex-column middle-column">
          <AgentConsole
            onAskAgent={handleAskAgent}
            sessionId={sessionId}
            onSessionChange={setSessionId}
          />
          <AnalyticsPanel />
        </div>

        <div className="dashboard-column flex-column">
          <div className="split-grid-row">
            <InventoryCard inventory={inventory} onRestockItem={handleRestockItem} />
            <OrderList orders={orders} />
          </div>
          <AlertPanel events={events} onAddEvent={handleAddEvent} />
        </div>
      </div>
    </div>
  );
}
