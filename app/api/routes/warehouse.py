from app.events.event_models import WarehouseEvent
from app.events.event_service import create_event, get_events
from app.models.warehouse import Inventory, Order, Robot, Worker
from app.services.agent_service import (
    AgentRateLimitError,
    AgentUnavailableError,
    run_coordinator,
)

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.database import get_db
from app.models.user import User

router = APIRouter(prefix="/warehouse", tags=["Warehouse"])


class Query(BaseModel):
    message: str
    session_id: int | None = None


class OrderCreate(BaseModel):
    product: str
    priority: str
    status: str = "Pending"


class RestockRequest(BaseModel):
    amount: int = 50


@router.get("/workers")
def get_workers(db: Session = Depends(get_db)):
    return db.query(Worker).all()


@router.get("/robots")
def get_robots(db: Session = Depends(get_db)):
    return db.query(Robot).all()


@router.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/events")
def add_event(event: WarehouseEvent, db: Session = Depends(get_db)):
    stored = create_event(db, event)
    return {
        "event_type": stored.event_type,
        "entity_id": stored.entity_id,
        "description": stored.description,
        "timestamp": stored.timestamp,
    }


@router.get("/events")
def read_events(db: Session = Depends(get_db)):
    events = get_events(db)
    return [
        {
            "event_type": event.event_type,
            "entity_id": event.entity_id,
            "description": event.description,
            "timestamp": event.timestamp,
        }
        for event in events
    ]


@router.post("/ask")
async def ask(
    query: Query,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user),
):
    user_id = user.email if user else "demo-user"

    try:
        response, session_id = await run_coordinator(
            message=query.message,
            db=db,
            session_id=query.session_id,
            user_id=user_id,
        )
    except AgentRateLimitError as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc
    except AgentUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "response": response or "No response returned.",
        "session_id": session_id,
    }


@router.post("/workers/{worker_id}/toggle")
def toggle_worker(
    worker_id: int,
    db: Session = Depends(get_db),
):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker.active = not worker.active
    db.commit()
    db.refresh(worker)
    return worker


@router.post("/robots/{robot_id}/charge")
def charge_robot(
    robot_id: int,
    db: Session = Depends(get_db),
):
    robot = db.query(Robot).filter(Robot.id == robot_id).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    robot.battery_level = 100
    robot.status = "Charging"
    db.commit()
    db.refresh(robot)
    return robot


@router.post("/inventory/{item_id}/restock")
def restock_inventory(
    item_id: int,
    request: RestockRequest,
    db: Session = Depends(get_db),
):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    item.quantity += request.amount
    db.commit()
    db.refresh(item)
    return item


@router.post("/orders")
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
):
    new_order = Order(
        product=order_data.product,
        priority=order_data.priority,
        status=order_data.status,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
