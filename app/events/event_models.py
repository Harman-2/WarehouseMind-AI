from pydantic import BaseModel
from datetime import datetime


class WarehouseEvent(BaseModel):

    event_type: str

    entity_id: int

    description: str

    timestamp: datetime