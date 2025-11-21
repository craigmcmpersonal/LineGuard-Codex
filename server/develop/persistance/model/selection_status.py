from enum import Enum


class SelectionStatus(str, Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    WON = "Won"
    LOST = "Lost"
    VOIDED = "Voided"