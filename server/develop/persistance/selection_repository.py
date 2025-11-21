from __future__ import annotations

from typing import Any, ClassVar
from uuid import UUID

from develop.betting_constants import POSITION_WINNER
from develop.persistance.model.outcome import Outcome
from develop.persistance.model import Selection
from develop.persistance.model import SelectionStatus
from develop.persistance.base_repository import BaseRepository


class SelectionRepository(BaseRepository[Selection]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
event_key,
market_key,
status,
outcome,
public_key,
position,
entrant_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Selection" (
    event_key,
    market_key,
    entrant_key,
    status,
    outcome,
    public_key,
    position
)
VALUES ($1, $2, $3, $4, $5, COALESCE($6, gen_random_uuid()), $7)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Selection"
WHERE key = $1;
"""

    _SQL_TRY_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Selection"
WHERE event_key = $1
  AND market_key = $2
  AND entrant_key = $3
ORDER BY market_key, event_key, entrant_key;
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Selection"
WHERE key = $1
RETURNING key;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Selection"
SET status = $2,
    outcome = $3 
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, Selection)

    async def create(
        self,
        event_key: int,
        market_key: int,
        entrant_key: int,
        *,
        status: SelectionStatus = SelectionStatus.ACTIVE,
        outcome: Outcome | None = None,
        public_key: UUID | None = None,
        position: str = POSITION_WINNER,
    ) -> Selection | None:
        result: Selection | None = await self._fetch_row(
            self._SQL_CREATE,
            event_key,
            market_key,
            entrant_key,
            status.value if status else None,
            outcome.value if outcome else None,
            public_key,
            position
        )
        return result

    async def find(self, event_key: int, market_key: int, entrant_key: int) -> list[Selection]:
        result: list[Selection] = await self._fetch_all(self._SQL_TRY_FIND, event_key, market_key, entrant_key)
        return result

    async def try_delete(self, selection: Selection | int) -> bool:
        key = selection.key if isinstance(selection, Selection) else selection
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> Selection | None:
        result: Selection | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, selection: Selection) -> Selection:
        result: Selection = await self._fetch_row(
            self._SQL_UPDATE,
            selection.key,
            selection.status,
            selection.outcome
        )
        return result
