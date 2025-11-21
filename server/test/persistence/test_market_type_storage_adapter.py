import unittest

from asyncpg.pool import Pool

from develop.persistence.model.market_type import MarketType
from develop.persistence.market_type_storage_adapter import MarketTypeStorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestMarketTypeStorageAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_market_type_storage_adapter_creates_market_type_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: MarketTypeStorageAdapter = MarketTypeStorageAdapter(connection)
            market_type: MarketType = await storage_adapter.create(name)
            self.assertIsNotNone(market_type)
            self.assertIsNotNone(market_type.key)
            try:
                self.assertEqual(name, market_type.name)
                initial_market_type: str = market_type.model_dump_json()
                print(initial_market_type)
            finally:
                await storage_adapter.try_delete(market_type)

    async def test_market_type_storage_adapter_finds_market_type_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: MarketTypeStorageAdapter = MarketTypeStorageAdapter(connection)
            market_type: MarketType = await storage_adapter.create(name)
            try:
                retrieved_market_type: MarketType = await storage_adapter.find(market_type.name)
                self.assertIsNotNone(retrieved_market_type)
                self.assertEqual(market_type.key, retrieved_market_type.key)
                self.assertEqual(market_type.name, retrieved_market_type.name)
            finally:
                await storage_adapter.try_delete(market_type)

    async def test_market_type_storage_adapter_gets_market_type_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: MarketTypeStorageAdapter = MarketTypeStorageAdapter(connection)
            market_type: MarketType = await storage_adapter.create(name)
            try:
                retrieved_market_type: MarketType = await storage_adapter.try_get(market_type.key)
                self.assertIsNotNone(retrieved_market_type)
                self.assertEqual(market_type.key, retrieved_market_type.key)
                self.assertEqual(market_type.name, retrieved_market_type.name)
            finally:
                await storage_adapter.try_delete(market_type)

    async def test_market_type_storage_adapter_updates_market_type_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: MarketTypeStorageAdapter = MarketTypeStorageAdapter(connection)
            market_type: MarketType = await storage_adapter.create(name)
            try:
                new_name: str = compose_unique_identifier()
                market_type.name = new_name
                revised_market_type: MarketType = await storage_adapter.update(market_type)
                self.assertIsNotNone(revised_market_type)
                self.assertEqual(market_type.key, revised_market_type.key)
                self.assertEqual(new_name, revised_market_type.name)
                retrieved_market_type: MarketType = await storage_adapter.try_get(market_type.key)
                self.assertIsNotNone(retrieved_market_type)
                self.assertEqual(new_name, retrieved_market_type.name)
            finally:
                await storage_adapter.try_delete(market_type)


if __name__ == '__main__':
    unittest.main()
