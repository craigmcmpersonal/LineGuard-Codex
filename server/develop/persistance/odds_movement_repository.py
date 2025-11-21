from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar

from develop.persistance.model import OddsMovement
from develop.persistance.base_repository import BaseRepository


class OddsMovementRepository(BaseRepository[OddsMovement]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
book_key,
market_key,
attribute,
old_value,
new_value,
change_percentage,
creation_time
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Odds_Movement" (
    book_key,
    market_key,
    attribute,
    old_value,
    new_value,
    change_percentage
)
VALUES ($1, $2, $3, $4, $5, $6)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Odds_Movement"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Odds_Movement"
WHERE market_key = $1
ORDER BY creation_time DESC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Odds_Movement"
WHERE key = $1;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, OddsMovement)

    async def create(
        self,
        book_key: int,
        market_key: int,
        attribute: str,
        new_value: Decimal,
        *,
        old_value: Decimal|None = None,
        change_percentage: Decimal | None = None,
    ) -> OddsMovement | None:
        result: OddsMovement | None = await self._fetch_row(
            self._SQL_CREATE,
            book_key,
            market_key,
            attribute,
            old_value,
            new_value,
            change_percentage,
        )
        return result

    async def find(self, market_key: int) -> list[OddsMovement]:
        result: list[OddsMovement] = await self._fetch_all(self._SQL_FIND, market_key)
        return result

    async def try_delete(self, odds_movement: OddsMovement | int) -> bool:
        key = odds_movement.key if isinstance(odds_movement, OddsMovement) else odds_movement
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> OddsMovement | None:
        result: OddsMovement | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result
