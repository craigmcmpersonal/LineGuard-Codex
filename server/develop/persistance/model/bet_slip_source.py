from enum import Enum


class BetSlipSource(str, Enum):
    MANUAL = "Manual"
    SYNC = "Sync"
    EMAIL = "Email"
    IMAGE = "Image"
    AUDIO = "Audio"