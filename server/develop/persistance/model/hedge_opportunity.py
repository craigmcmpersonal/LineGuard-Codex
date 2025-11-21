from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from develop.persistance.model.hedge_opportunity_status import HedgeOpportunityStatus


class HedgeOpportunity(BaseModel):
    key: int
    bet_slip_key: int
    hedge_rule_key: int
    trigger_reason: str | None = None
    original_win_probability: float | None = None
    recommended_hedge_stake: Decimal | None = None
    optimal_hedge_odds: Decimal | None = None
    creation_time: datetime
    expiration_time: datetime | None = None
    status: HedgeOpportunityStatus | None = None