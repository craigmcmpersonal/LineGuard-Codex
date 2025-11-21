import unittest

from asyncpg.pool import Pool

from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.book import Book
from develop.persistence.model.hedge_rule import HedgeRule
from develop.persistence.model .hedge_rule_bet_slip import HedgeRuleBetSlip
from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
import test.test_contants as test_constants
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestHedgeRuleStorageAdapter(BaseStorageAdapterTest):
    async def test_hedge_rule_storage_adapter_adds_bet_slips_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(storage_adapter)
            try:
                rule_name: str = compose_unique_identifier()
                original: str = compose_unique_identifier()
                hedge_rule: HedgeRule = await storage_adapter.hedge_rule.create(
                    user_hedge_profile.key,
                    rule_name,
                    original
                )
                self.assertIsNotNone(hedge_rule)
                self.assertIsNotNone(hedge_rule.key)
                try:
                    book: Book = await self._create_book(storage_adapter)
                    try:
                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                        try:
                            hedge_rule_bet_slip: HedgeRuleBetSlip = await storage_adapter.hedge_rule.add_bet_slip(
                                hedge_rule.key,
                                bet_slip.key
                            )
                            self.assertIsNotNone(hedge_rule_bet_slip)
                            try:
                                self.assertEqual(hedge_rule.key, hedge_rule_bet_slip.hedge_rule_key)
                                self.assertEqual(bet_slip.key, hedge_rule_bet_slip.bet_slip_key)
                            finally:
                                await storage_adapter.hedge_rule.remove_bet_slip(hedge_rule_bet_slip)
                        finally:
                            await storage_adapter.bet_slip.try_delete(bet_slip)
                    finally:
                        await storage_adapter.book.try_delete(book)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_storage_adapter_creates_hedge_rule_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(storage_adapter)
            try:
                rule_name: str = compose_unique_identifier()
                original: str = compose_unique_identifier()
                hedge_rule: HedgeRule = await storage_adapter.hedge_rule.create(
                    user_hedge_profile.key,
                    rule_name,
                    original
                )
                self.assertIsNotNone(hedge_rule)
                self.assertIsNotNone(hedge_rule.key)
                try:
                    self.assertIsNotNone(hedge_rule.rule_name)
                    self.assertIsNotNone(original, hedge_rule.original)
                    serialized: str = user_hedge_profile.model_dump_json()
                    print(serialized)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_storage_adapter_deactivates_hedge_rule_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(storage_adapter)
            try:
                rule_name: str = compose_unique_identifier()
                original: str = compose_unique_identifier()
                hedge_rule: HedgeRule = await storage_adapter.hedge_rule.create(
                    user_hedge_profile.key,
                    rule_name,
                    original
                )
                self.assertIsNotNone(hedge_rule)
                self.assertIsNotNone(hedge_rule.key)
                try:
                    deactivated: HedgeRule = await storage_adapter.hedge_rule.deactivate(hedge_rule)
                    self.assertNotEqual(hedge_rule.active, deactivated.active)
                    self.assertNotEqual(hedge_rule.valid_to, deactivated.valid_to)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_storage_adapter_finds_bet_slips_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(storage_adapter)
            try:
                rule_name: str = compose_unique_identifier()
                original: str = compose_unique_identifier()
                hedge_rule: HedgeRule = await storage_adapter.hedge_rule.create(
                    user_hedge_profile.key,
                    rule_name,
                    original
                )
                self.assertIsNotNone(hedge_rule)
                self.assertIsNotNone(hedge_rule.key)
                try:
                    book: Book = await self._create_book(storage_adapter)
                    try:
                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                        try:
                            hedge_rule_bet_slip: HedgeRuleBetSlip = await storage_adapter.hedge_rule.add_bet_slip(
                                hedge_rule.key,
                                bet_slip.key
                            )
                            self.assertIsNotNone(hedge_rule_bet_slip)
                            try:
                                retrieved: list[HedgeRuleBetSlip] = await storage_adapter.hedge_rule.find_bet_slips(
                                    hedge_rule.key
                                )
                                self.assertIsNotNone(retrieved)
                                if (count := len(retrieved)) != 1:
                                    self.fail(count)
                                else:
                                    self.assertEqual(hedge_rule.key, retrieved[0].hedge_rule_key)
                                    self.assertEqual(bet_slip.key, retrieved[0].bet_slip_key)
                            finally:
                                await storage_adapter.hedge_rule.remove_bet_slip(hedge_rule_bet_slip)
                        finally:
                            await storage_adapter.bet_slip.try_delete(bet_slip)
                    finally:
                        await storage_adapter.book.try_delete(book)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_storage_adapter_finds_hedge_rule_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(storage_adapter)
            try:
                rule_name: str = compose_unique_identifier()
                original: str = compose_unique_identifier()
                hedge_rule: HedgeRule = await storage_adapter.hedge_rule.create(
                    user_hedge_profile.key,
                    rule_name,
                    original
                )
                self.assertIsNotNone(hedge_rule)
                self.assertIsNotNone(hedge_rule.key)
                try:
                    retrieved: list[HedgeRule] = await storage_adapter.hedge_rule.find(user_hedge_profile.key)
                    self.assertIsNotNone(retrieved)
                    if (count := len(retrieved)) != 1:
                        self.fail(count)
                    else:
                        self.assertEqual(hedge_rule.key, retrieved[0].key)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_storage_adapter_gets_hedge_rule_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(storage_adapter)
            try:
                rule_name: str = compose_unique_identifier()
                original: str = compose_unique_identifier()
                hedge_rule: HedgeRule = await storage_adapter.hedge_rule.create(
                    user_hedge_profile.key,
                    rule_name,
                    original
                )
                self.assertIsNotNone(hedge_rule)
                self.assertIsNotNone(hedge_rule.key)
                try:
                    retrieved: HedgeRule = await storage_adapter.hedge_rule.try_get(hedge_rule.key)
                    self.assertIsNotNone(retrieved)
                    self.assertEqual(hedge_rule.key, retrieved.key)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_storage_adapter_updates_hedge_rule_model_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(storage_adapter)
            try:
                rule_name: str = compose_unique_identifier()
                original: str = compose_unique_identifier()
                hedge_rule: HedgeRule = await storage_adapter.hedge_rule.create(
                    user_hedge_profile.key,
                    rule_name,
                    original
                )
                self.assertIsNotNone(hedge_rule)
                self.assertIsNotNone(hedge_rule.key)
                try:
                    hedge_rule.model = test_constants.MARKET_PARAMETERS
                    updated: HedgeRule = await storage_adapter.hedge_rule.update_model(hedge_rule)
                    self.assertIsNotNone(updated.model)
                    print(updated.model)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

if __name__ == '__main__':
    unittest.main()
