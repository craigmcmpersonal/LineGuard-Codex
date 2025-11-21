from enum import Enum

class BetLegStatus(str, Enum):
    PENDING="Pending"
    WON = "Won"
    LOST = "Lost"
    VOIDED = "Voided"
