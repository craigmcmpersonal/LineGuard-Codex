import unittest

from asyncpg.pool import Pool

from develop.persistance.model import Sport
from develop.persistance.model import SportType
from develop.persistance.sport_repository import SportRepository
from develop.persistance.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestSportRepository(unittest.IsolatedAsyncioTestCase):
    async def test_sport_repository_creates_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: SportRepository = SportRepository(connection)
            sport: Sport = await repository.create(name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                self.assertEqual(name, sport.name)
                initial_sport: str = sport.model_dump_json()
                print(initial_sport)
            finally:
                await repository.try_delete(sport)

    async def test_sport_repository_finds_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: SportRepository = SportRepository(connection)
            sport: Sport = await repository.create(name)
            try:
                retrieved_sport: Sport = await repository.try_find(sport.name)
                self.assertIsNotNone(retrieved_sport)
                self.assertEqual(sport.key, retrieved_sport.key)
                self.assertEqual(sport.name, retrieved_sport.name)
            finally:
                await repository.try_delete(sport)

    async def test_sport_repository_gets_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: SportRepository = SportRepository(connection)
            sport: Sport = await repository.create(name)
            try:
                retrieved_sport: Sport = await repository.try_get(sport.key)
                self.assertIsNotNone(retrieved_sport)
                self.assertEqual(sport.key, retrieved_sport.key)
                self.assertEqual(sport.name, retrieved_sport.name)
            finally:
                await repository.try_delete(sport)

    async def test_sport_repository_updates_sport_record_async(self):
        name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: SportRepository = SportRepository(connection)
            sport: Sport = await repository.create(name)
            try:
                new_name: str = compose_unique_identifier()
                sport.name = new_name
                revised_sport: Sport = await repository.update(sport)
                self.assertIsNotNone(revised_sport)
                self.assertEqual(sport.key, revised_sport.key)
                self.assertEqual(new_name, revised_sport.name)
                retrieved_sport: Sport = await repository.try_get(sport.key)
                self.assertIsNotNone(retrieved_sport)
                self.assertEqual(new_name, retrieved_sport.name)
            finally:
                await repository.try_delete(sport)


if __name__ == '__main__':
    unittest.main()
