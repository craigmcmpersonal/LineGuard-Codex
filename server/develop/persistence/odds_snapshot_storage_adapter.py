from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.odds_snapshot import OddsSnapshot


class OddsSnapshotStorageAdapter(BaseStorageAdapter[OddsSnapshot]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
book_key,
market_key,
"time",
live,
"raw",
home_price,
away_price,
home_spread,
home_spread_price,
away_spread,
away_spread_price,
over_total,
over_price,
under_total,
under_price
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Odds_Snapshot" (
    book_key,
    market_key,
    "time",
    live,
    "raw",
    home_price,
    away_price,
    home_spread,
    home_spread_price,
    away_spread,
    away_spread_price,
    over_total,
    over_price,
    under_total,
    under_price
)
VALUES ($1, $2, COALESCE($3, now()), COALESCE($4, false), $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Odds_Snapshot"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND_BY_MARKET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Odds_Snapshot"
WHERE market_key = $1
ORDER BY "time" DESC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Odds_Snapshot"
WHERE key = $1;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, OddsSnapshot)

    async def create(
        self,
        book_key: int,
        market_key: int,
        raw: Any,
        *,
        snapshot_time: datetime | None = None,
        live: bool = False,
        home_price: int | None = None,
        away_price: int | None = None,
        home_spread: Decimal | None = None,
        home_spread_price: int | None = None,
        away_spread: Decimal | None = None,
        away_spread_price: int | None = None,
        over_total: Decimal | None = None,
        over_price: int | None = None,
        under_total: Decimal | None = None,
        under_price: int | None = None,
    ) -> OddsSnapshot | None:
        result: OddsSnapshot | None = await self._fetch_row(
            self._SQL_CREATE,
            book_key,
            market_key,
            snapshot_time,
            live,
            raw,
            home_price,
            away_price,
            home_spread,
            home_spread_price,
            away_spread,
            away_spread_price,
            over_total,
            over_price,
            under_total,
            under_price,
        )
        return result

    async def find(self, market_key: int) -> list[OddsSnapshot]:
        result: list[OddsSnapshot] = await self._fetch_all(self._SQL_FIND_BY_MARKET, market_key)
        return result

    async def try_delete(self, odds_snapshot: OddsSnapshot | int) -> bool:
        key = odds_snapshot.key if isinstance(odds_snapshot, OddsSnapshot) else odds_snapshot
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> OddsSnapshot | None:
        result: OddsSnapshot | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result
