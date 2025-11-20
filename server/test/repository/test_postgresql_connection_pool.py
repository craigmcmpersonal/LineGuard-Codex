import asyncio
import unittest
from typing import Callable, Coroutine, Any

from asyncpg import Pool

from develop.model.market_type import MarketType
from develop.repository.market_type_repository import MarketTypeRepository
from develop.repository.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestPostgresqlConnectionPool(unittest.IsolatedAsyncioTestCase):
    async def use_pool_async(self, pool: Pool):
        name: str = compose_unique_identifier()
        async with pool.acquire() as connection:
            repository: MarketTypeRepository = MarketTypeRepository(connection)
            market_type: MarketType = await repository.create(name)
            self.assertIsNotNone(market_type)
            self.assertIsNotNone(market_type.key)
            try:
                self.assertEqual(name, market_type.name)
                initial_market_type: str = market_type.model_dump_json()
                print(initial_market_type)
            finally:
                await repository.try_delete(market_type)

    async def test_postgresql_connection_pool_works_async(self):
        number_cases: int = 5
        connection_pool: Pool = await create_pool_async()
        tasks: list[Coroutine[Any, Any, None]] = [
            self.use_pool_async(connection_pool)
            for _ in range(number_cases)
        ]
        count_tasks: int = len(tasks)
        self.assertEqual(number_cases, count_tasks)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    unittest.main()
