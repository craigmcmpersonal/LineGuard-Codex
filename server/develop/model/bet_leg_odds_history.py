from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BetLegOddsHistory(BaseModel):
    key: int
    bet_leg_key: int
    book_key: int
    odds: Decimal
    captured_time: datetime