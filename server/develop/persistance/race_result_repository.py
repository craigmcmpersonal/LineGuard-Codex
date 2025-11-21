from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar

from develop.persistance.model import RaceResult
from develop.persistance.base_repository import BaseRepository


class RaceResultRepository(BaseRepository[RaceResult]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
event_key,
"position",
win_payout,
place_payout,
entrant_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Race_Result" (
    event_key,
    "position",
    win_payout,
    place_payout,
    entrant_key
)
VALUES ($1, $2, $3, $4, $5)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Race_Result"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Race_Result"
WHERE event_key = $1
ORDER BY position;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Race_Result"
WHERE key = $1;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Race_Result"
SET "position" = $2,
    win_payout = $3,
    place_payout = $4
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, RaceResult)

    async def create(
        self,
        event_key: int,
        entrant_key: int,
        position: int,
        *,
        win_payout: Decimal | None = None,
        place_payout: Decimal | None = None,
    ) -> RaceResult | None:
        result: RaceResult | None = await self._fetch_row(
            self._SQL_CREATE,
            event_key,
            position,
            win_payout,
            place_payout,
            entrant_key,
        )
        return result

    async def find(self, event_key: int) -> list[RaceResult]:
        result: list[RaceResult] = await self._fetch_all(self._SQL_FIND, event_key)
        return result

    async def try_delete(self, race_result: RaceResult | int) -> bool:
        key = race_result.key if isinstance(race_result, RaceResult) else race_result
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> RaceResult | None:
        result: RaceResult | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, race_result: RaceResult) -> RaceResult | None:
        result: RaceResult | None = await self._fetch_row(
            self._SQL_UPDATE,
            race_result.key,
            race_result.position,
            race_result.win_payout,
            race_result.place_payout,
        )
        return result
