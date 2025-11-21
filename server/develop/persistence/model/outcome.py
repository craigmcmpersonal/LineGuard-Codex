from enum import Enum

class Outcome(str, Enum):
    WON = "Won"
    LOST = "Lost"
    VOIDED = "Voided"
    HALF_WON = "Half Won"
    HALF_LOST = "Half Lost"