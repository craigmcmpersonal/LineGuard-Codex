from datetime import datetime

from pydantic import BaseModel


class RuleEvaluationLog(BaseModel):
    key: int
    hedge_rule_key: int
    bet_slip_key: int
    evaluation_time: datetime
    inputs: str
    output: str
    hedge_opportunity_key: int | None = None