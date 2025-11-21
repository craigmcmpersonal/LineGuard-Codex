from __future__ import annotations

from typing import Any, ClassVar

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.book import Book


class BookStorageAdapter(BaseStorageAdapter[Book]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
name,
last_seen
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Book" (name)
VALUES ($1)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
 DELETE
 FROM public."Book"
 WHERE key = $1
 RETURNING key;
 """

    _SQL_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Book"
ORDER BY name ASC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Book"
WHERE key = $1;
"""

    _SQL_TRY_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Book"
WHERE name = $1;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Book"
SET name = $2,
    last_seen = now()
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, Book)

    async def create(
        self,
        name: str
    ) -> Book:
        result: Book = await self._fetch_row(self._SQL_CREATE, name)
        return result

    async def get(self) -> list[Book]:
        result: list[Book] = await self._fetch_all(self._SQL_GET)
        return result

    async def try_delete(self, book: Book | int) -> bool:
        result: bool = await self._execute(
            self._SQL_DELETE,
            book.key if isinstance(
                book,
                Book
            ) else book
        )
        return result

    async def try_find(self, name: str) -> Book | None:
        result: Book|None = await self._fetch_row(self._SQL_TRY_FIND, name)
        return result

    async def try_get(self, key: int) -> Book | None:
        result: Book|None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, book: Book) -> Book:
        result: Book = await self._fetch_row(
            self._SQL_UPDATE,
            book.key,
            book.name
        )
        return result

