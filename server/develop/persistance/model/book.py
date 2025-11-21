from datetime import datetime

from pydantic import BaseModel


class Book(BaseModel):
    key: int
    name: str
    last_seen: datetime