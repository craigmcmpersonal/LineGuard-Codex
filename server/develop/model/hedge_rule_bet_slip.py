from pydantic import BaseModel


class HedgeRuleBetSlip(BaseModel):
    hedge_rule_key: int
    bet_slip_key: int