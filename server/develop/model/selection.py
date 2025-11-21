from uuid import UUID

from pydantic import BaseModel

from develop.betting_constants import POSITION_WINNER
from develop.model.outcome import Outcome
from develop.model.selection_status import SelectionStatus


class Selection(BaseModel):
    key: int
    event_key: int
    entrant_key: int
    market_key: int
    status: SelectionStatus | None = None
    outcome: Outcome | None = None
    position: str = POSITION_WINNER
    public_key: UUID
