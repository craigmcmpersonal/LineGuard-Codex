from __future__ import annotations

from typing import Any, ClassVar
from uuid import UUID

from develop.model.market import Market
from develop.model.market_status import MarketStatus
from develop.repository.base_repository import BaseRepository


class MarketRepository(BaseRepository[Market]):
    """Repository for public.\"Market\" rows."""

    _SELECT_COLUMNS: ClassVar[str] = """
key,
event_key,
market_type_key,
parameters,
status,
public_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Market" (
    event_key,
    market_type_key,
    parameters,
    status,
    public_key
)
VALUES ($1, $2, $3, $4, COALESCE($5, gen_random_uuid()))
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Market"
WHERE event_key = $1
  AND market_type_key = $2
ORDER BY event_key, market_type_key;
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Market"
WHERE key = $1
RETURNING key;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Market"
WHERE key = $1;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Market"
SET status = $2,
    parameters = $3 
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, Market)

    async def create(
        self,
        event_key: int,
        market_type_key: int,
        *,
        parameters: Any | None = None,
        status: MarketStatus | None = None,
        public_key: UUID | None = None,
    ) -> Market | None:
        result: Market | None = await self._fetch_row(
            self._SQL_CREATE,
            event_key,
            market_type_key,
            parameters,
            status.value if status else None,
            public_key,
        )
        return result

    async def find(self, event_key: int, market_type_key: int) -> list[Market]:
        result: list[Market] = await self._fetch_all(self._SQL_FIND, event_key, market_type_key)
        return result

    async def try_get(self, key: int) -> Market | None:
        result: Market | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def try_delete(self, market: Market | int) -> bool:
        key = market.key if isinstance(market, Market) else market
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def update(self, market: Market) -> Market:
        result: Market = await self._fetch_row(
            self._SQL_UPDATE,
            market.key,
            market.status,
            market.parameters
        )
        return result
