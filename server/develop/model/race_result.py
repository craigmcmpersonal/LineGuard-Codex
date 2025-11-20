from pydantic import BaseModel


class RaceResult(BaseModel):
    key: int
    event_key: int
    position: int
    win_payout: float | None = None
    place_payout: float | None = None
    entrant_key: int