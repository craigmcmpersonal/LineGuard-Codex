from pydantic import BaseModel

from develop.model.market_status import MarketStatus


class Market(BaseModel):
    key: int
    event_key: int
    market_type_key: int
    name: str
    parameters: str | None = None
    status: MarketStatus | None = None
    public_key: str | None = None