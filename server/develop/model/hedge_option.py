from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class HedgeOption(BaseModel):
    key: int
    hedge_opportunity_key: int
    book: str
    odds: float
    required_stake: Decimal
    guaranteed_profit: Decimal
    implied_probability: float | None = None
    option_rank: int | None = None
    public_key: str
    resource_location: str | None = None
    last_update_time: datetime