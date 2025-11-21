from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserHedgeProfile(BaseModel):
    key: int
    content: str|None = None
    valid_from: datetime
    valid_to: datetime
    creation_time: datetime
    user_key: UUID
    version: int
    valid_from: datetime
    valid_to: datetime|None = None