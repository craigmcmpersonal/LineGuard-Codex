from datetime import datetime

from pydantic import BaseModel


class HedgeRule(BaseModel):
    key: int
    user_hedge_profile_key: int
    rule_name: str
    original: str
    model: str | None = None
    priority: int
    active: bool
    creation_time: datetime
    version: int
    valid_from: datetime
    valid_to: datetime|None