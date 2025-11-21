from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OddsMovement(BaseModel):
    key: int
    book_key: int
    market_key: int
    attribute: str
    old_value: Decimal|None = None
    new_value: Decimal
    change_percentage: Decimal | None = None
    creation_time: datetime