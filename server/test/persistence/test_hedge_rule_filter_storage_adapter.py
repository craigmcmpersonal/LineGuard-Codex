import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.persistence.model.hedge_rule import HedgeRule
from develop.persistence.model.hedge_rule_filter import HedgeRuleFilter
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.sport import Sport
from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestHedgeRuleFilterStorageAdapter(BaseStorageAdapterTest):
    async def test_hedge_rule_filter_storage_adapter_creates_hedge_rule_filter_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await self._create_sport(storage_adapter)
            try:
                market_type: MarketType = await self._create_market_type(storage_adapter)
                try:
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
                            hedge_rule_filter: HedgeRuleFilter = await storage_adapter.hedge_rule_filter.create(
                                hedge_rule.key,
                                sport_key=sport.key,
                                market_type_key=market_type.key,
                                minimum_odds=Decimal(2.0),
                                maximum_odds=Decimal(3.0)
                            )
                            self.assertIsNotNone(hedge_rule_filter)
                            self.assertIsNotNone(hedge_rule_filter.key)
                            try:
                                serialized: str = user_hedge_profile.model_dump_json()
                                print(serialized)
                            finally:
                                await storage_adapter.hedge_rule_filter.try_delete(hedge_rule_filter)
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.market_type.try_delete(market_type)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_hedge_rule_filter_storage_adapter_finds_hedge_rule_filter_record_async(self):
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
                    hedge_rule_filter: HedgeRuleFilter = await storage_adapter.hedge_rule_filter.create(
                        hedge_rule.key,
                        minimum_odds=Decimal(2.0),
                        maximum_odds=Decimal(3.0)
                    )
                    self.assertIsNotNone(hedge_rule_filter)
                    self.assertIsNotNone(hedge_rule_filter.key)
                    try:
                        retrieved: list[HedgeRuleFilter] = await storage_adapter.hedge_rule_filter.find(
                            hedge_rule.key
                        )
                        self.assertIsNotNone(retrieved)
                        if (count := len(retrieved)) != 1:
                            self.fail(count)
                        else:
                            self.assertEqual(hedge_rule_filter.key, retrieved[0].key)
                    finally:
                        await storage_adapter.hedge_rule_filter.try_delete(hedge_rule_filter)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_filter_storage_adapter_gets_hedge_rule_filter_record_async(self):
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
                    hedge_rule_filter: HedgeRuleFilter = await storage_adapter.hedge_rule_filter.create(
                        hedge_rule.key,
                        minimum_odds=Decimal(2.0),
                        maximum_odds=Decimal(3.0)
                    )
                    self.assertIsNotNone(hedge_rule_filter)
                    self.assertIsNotNone(hedge_rule_filter.key)
                    try:
                        retrieved: HedgeRuleFilter = await storage_adapter.hedge_rule_filter.try_get(
                            hedge_rule_filter.key
                        )
                        self.assertIsNotNone(retrieved)
                        self.assertEqual(hedge_rule_filter.key, retrieved.key)
                    finally:
                        await storage_adapter.hedge_rule_filter.try_delete(hedge_rule_filter)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

    async def test_hedge_rule_filter_storage_adapter_updates_hedge_rule_filter_record_async(self):
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
                    hedge_rule_filter: HedgeRuleFilter = await storage_adapter.hedge_rule_filter.create(
                        hedge_rule.key,
                        minimum_odds=Decimal(2.0),
                        maximum_odds=Decimal(3.0)
                    )
                    self.assertIsNotNone(hedge_rule_filter)
                    self.assertIsNotNone(hedge_rule_filter.key)
                    try:
                        difference: Decimal = Decimal(1.0)
                        hedge_rule_filter.minimum_odds = hedge_rule_filter.minimum_odds - difference
                        hedge_rule_filter.maximum_odds = hedge_rule_filter.maximum_odds + difference
                        updated: HedgeRuleFilter = await storage_adapter.hedge_rule_filter.update(
                            hedge_rule_filter
                        )
                        self.assertIsNotNone(updated)
                        self.assertEqual(hedge_rule_filter.minimum_odds, updated.minimum_odds)
                        self.assertEqual(hedge_rule_filter.maximum_odds, updated.maximum_odds)
                    finally:
                        await storage_adapter.hedge_rule_filter.try_delete(hedge_rule_filter)
                finally:
                    await storage_adapter.hedge_rule.try_delete(hedge_rule)
            finally:
                await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)

if __name__ == '__main__':
    unittest.main()
