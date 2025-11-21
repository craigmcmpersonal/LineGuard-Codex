from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID


from .base_repository import BaseRepository
from ..model.event import Event
from ..model.event_status import EventStatus


class EventRepository(BaseRepository[Event]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
sport_key,
name,
start_time,
status,
public_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Event" (
    sport_key,
    name,
    start_time,
    status,
    public_key
)
VALUES ($1, $2, $3, $4, COALESCE($5, gen_random_uuid()))
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE
FROM public."Event"
WHERE key = $1
RETURNING key;
"""

    _SQL_TRY_FIND_NAME: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Event"
WHERE name = $1
ORDER BY start_time DESC
"""

    _SQL_TRY_FIND_PUBLIC_KEY: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Event"
WHERE public_key = $1;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Event"
WHERE key = $1;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Event"
SET start_time = $2,
    status = $3 
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, Event)

    async def create(
        self,
        sport_key: int,
        name: str,
        start_time: datetime,
        *,
        status: EventStatus = EventStatus.SCHEDULED,
        public_key: UUID | None = None,
    ) -> Event | None:
        result: Event | None = await self._fetch_row(
            self._SQL_CREATE,
            sport_key,
            name,
            start_time,
            status.value if status else None,
            public_key,
        )
        return result

    async def try_delete(self, event: Event | int) -> bool:
        key = event.key if isinstance(event, Event) else event
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_find(
        self,
        *,
        public_key: UUID | None = None,
        name: str | None = None
    ) -> Event|list[Event]|None:
        if public_key:
            result: Event | None = await self._fetch_row(self._SQL_TRY_FIND_PUBLIC_KEY, public_key)
            return result
        elif name:
            result: list[Event] = await self._fetch_all(self._SQL_TRY_FIND_NAME, name)
            return result
        else:
            raise ValueError()

    async def try_get(self, key: int) -> Event | None:
        result: Event | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, event: Event) -> Event:
        result: Event = await self._fetch_row(
            self._SQL_UPDATE,
            event.key,
            event.start_time,
            event.status.value
        )
        return result


