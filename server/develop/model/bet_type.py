from enum import Enum


class BetType(str, Enum):
    SINGLE = "Single"
    PARLAY = "Parlay"
    TEASER = "Teaser"
    ROUND_ROBIN = "Round Robin"