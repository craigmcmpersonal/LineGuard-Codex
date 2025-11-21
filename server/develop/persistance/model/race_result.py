from decimal import Decimal

from pydantic import BaseModel


class RaceResult(BaseModel):
    key: int
    event_key: int
    position: int
    win_payout: Decimal | None = None
    place_payout: Decimal | None = None
    entrant_key: int