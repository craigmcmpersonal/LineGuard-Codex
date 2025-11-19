from pydantic import BaseModel


class MarketType(BaseModel):
    key: int
    name: str
