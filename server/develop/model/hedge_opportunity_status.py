from enum import Enum


class HedgeOpportunityStatus(str, Enum):
    ACTIVE = "Active"
    EXECUTED = "Executed"
    EXPIRED = "Expired"