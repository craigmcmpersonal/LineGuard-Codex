from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from develop.model.event_status import EventStatus


class Event(BaseModel):
    key: int
    sport_key: int
    name: str
    start_time: datetime
    status: EventStatus | None = None
    public_key: UUID