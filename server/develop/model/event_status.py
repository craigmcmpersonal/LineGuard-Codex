from enum import Enum


class EventStatus(str, Enum):
    SCHEDULED = "Scheduled"
    LIVE = "Live"
    FINAL = "Final"
    CANCELLED = "Cancelled"
    POSTPONED = "Postponed"