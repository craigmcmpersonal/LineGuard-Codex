from pydantic import BaseModel


class HedgeOpportunityLeg(BaseModel):
    key: int
    hedge_opportunity_key: int
    bet_leg_key: int
