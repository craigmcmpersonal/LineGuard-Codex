from __future__ import annotations

from typing import Any, ClassVar

from develop.model.entrant import Entrant
from develop.repository.base_repository import BaseRepository


class EntrantRepository(BaseRepository[Entrant]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
name,
number,
event_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Entrant" (
    name,
    "number",
    event_key
)
VALUES ($1, $2, $3)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Entrant"
WHERE key = $1;
"""

    _SQL_TRY_FIND_NAME: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Entrant"
WHERE name = $1
ORDER BY "number";
"""

    _SQL_TRY_FIND_NUMBER: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Entrant"
WHERE "number" = $1
ORDER BY "number";
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Entrant"
WHERE key = $1
RETURNING key;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Entrant"
SET name = $2,
    "number" = $3 
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, Entrant)

    async def create(self, name: str, event_key: int, *, number: str | None = None) -> Entrant | None:
        result: Entrant | None = await self._fetch_row(self._SQL_CREATE, name, number, event_key)
        return result

    async def find(
            self,
            *,
            name: str | None = None,
            number: str | None = None
    ) -> list[Entrant]:
        if name:
            result: list[Entrant] = await self._fetch_all(self._SQL_TRY_FIND_NAME, name)
            return result
        elif number:
            result: list[Entrant] = await self._fetch_all(self._SQL_TRY_FIND_NUMBER, number)
            return result
        else:
            raise ValueError()

    async def try_get(self, key: int) -> Entrant | None:
        result: Entrant | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def try_delete(self, entrant: Entrant | int) -> bool:
        key = entrant.key if isinstance(entrant, Entrant) else entrant
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def update(self, entrant: Entrant) -> Entrant:
        result: Entrant = await self._fetch_row(
            self._SQL_UPDATE,
            entrant.key,
            entrant.name,
            entrant.number
        )
        return result
