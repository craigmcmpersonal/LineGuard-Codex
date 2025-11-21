from enum import Enum


class BetSlipStatus(str, Enum):
    PENDING = "Pending"
    PLACED = "Placed"
    WON = "Won"
    LOST = "Lost"
    CASHOUT_OFFERED = "Cashout Offered"
    CASHED_OUT = "Cashed Out"
    VOIDED = "Voided"
    PARTIALLY_WON = "Partially Won"