from __future__ import annotations

import asyncio
import inspect

import asyncpg
from typing import Optional

from develop import environment


class PostgreSqlPoolFactory:
    _instance: Optional[PostgreSqlPoolFactory] = None
    _instance_lock = asyncio.Lock()
    _pool_init_lock = asyncio.Lock()

    def __init__(self):
        self._pool: Optional[asyncpg.pool.Pool] = None

    @classmethod
    async def get_instance(cls) -> PostgreSqlPoolFactory:
        method: str = inspect.currentframe().f_code.co_name
        if cls._instance is None:
            async with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = PostgreSqlPoolFactory()
                    print(method)
        return cls._instance

    async def get_pool(self) -> asyncpg.pool.Pool:
        method: str = inspect.currentframe().f_code.co_name
        if self._pool is None:
            async with self._pool_init_lock:
                if self._pool is None:  # double-checked locking
                    self._pool = await asyncpg.create_pool(
                        min_size=1,
                        max_size=10,
                        host=environment.try_get_value(environment.KEY_POSTGRES_HOST),
                        port=environment.try_get_value(environment.KEY_POSTGRES_PORT),
                        database=environment.try_get_value(environment.KEY_POSTGRES_DATABASE),
                        user=environment.try_get_value(environment.KEY_POSTGRES_USER),
                        password=environment.try_get_value(environment.KEY_POSTGRES_PASSWORD)
                    )
                    print(method)
        return self._pool


