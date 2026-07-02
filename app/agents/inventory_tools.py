from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.warehouse import Inventory


def check_inventory():
    """
    Returns the current warehouse inventory for the Inventory Agent.
    """

    db: Session = SessionLocal()

    try:
        items = db.query(Inventory).all()

        return [
            {
                "product": item.product_name,
                "quantity": item.quantity,
                "threshold": item.threshold,
                "low_stock": item.quantity < item.threshold,
            }
            for item in items
        ]

    finally:
        db.close()