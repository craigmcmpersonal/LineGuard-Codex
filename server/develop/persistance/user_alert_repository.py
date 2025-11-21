from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

from develop.persistance.model import AlertType
from develop.persistance.model import UserAlert
from develop.persistance.base_repository import BaseRepository


class UserAlertRepository(BaseRepository[UserAlert]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
user_key,
hedge_opportunity_key,
title,
message,
read,
resource_location,
creation_time,
sent_time,
public_key,
type
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."User_Alert" (
    user_key,
    hedge_opportunity_key,
    title,
    message,
    read,
    resource_location,
    creation_time,
    sent_time,
    public_key,
    type
)
VALUES ($1, $2, $3, $4, COALESCE($5, false), $6, COALESCE($7, now()), $8, COALESCE($9, gen_random_uuid()), $10)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."User_Alert"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND_BY_PUBLIC_KEY: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."User_Alert"
WHERE public_key = $1;
"""

    _SQL_FIND_BY_USER: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."User_Alert"
WHERE user_key = $1
ORDER BY creation_time DESC;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."User_Alert"
SET read = $2,
    sent_time = $3
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."User_Alert"
WHERE key = $1;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, UserAlert)

    async def create(
        self,
        user_key: UUID,
        title: str,
        message: str,
        *,
        hedge_opportunity_key: int | None = None,
        read: bool = False,
        resource_location: str | None = None,
        creation_time: datetime | None = None,
        sent_time: datetime | None = None,
        alert_type: AlertType | None = None,
        public_key: UUID | None = None,
    ) -> UserAlert | None:
        result: UserAlert | None = await self._fetch_row(
            self._SQL_CREATE,
            user_key,
            hedge_opportunity_key,
            title,
            message,
            read,
            resource_location,
            creation_time,
            sent_time,
            public_key,
            alert_type.value if alert_type else None,
        )
        return result

    async def find_by_user(self, user_key: UUID) -> list[UserAlert]:
        result: list[UserAlert] = await self._fetch_all(self._SQL_FIND_BY_USER, user_key)
        return result

    async def try_delete(self, alert: UserAlert | int) -> bool:
        key = alert.key if isinstance(alert, UserAlert) else alert
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_find_by_public_key(self, public_key: UUID) -> UserAlert:
        result: UserAlert = await self._fetch_row(self._SQL_FIND_BY_PUBLIC_KEY, public_key)
        return result

    async def try_get(self, key: int) -> UserAlert | None:
        result: UserAlert | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, alert: UserAlert) -> UserAlert | None:
        result: UserAlert | None = await self._fetch_row(self._SQL_UPDATE, alert.key, alert.read, alert.sent_time)
        return result
