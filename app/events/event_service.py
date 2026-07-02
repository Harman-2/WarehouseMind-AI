from sqlalchemy.orm import Session

from app.events.event_models import WarehouseEvent
from app.models.events import StoredEvent


def create_event(db: Session, event: WarehouseEvent) -> StoredEvent:
    stored = StoredEvent(
        event_type=event.event_type,
        entity_id=event.entity_id,
        description=event.description,
        timestamp=event.timestamp,
    )
    db.add(stored)
    db.commit()
    db.refresh(stored)
    return stored


def get_events(db: Session, limit: int = 100) -> list[StoredEvent]:
    return (
        db.query(StoredEvent)
        .order_by(StoredEvent.timestamp.desc())
        .limit(limit)
        .all()
    )
