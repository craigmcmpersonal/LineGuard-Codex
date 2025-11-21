from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserAlert(BaseModel):
    key: int
    hedge_opportunity_key: int
    title: str
    message: str
    creation_time: datetime
    public_key: UUID
    read: bool = False
    resource_location: str|None = None
    sent_time: datetime|None = None
