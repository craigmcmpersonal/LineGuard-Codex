import datetime
import unittest

from asyncpg.pool import Pool

from develop.persistence.model.event import Event
from develop.persistence.model.event_status import EventStatus
from develop.persistence.model.sport import Sport
from develop.persistence.model.sport_type import SportType
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier


class TestEventStorageAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_event_storage_adapter_creates_sport_record_async(self):
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
                    self.assertEqual(event_name, event.name)
                    self.assertEqual(start_time, event.start_time)
                    initial_event: str = event.model_dump_json()
                    print(initial_event)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_event_storage_adapter_finds_event_record_async(self):
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
                    matches: list[Event] = await storage_adapter.event.try_find(name=event_name)
                    self.assertIsNotNone(matches)
                    if len(matches) != 1:
                        self.fail()
                    else:
                        self.assertIsNotNone(matches[0])
                        self.assertIsNotNone(matches[0].key)
                        self.assertEqual(event.key, matches[0].key)
                        retrieved: Event = await storage_adapter.event.try_find(public_key=matches[0].public_key)
                        self.assertIsNotNone(retrieved)
                        self.assertIsNotNone(retrieved.key)
                        self.assertEqual(event.key, retrieved.key)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_event_storage_adapter_gets_event_record_async(self):
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
                    retrieved: Event = await storage_adapter.event.try_get(event.key)
                    self.assertIsNotNone(retrieved)
                    self.assertIsNotNone(retrieved.key)
                    self.assertEqual(event.name, retrieved.name)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_event_storage_adapter_updates_event_record_async(self):
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
                    event.status = EventStatus.LIVE
                    updated_status: Event = await storage_adapter.event.update(event)
                    self.assertIsNotNone(updated_status)
                    self.assertEqual(event.status, updated_status.status)
                    event.start_time = datetime.datetime.now(datetime.timezone.utc)
                    updated_time: Event = await storage_adapter.event.update(event)
                    self.assertIsNotNone(updated_time)
                    self.assertEqual(event.start_time, updated_time.start_time)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)


if __name__ == '__main__':
    unittest.main()
