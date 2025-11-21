from __future__ import annotations

from typing import Any, ClassVar
from uuid import UUID

from develop.persistance.model import UserHedgeProfile
from develop.persistance.base_repository import BaseRepository


class UserHedgeProfileRepository(BaseRepository[UserHedgeProfile]):
    _SELECT_COLUMNS: ClassVar[str] = """
key,
user_key,
content,
version,
creation_time,
valid_from,
valid_to
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."User_Hedge_Profile" (user_key, content, version)
VALUES ($1, $2, $3)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
 DELETE
 FROM public."User_Hedge_Profile"
 WHERE key = $1
 RETURNING key;
 """

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."User_Hedge_Profile"
WHERE key = $1;
"""

    _SQL_TRY_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."User_Hedge_Profile"
WHERE user_key = $1
ORDER BY creation_time DESC;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."User_Hedge_Profile"
SET valid_to = $2
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, UserHedgeProfile)

    async def create(
        self,
        user_key: UUID,
        *,
        content: str|None = None,
        version: int = 1
    ) -> UserHedgeProfile:
        result: UserHedgeProfile = await self._fetch_row(
            self._SQL_CREATE,
            user_key,
            content,
            version
        )
        return result

    async def try_delete(self, user_hedge_profile: UserHedgeProfile | int) -> bool:
        result: bool = await self._execute(
            self._SQL_DELETE,
            user_hedge_profile.key if isinstance(
                user_hedge_profile,
                UserHedgeProfile
            ) else user_hedge_profile
        )
        return result

    async def try_find(self, user_key: UUID) -> UserHedgeProfile | None:
        result: UserHedgeProfile|None = await self._fetch_row(self._SQL_TRY_FIND, user_key)
        return result

    async def try_get(self, key: int) -> UserHedgeProfile | None:
        result: UserHedgeProfile|None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, user_hedge_profile: UserHedgeProfile) -> UserHedgeProfile:
        result: UserHedgeProfile = await self._fetch_row(
            self._SQL_UPDATE,
            user_hedge_profile.key,
            user_hedge_profile.valid_to
        )
        return result

