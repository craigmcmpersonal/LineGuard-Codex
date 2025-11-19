from __future__ import annotations

from typing import Any, Coroutine

from asyncpg import Record
from asyncpg.pool import PoolAcquireContext

from develop.model.market_type import MarketType


_SQL_CREATE: str = """
INSERT INTO public."Market_Type" (name)
VALUES ($1) 
RETURNING key, name;
"""
_SQL_DELETE: str = """
DELETE FROM public."Market_Type"
WHERE key = $1
RETURNING key;
"""
_SQL_GET: str = """
SELECT key, name
FROM public."Market_Type"
ORDER BY key;
"""
_SQL_TRY_FIND: str = """
SELECT key, name
FROM public."Market_Type"
WHERE name = $1;
"""
_SQL_TRY_GET: str = """
SELECT key, name
FROM public."Market_Type"
WHERE key = $1;
"""
_SQL_UPDATE: str = """
UPDATE public."Market_Type"
SET "name" = $1
WHERE key = $2
RETURNING key, name;
"""

async def create(name: str, connection: Any) -> MarketType | None:
    row: Record = await connection.fetchrow(_SQL_CREATE, name)
    result: MarketType | None = MarketType(**row) if row else None
    return result

async def get(connection: Any) -> list[MarketType]:
    rows: list[Record] = await connection.fetch(_SQL_GET)
    result: list[MarketType] = [
        MarketType(**item)
        for item in rows
    ]
    return result

async def try_delete(market_type: MarketType|str, connection:Any) -> bool:
    row: Coroutine[Any, Any, Any|None] = await connection.fetchrow(
        _SQL_DELETE, market_type.key if isinstance(
            market_type,
            MarketType
        ) else market_type
    )
    result: bool = row is not None
    return result

async def try_find(name: str, connection: Any) -> MarketType | None:
    row: Record = await connection.fetchrow(_SQL_TRY_FIND, name)
    result: MarketType | None = MarketType(**row) if row else None
    return result

async def try_get(key: int, connection: Any) -> MarketType | None:
    row: Record = await connection.fetchrow(_SQL_TRY_GET, key)
    result: MarketType | None = MarketType(**row) if row else None
    return result

async def update(market_type: MarketType, connection: Any) -> MarketType | None:
    values: list[Any] = [
        market_type.name,
        market_type.key
    ]
    row = await connection.fetchrow(_SQL_UPDATE, *values)
    result: MarketType|None = MarketType(**row) if row else None
    return result
