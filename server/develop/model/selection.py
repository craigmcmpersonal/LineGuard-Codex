from pydantic import BaseModel

from develop.model.outcome import Outcome
from develop.model.selection_status import SelectionStatus


class Selection(BaseModel):
    key: int
    event_key: int
    entrant_key: int
    market_key: int
    status: SelectionStatus | None = None
    outcome: Outcome | None = None
    position: str = "1" # In a race, the position being bet on. In a game, 1 signifies betting on the winner.
    public_key: str
