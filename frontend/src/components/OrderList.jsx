import React from 'react';

export default function OrderList({ orders }) {
  const getPriorityClass = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      default: return 'priority-low';
    }
  };

  return (
    <div className="dashboard-card glass-panel">
      <div className="card-header">
        <div className="card-title-container">
          <svg className="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
          </svg>
          <h3>Active Customer Orders</h3>
        </div>
        <span className="card-badge">{orders.length} Queue</span>
      </div>

      <div className="card-body">
        <div className="orders-list">
          {orders.length === 0 ? (
            <div className="empty-state">No active orders</div>
          ) : (
            orders.map((order) => (
              <div key={order.id} className="order-item">
                <div className="order-details">
                  <span className="order-product">{order.product}</span>
                  <span className="order-id">#ORD-{order.id}</span>
                </div>
                <div className="order-tags">
                  <span className={`priority-badge ${getPriorityClass(order.priority)}`}>
                    {order.priority}
                  </span>
                  <span className={`status-badge status-${order.status.toLowerCase()}`}>
                    {order.status}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
