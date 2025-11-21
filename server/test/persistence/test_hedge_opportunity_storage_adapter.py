import datetime
import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.book import Book
from develop.persistence.model.hedge_opportunity import HedgeOpportunity
from develop.persistence.model.hedge_opportunity_status import HedgeOpportunityStatus
from develop.persistence.model.hedge_rule import HedgeRule
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.sport import Sport
from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestHedgeOpportunityStorageAdapter(BaseStorageAdapterTest):
    async def test_hedge_opportunity_storage_adapter_creates_hedge_opportunity_record_async(self):
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
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                try:
                                    trigger_reason: str = compose_unique_identifier()
                                    hedge_opportunity: HedgeOpportunity = await storage_adapter.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key,
                                        trigger_reason=trigger_reason,
                                        original_win_probability=Decimal(1),
                                        recommended_hedge_stake=Decimal(50.50),
                                        optimal_hedge_odds=Decimal(0.5),
                                        status=HedgeOpportunityStatus.ACTIVE
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        serialized: str = user_hedge_profile.model_dump_json()
                                        print(serialized)
                                    finally:
                                        await storage_adapter.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await storage_adapter.bet_slip.try_delete(bet_slip)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.market_type.try_delete(market_type)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_hedge_opportunity_storage_adapter_finds_hedge_opportunity_record_by_bet_slip_async(self):
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
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await storage_adapter.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        retrieved: list[HedgeOpportunity] = \
                                            await storage_adapter.hedge_opportunity.find_by_bet_slip(bet_slip.key)
                                        self.assertIsNotNone(retrieved)
                                        if (count := len(retrieved)) != 1:
                                            self.fail(count)
                                        else:
                                            self.assertEqual(hedge_opportunity.key, retrieved[0].key)
                                    finally:
                                        await storage_adapter.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await storage_adapter.bet_slip.try_delete(bet_slip)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.market_type.try_delete(market_type)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_hedge_opportunity_storage_adapter_finds_hedge_opportunity_record_by_hedge_rule_async(self):
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
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await storage_adapter.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        retrieved: list[HedgeOpportunity] = \
                                            await storage_adapter.hedge_opportunity.find_by_hedge_rule(hedge_rule.key)
                                        self.assertIsNotNone(retrieved)
                                        if (count := len(retrieved)) != 1:
                                            self.fail(count)
                                        else:
                                            self.assertEqual(hedge_opportunity.key, retrieved[0].key)
                                    finally:
                                        await storage_adapter.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await storage_adapter.bet_slip.try_delete(bet_slip)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.market_type.try_delete(market_type)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_hedge_opportunity_storage_adapter_finds_hedge_opportunity_record_by_user_async(self):
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
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(
                                    storage_adapter,
                                    book, user_key=user_hedge_profile.user_key
                                )
                                try:
                                    hedge_opportunity: HedgeOpportunity = await storage_adapter.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        retrieved: list[HedgeOpportunity] = \
                                            await storage_adapter.hedge_opportunity.find_by_user(bet_slip.user_key)
                                        self.assertIsNotNone(retrieved)
                                        if (count := len(retrieved)) != 1:
                                            self.fail(count)
                                        else:
                                            self.assertEqual(hedge_opportunity.key, retrieved[0].key)
                                    finally:
                                        await storage_adapter.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await storage_adapter.bet_slip.try_delete(bet_slip)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.market_type.try_delete(market_type)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_hedge_opportunity_storage_adapter_gets_hedge_opportunity_record_async(self):
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
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await storage_adapter.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        retrieved: HedgeOpportunity = await storage_adapter.hedge_opportunity.try_get(
                                            hedge_opportunity.key
                                        )
                                        self.assertIsNotNone(retrieved)
                                        self.assertEqual(hedge_opportunity.key, retrieved.key)
                                    finally:
                                        await storage_adapter.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await storage_adapter.bet_slip.try_delete(bet_slip)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.market_type.try_delete(market_type)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_hedge_opportunity_storage_adapter_updates_opportunity_record_async(self):
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
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await storage_adapter.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        hedge_opportunity.status = HedgeOpportunityStatus.EXPIRED
                                        hedge_opportunity.expiration_time = datetime.datetime.now(
                                            datetime.timezone.utc
                                        )
                                        updated: HedgeOpportunity = await storage_adapter.hedge_opportunity.update(
                                            hedge_opportunity
                                        )
                                        self.assertIsNotNone(updated)
                                        self.assertEqual(hedge_opportunity.key, updated.key)
                                        self.assertEqual(hedge_opportunity.status, updated.status)
                                        self.assertEqual(hedge_opportunity.expiration_time, updated.expiration_time)
                                    finally:
                                        await storage_adapter.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await storage_adapter.bet_slip.try_delete(bet_slip)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.market_type.try_delete(market_type)
            finally:
                await storage_adapter.sport.try_delete(sport)

if __name__ == '__main__':
    unittest.main()
