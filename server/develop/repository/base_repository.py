from typing import Any, Generic, TypeVar, Type, List
from asyncpg import Record

TModel = TypeVar("TModel")  # The Pydantic model

class BaseRepository(Generic[TModel]):

    def __init__(self, connection: Any, model: Type[TModel]):
        self._connection = connection
        self._model = model

    def _to_model(self, row: Record) -> TModel:
        result: TModel = self._model(**row)
        return result

    async def _fetch_row(self, sql: str, *args) -> TModel | None:
        row: Any = await self._connection.fetchrow(sql, *args)
        result: TModel|None = self._to_model(row) if row else None
        return result

    async def _fetch_all(self, sql: str, *args) -> List[TModel]:
        rows: list = await self._connection.fetch(sql, *args)
        result: List[TModel] = [
            self._to_model(item)
            for item in rows
        ]
        return result

    async def _execute(self, sql: str, *args) -> bool:
        row: Any = await self._connection.fetchrow(sql, *args)
        result: bool = row is not None
        return result
