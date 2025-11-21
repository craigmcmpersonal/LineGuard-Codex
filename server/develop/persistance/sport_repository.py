from __future__ import annotations

from typing import Any, ClassVar



from .base_repository import BaseRepository
from develop.persistance.model.sport import Sport
from develop.persistance.model.sport_type import SportType


class SportRepository(BaseRepository[Sport]):
    _SELECT_COLUMNS: ClassVar[str] = """
key,
name,
active,
sport_type
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Sport" (name, active, sport_type)
VALUES ($1, $2, $3)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
 DELETE
 FROM public."Sport"
 WHERE key = $1
 RETURNING key;
 """

    _SQL_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Sport"
ORDER BY name ASC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Sport"
WHERE key = $1;
"""

    _SQL_TRY_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Sport"
WHERE name = $1;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Sport"
SET name = $2,
    active = $3, 
    sport_type = $4
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, Sport)

    async def create(
        self,
        name: str,
        *,
        active: bool = True,
        sport_type: SportType = SportType.GAME,
    ) -> Sport:
        result: Sport = await self._fetch_row(self._SQL_CREATE, name, active, sport_type.value)
        return result

    async def get(self) -> list[Sport]:
        result: list[Sport] = await self._fetch_all(self._SQL_GET)
        return result

    async def try_delete(self, sport: Sport | int) -> bool:
        result: bool = await self._execute(
            self._SQL_DELETE,
            sport.key if isinstance(
                sport,
                Sport
            ) else sport
        )
        return result

    async def try_find(self, name: str) -> Sport | None:
        result: Sport|None = await self._fetch_row(self._SQL_TRY_FIND, name)
        return result

    async def try_get(self, key: int) -> Sport | None:
        result: Sport|None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, sport: Sport) -> Sport:
        result: Sport = await self._fetch_row(
            self._SQL_UPDATE,
            sport.key,
            sport.name,
            sport.active,
            sport.sport_type
        )
        return result

