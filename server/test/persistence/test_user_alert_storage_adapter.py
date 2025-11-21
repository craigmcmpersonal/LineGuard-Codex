import datetime
import unittest
import uuid

from asyncpg.pool import Pool

from develop.persistence.model.alert_type import AlertType
from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.book import Book
from develop.persistence.model.hedge_opportunity import HedgeOpportunity
from develop.persistence.model.hedge_rule import HedgeRule
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.sport import Sport
from develop.persistence.model.user_alert import UserAlert
from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestUserAlertStorageAdapter(BaseStorageAdapterTest):
    async def test_user_alert_storage_adapter_creates_user_alert_record_async(self):
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
                                        text: str = compose_unique_identifier()
                                        time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await storage_adapter.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            resource_location=text,
                                            creation_time=time,
                                            sent_time=time,
                                            alert_type=AlertType.HEDGE_OPPORTUNITY,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            serialized: str = user_alert.model_dump_json()
                                            print(serialized)
                                        finally:
                                            await storage_adapter.user_alert.try_delete(user_alert)
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

    async def test_user_alert_storage_adapter_finds_user_alert_record_by_user_async(self):
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
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await storage_adapter.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            retrieved: list[UserAlert] = await storage_adapter.user_alert.find_by_user(
                                                user_hedge_profile.user_key
                                            )
                                            self.assertIsNotNone(retrieved)
                                            if (count := len(retrieved)) != 1:
                                                self.fail(count)
                                            else:
                                                self.assertEqual(user_alert.key, retrieved[0].key)
                                        finally:
                                            await storage_adapter.user_alert.try_delete(user_alert)
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

    async def test_user_alert_storage_adapter_finds_user_alert_record_by_public_key_async(self):
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
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await storage_adapter.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            retrieved: UserAlert = await storage_adapter.user_alert.try_find_by_public_key(
                                                user_alert.public_key
                                            )
                                            self.assertIsNotNone(retrieved)
                                            self.assertEqual(user_alert.key, retrieved.key)
                                        finally:
                                            await storage_adapter.user_alert.try_delete(user_alert)
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

    async def test_user_alert_storage_adapter_gets_user_alert_record_async(self):
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
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await storage_adapter.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            retrieved: UserAlert = await storage_adapter.user_alert.try_get(
                                                user_alert.key
                                            )
                                            self.assertIsNotNone(retrieved)
                                            self.assertEqual(user_alert.key, retrieved.key)
                                        finally:
                                            await storage_adapter.user_alert.try_delete(user_alert)
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

    async def test_user_alert_storage_adapter_updates_user_alert_record_async(self):
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
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await storage_adapter.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            user_alert.sent_time = datetime.datetime.now(datetime.timezone.utc)
                                            updated: UserAlert = await storage_adapter.user_alert.update(
                                                user_alert
                                            )
                                            self.assertIsNotNone(updated)
                                            self.assertEqual(user_alert.sent_time, updated.sent_time)
                                        finally:
                                            await storage_adapter.user_alert.try_delete(user_alert)
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
