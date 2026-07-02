from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.warehouse import Inventory, Order, Robot, Worker


def _estimate_daily_demand(orders: list[Order], product: str) -> float:
    product_orders = [order for order in orders if order.product.lower() == product.lower()]
    if not product_orders:
        return 1.0
    return max(len(product_orders) * 2.5, 1.0)


def get_kpis(db: Session) -> dict:
    workers = db.query(Worker).all()
    robots = db.query(Robot).all()
    inventory = db.query(Inventory).all()
    orders = db.query(Order).all()

    active_workers = sum(1 for worker in workers if worker.active)
    low_stock = [item for item in inventory if item.quantity < item.threshold]
    critical_stock = [item for item in inventory if item.quantity <= item.threshold * 0.5]
    high_priority_orders = [
        order
        for order in orders
        if order.priority.lower() == "high" and order.status.lower() != "completed"
    ]
    robots_needing_attention = [
        robot
        for robot in robots
        if robot.battery_level < 25 or robot.status.lower() == "maintenance"
    ]

    return {
        "active_workers": active_workers,
        "total_workers": len(workers),
        "worker_utilization_pct": round((active_workers / len(workers)) * 100, 1) if workers else 0,
        "active_robots": sum(1 for robot in robots if robot.status.lower() == "working"),
        "total_robots": len(robots),
        "stock_alerts": len(low_stock),
        "critical_stock_items": len(critical_stock),
        "high_priority_orders": len(high_priority_orders),
        "robots_needing_attention": len(robots_needing_attention),
    }


def get_inventory_chart(db: Session) -> list[dict]:
    items = db.query(Inventory).all()
    return [
        {
            "product": item.product_name,
            "quantity": item.quantity,
            "threshold": item.threshold,
            "status": "critical" if item.quantity <= item.threshold * 0.5 else "low" if item.quantity < item.threshold else "healthy",
        }
        for item in items
    ]


def get_worker_utilization(db: Session) -> list[dict]:
    workers = db.query(Worker).all()
    zones: dict[str, dict] = {}

    for worker in workers:
        zone = worker.zone or "Unassigned"
        if zone not in zones:
            zones[zone] = {"zone": zone, "active": 0, "inactive": 0}
        if worker.active:
            zones[zone]["active"] += 1
        else:
            zones[zone]["inactive"] += 1

    return list(zones.values())


def get_order_distribution(db: Session) -> list[dict]:
    orders = db.query(Order).all()
    counts: dict[str, int] = {}
    for order in orders:
        counts[order.priority] = counts.get(order.priority, 0) + 1
    return [{"priority": priority, "count": count} for priority, count in counts.items()]


def get_predictive_alerts(db: Session) -> list[dict]:
    inventory = db.query(Inventory).all()
    orders = db.query(Order).all()
    workers = db.query(Worker).all()
    robots = db.query(Robot).all()
    alerts = []

    for item in inventory:
        daily_demand = _estimate_daily_demand(orders, item.product_name)
        days_remaining = item.quantity / daily_demand
        if days_remaining <= 7:
            alerts.append(
                {
                    "type": "demand_forecast",
                    "severity": "critical" if days_remaining <= 2 else "warning",
                    "title": f"{item.product_name} stockout risk",
                    "message": (
                        f"Estimated {days_remaining:.1f} days of stock remaining "
                        f"at current order velocity."
                    ),
                    "recommended_action": "Place replenishment order immediately.",
                }
            )

    inactive_by_zone: dict[str, int] = {}
    for worker in workers:
        if not worker.active:
            inactive_by_zone[worker.zone] = inactive_by_zone.get(worker.zone, 0) + 1

    for zone, count in inactive_by_zone.items():
        alerts.append(
            {
                "type": "staffing",
                "severity": "warning",
                "title": f"Staffing gap in {zone}",
                "message": f"{count} inactive worker(s) may reduce throughput.",
                "recommended_action": "Reassign staff or call in backup coverage.",
            }
        )

    for robot in robots:
        if robot.battery_level < 20:
            alerts.append(
                {
                    "type": "robot_battery",
                    "severity": "critical" if robot.battery_level < 10 else "warning",
                    "title": f"{robot.name} low battery",
                    "message": f"Battery at {robot.battery_level}%.",
                    "recommended_action": "Route robot to charging station.",
                }
            )

    return alerts


def get_ai_recommendations(db: Session) -> list[str]:
    alerts = get_predictive_alerts(db)
    recommendations = []

    for alert in alerts[:5]:
        recommendations.append(f"{alert['title']}: {alert['recommended_action']}")

    if not recommendations:
        recommendations.append("Operations stable. Continue monitoring inventory thresholds and shift coverage.")

    return recommendations


def get_root_cause_analysis(db: Session, issue: str) -> dict:
    inventory = db.query(Inventory).all()
    workers = db.query(Worker).all()
    robots = db.query(Robot).all()
    issue_lower = issue.lower()

    causes = []
    impacts = []
    actions = []

    if any(term in issue_lower for term in ["stock", "inventory", "keyboard", "monitor"]):
        low_items = [item for item in inventory if item.quantity < item.threshold]
        for item in low_items:
            causes.append(f"{item.product_name} below threshold ({item.quantity}/{item.threshold}).")
            impacts.append(f"Order fulfillment delays for {item.product_name}.")
            actions.append(f"Restock {item.product_name} and review reorder point.")

    if any(term in issue_lower for term in ["worker", "staff", "shift", "sick"]):
        inactive = [worker for worker in workers if not worker.active]
        for worker in inactive:
            causes.append(f"{worker.name} inactive in {worker.zone}.")
            impacts.append(f"Reduced capacity in {worker.zone}.")
            actions.append(f"Assign backup coverage for {worker.role} in {worker.zone}.")

    if any(term in issue_lower for term in ["robot", "battery", "maintenance"]):
        troubled = [robot for robot in robots if robot.battery_level < 25 or robot.status.lower() == "maintenance"]
        for robot in troubled:
            causes.append(f"{robot.name} status {robot.status}, battery {robot.battery_level}%.")
            impacts.append("Automation throughput reduced in affected zones.")
            actions.append(f"Charge or service {robot.name} before next peak window.")

    if not causes:
        causes.append("No single dominant signal detected from current operational data.")
        impacts.append("Issue may be external or require manual investigation.")
        actions.append("Run targeted checks with inventory, worker, and knowledge agents.")

    return {
        "issue": issue,
        "probable_causes": causes,
        "operational_impacts": impacts,
        "recommended_actions": actions,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
