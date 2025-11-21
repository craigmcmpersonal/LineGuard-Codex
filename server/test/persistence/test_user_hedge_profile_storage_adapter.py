import datetime
import unittest

from uuid import UUID, uuid4

from asyncpg.pool import Pool

from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.user_hedge_profile_storage_adapter import UserHedgeProfileStorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestUserHedgeProfileStorageAdapter(BaseStorageAdapterTest):
    async def test_user_hedge_profile_storage_adapter_creates_user_hedge_profile_record_async(self):
        user_key: UUID = uuid4()
        content: str = compose_unique_identifier()
        version: int = 2
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: UserHedgeProfileStorageAdapter = UserHedgeProfileStorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await storage_adapter.create(user_key, content=content, version=version)
            self.assertIsNotNone(user_hedge_profile)
            self.assertIsNotNone(user_hedge_profile.key)
            try:
                self.assertEqual(user_key, user_hedge_profile.user_key)
                self.assertEqual(content, user_hedge_profile.content)
                self.assertEqual(version, user_hedge_profile.version)
                initial_user_hedge_profile: str = user_hedge_profile.model_dump_json()
                print(initial_user_hedge_profile)
            finally:
                await storage_adapter.try_delete(user_hedge_profile)

    async def test_user_hedge_profile_storage_adapter_finds_user_hedge_profile_record_async(self):
        user_key: UUID = uuid4()
        content: str = compose_unique_identifier()
        version: int = 2
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: UserHedgeProfileStorageAdapter = UserHedgeProfileStorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await storage_adapter.create(user_key, content=content, version=version)
            self.assertIsNotNone(user_hedge_profile)
            self.assertIsNotNone(user_hedge_profile.key)
            try:
                self.assertEqual(user_key, user_hedge_profile.user_key)
                self.assertEqual(content, user_hedge_profile.content)
                self.assertEqual(version, user_hedge_profile.version)
                initial_user_hedge_profile: str = user_hedge_profile.model_dump_json()
                print(initial_user_hedge_profile)
            finally:
                await storage_adapter.try_delete(user_hedge_profile)

    async def test_user_hedge_profile_storage_adapter_gets_user_hedge_profile_record_async(self):
        user_key: UUID = uuid4()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: UserHedgeProfileStorageAdapter = UserHedgeProfileStorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await storage_adapter.create(user_key)
            try:
                retrieved_user_hedge_profile: UserHedgeProfile = await storage_adapter.try_get(user_hedge_profile.key)
                self.assertEqual(user_key, retrieved_user_hedge_profile.user_key)
                self.assertEqual(1, retrieved_user_hedge_profile.version)
            finally:
                await storage_adapter.try_delete(user_hedge_profile)

    async def test_user_hedge_profile_storage_adapter_updates_user_hedge_profile_record_async(self):
        user_key: UUID = uuid4()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: UserHedgeProfileStorageAdapter = UserHedgeProfileStorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await storage_adapter.create(user_key)
            try:
                self.assertIsNone(user_hedge_profile.valid_to)
                user_hedge_profile.valid_to = datetime.datetime.now(datetime.timezone.utc)
                revised_user_hedge_profile: UserHedgeProfile = await storage_adapter.update(user_hedge_profile)
                self.assertEqual(user_key, revised_user_hedge_profile.user_key)
                self.assertEqual(1, revised_user_hedge_profile.version)
                self.assertEqual(user_hedge_profile.valid_to, revised_user_hedge_profile.valid_to)
                retrieved_user_hedge_profile: UserHedgeProfile = await storage_adapter.try_get(user_hedge_profile.key)
                self.assertEqual(user_key, retrieved_user_hedge_profile.user_key)
                self.assertEqual(1, retrieved_user_hedge_profile.version)
                self.assertEqual(user_hedge_profile.valid_to, retrieved_user_hedge_profile.valid_to)
            finally:
                await storage_adapter.try_delete(user_hedge_profile)


if __name__ == '__main__':
    unittest.main()
