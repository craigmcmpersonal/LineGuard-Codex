import datetime
import unittest
import uuid

from asyncpg.pool import Pool

from develop.persistance.model import AlertType
from develop.persistance.model.bet_slip import BetSlip
from develop.persistance.model import Book
from develop.persistance.model import HedgeOpportunity
from develop.persistance.model.hedge_rule import HedgeRule
from develop.persistance.model import MarketType
from develop.persistance.model import Sport
from develop.persistance.model import UserAlert
from develop.persistance.model import UserHedgeProfile
from develop.persistance.repository import Repository
from develop.persistance.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
from test.persistence.base_repository_test import BaseRepositoryTest


class TestUserAlertRepository(BaseRepositoryTest):
    async def test_user_alert_repository_creates_user_alert_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                market_type: MarketType = await self._create_market_type(repository)
                try:
                    user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(repository)
                    try:
                        rule_name: str = compose_unique_identifier()
                        original: str = compose_unique_identifier()
                        hedge_rule: HedgeRule = await repository.hedge_rule.create(
                            user_hedge_profile.key,
                            rule_name,
                            original
                        )
                        self.assertIsNotNone(hedge_rule)
                        self.assertIsNotNone(hedge_rule.key)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await repository.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        text: str = compose_unique_identifier()
                                        time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await repository.user_alert.create(
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
                                            await repository.user_alert.try_delete(user_alert)
                                    finally:
                                        await repository.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await repository.bet_slip.try_delete(bet_slip)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.market_type.try_delete(market_type)
            finally:
                await repository.sport.try_delete(sport)

    async def test_user_alert_repository_finds_user_alert_record_by_user_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                market_type: MarketType = await self._create_market_type(repository)
                try:
                    user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(repository)
                    try:
                        rule_name: str = compose_unique_identifier()
                        original: str = compose_unique_identifier()
                        hedge_rule: HedgeRule = await repository.hedge_rule.create(
                            user_hedge_profile.key,
                            rule_name,
                            original
                        )
                        self.assertIsNotNone(hedge_rule)
                        self.assertIsNotNone(hedge_rule.key)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await repository.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await repository.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            retrieved: list[UserAlert] = await repository.user_alert.find_by_user(
                                                user_hedge_profile.user_key
                                            )
                                            self.assertIsNotNone(retrieved)
                                            if (count := len(retrieved)) != 1:
                                                self.fail(count)
                                            else:
                                                self.assertEqual(user_alert.key, retrieved[0].key)
                                        finally:
                                            await repository.user_alert.try_delete(user_alert)
                                    finally:
                                        await repository.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await repository.bet_slip.try_delete(bet_slip)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.market_type.try_delete(market_type)
            finally:
                await repository.sport.try_delete(sport)

    async def test_user_alert_repository_finds_user_alert_record_by_public_key_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                market_type: MarketType = await self._create_market_type(repository)
                try:
                    user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(repository)
                    try:
                        rule_name: str = compose_unique_identifier()
                        original: str = compose_unique_identifier()
                        hedge_rule: HedgeRule = await repository.hedge_rule.create(
                            user_hedge_profile.key,
                            rule_name,
                            original
                        )
                        self.assertIsNotNone(hedge_rule)
                        self.assertIsNotNone(hedge_rule.key)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await repository.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await repository.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            retrieved: UserAlert = await repository.user_alert.try_find_by_public_key(
                                                user_alert.public_key
                                            )
                                            self.assertIsNotNone(retrieved)
                                            self.assertEqual(user_alert.key, retrieved.key)
                                        finally:
                                            await repository.user_alert.try_delete(user_alert)
                                    finally:
                                        await repository.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await repository.bet_slip.try_delete(bet_slip)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.market_type.try_delete(market_type)
            finally:
                await repository.sport.try_delete(sport)

    async def test_user_alert_repository_gets_user_alert_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                market_type: MarketType = await self._create_market_type(repository)
                try:
                    user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(repository)
                    try:
                        rule_name: str = compose_unique_identifier()
                        original: str = compose_unique_identifier()
                        hedge_rule: HedgeRule = await repository.hedge_rule.create(
                            user_hedge_profile.key,
                            rule_name,
                            original
                        )
                        self.assertIsNotNone(hedge_rule)
                        self.assertIsNotNone(hedge_rule.key)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await repository.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await repository.user_alert.create(
                                            user_hedge_profile.user_key,
                                            text,
                                            text,
                                            hedge_opportunity_key=hedge_opportunity.key,
                                            public_key=identifier
                                        )
                                        self.assertIsNotNone(user_alert)
                                        self.assertIsNotNone(user_alert.key)
                                        try:
                                            retrieved: UserAlert = await repository.user_alert.try_get(
                                                user_alert.key
                                            )
                                            self.assertIsNotNone(retrieved)
                                            self.assertEqual(user_alert.key, retrieved.key)
                                        finally:
                                            await repository.user_alert.try_delete(user_alert)
                                    finally:
                                        await repository.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await repository.bet_slip.try_delete(bet_slip)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.market_type.try_delete(market_type)
            finally:
                await repository.sport.try_delete(sport)

    async def test_user_alert_repository_updates_user_alert_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                market_type: MarketType = await self._create_market_type(repository)
                try:
                    user_hedge_profile: UserHedgeProfile = await self._create_user_hedge_profile(repository)
                    try:
                        rule_name: str = compose_unique_identifier()
                        original: str = compose_unique_identifier()
                        hedge_rule: HedgeRule = await repository.hedge_rule.create(
                            user_hedge_profile.key,
                            rule_name,
                            original
                        )
                        self.assertIsNotNone(hedge_rule)
                        self.assertIsNotNone(hedge_rule.key)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                try:
                                    hedge_opportunity: HedgeOpportunity = await repository.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        text: str = compose_unique_identifier()
                                        identifier: uuid.UUID = uuid.uuid4()
                                        user_alert: UserAlert = await repository.user_alert.create(
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
                                            updated: UserAlert = await repository.user_alert.update(
                                                user_alert
                                            )
                                            self.assertIsNotNone(updated)
                                            self.assertEqual(user_alert.sent_time, updated.sent_time)
                                        finally:
                                            await repository.user_alert.try_delete(user_alert)
                                    finally:
                                        await repository.hedge_opportunity.try_delete(hedge_opportunity)
                                finally:
                                    await repository.bet_slip.try_delete(bet_slip)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.market_type.try_delete(market_type)
            finally:
                await repository.sport.try_delete(sport)

if __name__ == '__main__':
    unittest.main()
