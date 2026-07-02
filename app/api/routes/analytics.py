from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_role
from app.database.database import get_db
from app.models.user import User
from app.services import conversation_service
from app.services import predictions

router = APIRouter(prefix="/warehouse/analytics", tags=["Analytics"])


class RootCauseRequest(BaseModel):
    issue: str


@router.get("/kpis")
def analytics_kpis(
    db: Session = Depends(get_db),
    _: User | None = Depends(get_current_user),
):
    return predictions.get_kpis(db)


@router.get("/inventory")
def analytics_inventory(db: Session = Depends(get_db)):
    return predictions.get_inventory_chart(db)


@router.get("/worker-utilization")
def analytics_workers(db: Session = Depends(get_db)):
    return predictions.get_worker_utilization(db)


@router.get("/orders")
def analytics_orders(db: Session = Depends(get_db)):
    return predictions.get_order_distribution(db)


@router.get("/predictions")
def analytics_predictions(db: Session = Depends(get_db)):
    return predictions.get_predictive_alerts(db)


@router.get("/recommendations")
def analytics_recommendations(db: Session = Depends(get_db)):
    return {"recommendations": predictions.get_ai_recommendations(db)}


@router.post("/root-cause")
def analytics_root_cause(
    payload: RootCauseRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin", "manager")),
):
    return predictions.get_root_cause_analysis(db, payload.issue)
