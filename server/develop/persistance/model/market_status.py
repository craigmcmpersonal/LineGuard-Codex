from enum import Enum


class MarketStatus(str, Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    SETTLED = "Settled"