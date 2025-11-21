import uuid
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from develop.model.bet_slip_source import BetSlipSource
from develop.model.bet_slip_status import BetSlipStatus
from develop.model.outcome import Outcome


class BetSlip(BaseModel):
    key: int
    user_key: uuid.UUID
    total_odds: float
    stake: Decimal
    status: BetSlipStatus
    placed_time: datetime
    settled_time: datetime | None = None
    result: Outcome | None = None
    external_identifier: str
    book_key: int
    original: bytes
    model: str | None = None
    import_time: datetime
    source: BetSlipSource
    last_update_time: datetime
    total_odds_live: float | None = None
    public_key: UUID
    will_pay: Decimal|None = None