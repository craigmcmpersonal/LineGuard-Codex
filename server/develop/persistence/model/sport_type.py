from enum import Enum


class SportType(str, Enum):
    GAME = "Game"
    RACE = "Race"
    FIGHT = "Fight"
    TOURNAMENT = "Tournament"