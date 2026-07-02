from fastmcp import FastMCP
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.warehouse import Inventory, Worker, Robot, Order

# Initialize the WarehouseMind MCP server
mcp = FastMCP("WarehouseMind")


# ---------------------------------------------------------
# Inventory Tools
# ---------------------------------------------------------

@mcp.tool()
def get_inventory():
    """
    Return all inventory items in the warehouse.
    """

    db: Session = SessionLocal()

    try:
        items = db.query(Inventory).all()

        return [
            {
                "id": item.id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "threshold": item.threshold,
            }
            for item in items
        ]

    finally:
        db.close()


@mcp.tool()
def get_low_stock_items():
    """
    Return inventory items that are below their restocking threshold.
    """

    db: Session = SessionLocal()

    try:
        items = (
            db.query(Inventory)
            .filter(Inventory.quantity < Inventory.threshold)
            .all()
        )

        return [
            {
                "id": item.id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "threshold": item.threshold,
                "restock_needed": True,
            }
            for item in items
        ]

    finally:
        db.close()


# ---------------------------------------------------------
# Worker Tools
# ---------------------------------------------------------

@mcp.tool()
def get_workers():
    """
    Return all warehouse workers.
    """

    db: Session = SessionLocal()

    try:
        workers = db.query(Worker).all()

        return [
            {
                "id": worker.id,
                "name": worker.name,
                "role": worker.role,
                "active": worker.active,
                "shift_start": worker.shift_start,
                "shift_end": worker.shift_end,
                "zone": worker.zone,
            }
            for worker in workers
        ]

    finally:
        db.close()


# ---------------------------------------------------------
# Robot Tools
# ---------------------------------------------------------

@mcp.tool()
def get_robots():
    """
    Return all warehouse robots.
    """

    db: Session = SessionLocal()

    try:
        robots = db.query(Robot).all()

        return [
            {
                "id": robot.id,
                "name": robot.name,
                "status": robot.status,
                "battery_level": robot.battery_level,
            }
            for robot in robots
        ]

    finally:
        db.close()


# ---------------------------------------------------------
# Order Tools
# ---------------------------------------------------------

@mcp.tool()
def get_orders():
    """
    Return all warehouse orders.
    """

    db: Session = SessionLocal()

    try:
        orders = db.query(Order).all()

        return [
            {
                "id": order.id,
                "product": order.product,
                "priority": order.priority,
                "status": order.status,
            }
            for order in orders
        ]

    finally:
        db.close()