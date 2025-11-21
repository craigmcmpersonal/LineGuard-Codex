import datetime
import unittest

from asyncpg.pool import Pool

from develop.persistence.model.entrant import Entrant
from develop.persistence.model.event import Event
from develop.persistence.model.sport import Sport
from develop.persistence.model.sport_type import SportType
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestEntrantStorageAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_entrant_storage_adapter_creates_sport_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    entrant_name: str = compose_unique_identifier()
                    entrant_number: str = compose_unique_identifier()
                    entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key, number=entrant_number)
                    self.assertIsNotNone(entrant)
                    self.assertIsNotNone(entrant.key)
                    try:
                        self.assertEqual(entrant_name, entrant.name)
                        self.assertEqual(entrant_number, entrant.number)
                        initial_entrant: str = entrant.model_dump_json()
                        print(initial_entrant)
                    finally:
                        await storage_adapter.entrant.try_delete(entrant)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_entrant_storage_adapter_finds_entrant_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    entrant_name: str = compose_unique_identifier()
                    entrant_number: str = compose_unique_identifier()
                    entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key, number=entrant_number)
                    self.assertIsNotNone(entrant)
                    self.assertIsNotNone(entrant.key)
                    try:
                        retrieved_by_name: list[Entrant] = await storage_adapter.entrant.find(name=entrant.name)
                        self.assertIsNotNone(retrieved_by_name)
                        if len(retrieved_by_name) != 1:
                            self.fail()
                        else:
                            self.assertEqual(entrant.key, retrieved_by_name[0].key)
                            retrieved_by_number: list[Entrant] = await storage_adapter.entrant.find(
                                number=entrant.number
                            )
                            self.assertIsNotNone(retrieved_by_number)
                            if len(retrieved_by_number) != 1:
                                self.fail()
                            else:
                                self.assertEqual(entrant.key, retrieved_by_number[0].key)
                    finally:
                        await storage_adapter.entrant.try_delete(entrant)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_entrant_storage_adapter_gets_entrant_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    entrant_name: str = compose_unique_identifier()
                    entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key)
                    self.assertIsNotNone(entrant)
                    self.assertIsNotNone(entrant.key)
                    try:
                        retrieved: Entrant = await storage_adapter.entrant.try_get(entrant.key)
                        self.assertIsNotNone(retrieved)
                        self.assertEqual(entrant.name, retrieved.name)
                    finally:
                        await storage_adapter.entrant.try_delete(entrant)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_entrant_storage_adapter_updates_entrant_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    entrant_name: str = compose_unique_identifier()
                    entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key)
                    self.assertIsNotNone(entrant)
                    self.assertIsNotNone(entrant.key)
                    try:
                        entrant.name = compose_unique_identifier()
                        updated_name: Entrant = await storage_adapter.entrant.update(entrant)
                        self.assertIsNotNone(updated_name)
                        self.assertEqual(entrant.name, updated_name.name)
                        entrant.number = compose_unique_identifier()
                        updated_number: Entrant = await storage_adapter.entrant.update(entrant)
                        self.assertIsNotNone(updated_number)
                        self.assertEqual(entrant.number, updated_number.number)
                    finally:
                        await storage_adapter.entrant.try_delete(entrant)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)


if __name__ == '__main__':
    unittest.main()
