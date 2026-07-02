from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database.database import Base


class StoredEvent(Base):
    __tablename__ = "warehouse_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
