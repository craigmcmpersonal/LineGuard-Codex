from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OddsSnapshot(BaseModel):
    key: int
    book_key: int
    market_key: int
    time: datetime
    live: bool
    raw: str
    home_price: int | None = None
    away_price: int | None = None
    home_spread: Decimal | None = None
    home_spread_price: int | None = None
    away_spread: Decimal | None = None
    away_spread_price: int | None = None
    over_total: Decimal | None = None
    over_price: int | None = None
    under_total: Decimal | None = None
    under_price: int | None = None