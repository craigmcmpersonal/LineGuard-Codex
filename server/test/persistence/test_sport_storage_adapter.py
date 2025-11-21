import unittest

from asyncpg.pool import Pool

from develop.persistence.model.sport import Sport
from develop.persistence.model.sport_type import SportType
from develop.persistence.sport_storage_adapter import SportStorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestSportStorageAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_sport_storage_adapter_creates_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: SportStorageAdapter = SportStorageAdapter(connection)
            sport: Sport = await storage_adapter.create(name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                self.assertEqual(name, sport.name)
                initial_sport: str = sport.model_dump_json()
                print(initial_sport)
            finally:
                await storage_adapter.try_delete(sport)

    async def test_sport_storage_adapter_finds_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: SportStorageAdapter = SportStorageAdapter(connection)
            sport: Sport = await storage_adapter.create(name)
            try:
                retrieved_sport: Sport = await storage_adapter.try_find(sport.name)
                self.assertIsNotNone(retrieved_sport)
                self.assertEqual(sport.key, retrieved_sport.key)
                self.assertEqual(sport.name, retrieved_sport.name)
            finally:
                await storage_adapter.try_delete(sport)

    async def test_sport_storage_adapter_gets_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: SportStorageAdapter = SportStorageAdapter(connection)
            sport: Sport = await storage_adapter.create(name)
            try:
                retrieved_sport: Sport = await storage_adapter.try_get(sport.key)
                self.assertIsNotNone(retrieved_sport)
                self.assertEqual(sport.key, retrieved_sport.key)
                self.assertEqual(sport.name, retrieved_sport.name)
            finally:
                await storage_adapter.try_delete(sport)

    async def test_sport_storage_adapter_updates_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: SportStorageAdapter = SportStorageAdapter(connection)
            sport: Sport = await storage_adapter.create(name)
            try:
                new_name: str = compose_unique_identifier()
                sport.name = new_name
                revised_sport: Sport = await storage_adapter.update(sport)
                self.assertIsNotNone(revised_sport)
                self.assertEqual(sport.key, revised_sport.key)
                self.assertEqual(new_name, revised_sport.name)
                retrieved_sport: Sport = await storage_adapter.try_get(sport.key)
                self.assertIsNotNone(retrieved_sport)
                self.assertEqual(new_name, retrieved_sport.name)
            finally:
                await storage_adapter.try_delete(sport)


if __name__ == '__main__':
    unittest.main()
