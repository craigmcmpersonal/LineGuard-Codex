from pydantic import BaseModel

from develop.persistence.model.sport_type import SportType


class Sport(BaseModel):
    key: int
    name: str
    active: bool
    sport_type: SportType