import React from 'react';

export default function InventoryCard({ inventory, onRestockItem }) {
  return (
    <div className="dashboard-card glass-panel">
      <div className="card-header">
        <div className="card-title-container">
          <svg className="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
            <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
            <line x1="12" y1="22.08" x2="12" y2="12" />
          </svg>
          <h3>Inventory stock</h3>
        </div>
        <span className="card-badge">{inventory.length} SKUs</span>
      </div>

      <div className="card-body">
        <div className="inventory-list">
          {inventory.map((item) => {
            const isLow = item.quantity < item.threshold;
            return (
              <div key={item.id} className={`inventory-item-row ${isLow ? 'low-stock' : ''}`}>
                <div className="item-meta">
                  <div className="item-name-container">
                    {isLow && <span className="pulse-dot"></span>}
                    <span className="item-name">{item.product_name}</span>
                  </div>
                  <span className="item-threshold">Threshold: {item.threshold}</span>
                </div>

                <div className="item-qty-container">
                  <div className="qty-visual">
                    <span className={`qty-value ${isLow ? 'text-alert' : ''}`}>{item.quantity}</span>
                    <span className="qty-unit">units</span>
                  </div>
                  <button 
                    className="btn-mini btn-restock"
                    onClick={() => onRestockItem(item.id)}
                  >
                    + Restock
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
