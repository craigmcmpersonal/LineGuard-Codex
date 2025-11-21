from typing import Any, ClassVar

from develop.model.market_type import MarketType
from develop.repository.base_repository import BaseRepository


class MarketTypeRepository(BaseRepository[MarketType]):

    _SQL_CREATE: ClassVar[str] = """
INSERT INTO public."Market_Type" (name)
VALUES ($1) RETURNING key, name; \
"""
    _SQL_DELETE: ClassVar[str] = """
DELETE 
FROM public."Market_Type"
WHERE key = $1
RETURNING key;
"""
    _SQL_GET: ClassVar[str] = """
SELECT key, name
FROM public."Market_Type"
ORDER BY key;
"""
    _SQL_TRY_FIND: ClassVar[str] = """
SELECT key, name
FROM public."Market_Type"
WHERE name = $1;
"""
    _SQL_TRY_GET: ClassVar[str] = """
SELECT key, name
FROM public."Market_Type"
WHERE key = $1;
"""
    _SQL_UPDATE: ClassVar[str] = """
UPDATE public."Market_Type"
SET "name" = $1
WHERE key = $2
RETURNING key, name;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, MarketType)

    async def create(self, name: str) -> MarketType | None:
        result: MarketType | None = await self._fetch_row(self._SQL_CREATE, name)
        return result

    async def get(self) -> list[MarketType]:
        result: list[MarketType] = await self._fetch_all(self._SQL_GET)
        return result

    async def try_delete(self, market_type: MarketType | int) -> bool:
        result: bool = await self._execute(
            self._SQL_DELETE,
            market_type.key if isinstance(
                market_type,
                MarketType
            ) else market_type
        )
        return result

    async def find(self, name: str) -> MarketType | None:
        result: MarketType | None = await self._fetch_row(self._SQL_TRY_FIND, name)
        return result

    async def try_get(self, key: int) -> MarketType | None:
        result: MarketType | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, market_type: MarketType) -> MarketType | None:
        result: MarketType|None = await self._fetch_row(
            self._SQL_UPDATE,
            market_type.name,
            market_type.key
        )
        return result
