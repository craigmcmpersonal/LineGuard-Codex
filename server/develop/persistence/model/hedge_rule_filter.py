from decimal import Decimal

from pydantic import BaseModel


class HedgeRuleFilter(BaseModel):
    key: int
    hedge_rule_key: int
    sport_key: int | None = None
    market_type_key: int | None = None
    minimum_odds: Decimal | None = None
    maximum_odds: Decimal | None = None