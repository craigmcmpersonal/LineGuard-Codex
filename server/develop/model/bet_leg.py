from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from develop.model.bet_leg_status import BetLegStatus
from develop.model.outcome import Outcome


class BetLeg(BaseModel):
    key: int
    bet_slip_key: int
    selection_key: int
    odds: float
    status: BetLegStatus
    result: Outcome | None = None
    index: int
    odds_live: float | None = None
    settled_time: datetime | None = None
    public_key: UUID