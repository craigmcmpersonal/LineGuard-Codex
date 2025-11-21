from uuid import UUID

from pydantic import BaseModel

from develop.persistence.model.market_status import MarketStatus


class Market(BaseModel):
    key: int
    event_key: int
    market_type_key: int
    parameters: str | None = None
    status: MarketStatus | None = None
    public_key: UUID