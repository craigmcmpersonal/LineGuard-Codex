import datetime
import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.persistance.model.bet_slip import BetSlip
from develop.persistance.model import Book
from develop.persistance.model import HedgeOpportunity
from develop.persistance.model import HedgeOpportunityStatus
from develop.persistance.model.hedge_rule import HedgeRule
from develop.persistance.model import MarketType
from develop.persistance.model import Sport
from develop.persistance.model import UserHedgeProfile
from develop.persistance.repository import Repository
from develop.persistance.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
from test.persistence.base_repository_test import BaseRepositoryTest


class TestHedgeOpportunityRepository(BaseRepositoryTest):
    async def test_hedge_opportunity_repository_creates_hedge_opportunity_record_async(self):
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
                                    trigger_reason: str = compose_unique_identifier()
                                    hedge_opportunity: HedgeOpportunity = await repository.hedge_opportunity.create(
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

    async def test_hedge_opportunity_repository_finds_hedge_opportunity_record_by_bet_slip_async(self):
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
                                        retrieved: list[HedgeOpportunity] = \
                                            await repository.hedge_opportunity.find_by_bet_slip(bet_slip.key)
                                        self.assertIsNotNone(retrieved)
                                        if (count := len(retrieved)) != 1:
                                            self.fail(count)
                                        else:
                                            self.assertEqual(hedge_opportunity.key, retrieved[0].key)
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

    async def test_hedge_opportunity_repository_finds_hedge_opportunity_record_by_hedge_rule_async(self):
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
                                        retrieved: list[HedgeOpportunity] = \
                                            await repository.hedge_opportunity.find_by_hedge_rule(hedge_rule.key)
                                        self.assertIsNotNone(retrieved)
                                        if (count := len(retrieved)) != 1:
                                            self.fail(count)
                                        else:
                                            self.assertEqual(hedge_opportunity.key, retrieved[0].key)
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

    async def test_hedge_opportunity_repository_finds_hedge_opportunity_record_by_user_async(self):
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
                                bet_slip: BetSlip = await self._create_bet_slip(
                                    repository,
                                    book, user_key=user_hedge_profile.user_key
                                )
                                try:
                                    hedge_opportunity: HedgeOpportunity = await repository.hedge_opportunity.create(
                                        bet_slip.key,
                                        hedge_rule.key
                                    )
                                    self.assertIsNotNone(hedge_opportunity)
                                    self.assertIsNotNone(hedge_opportunity.key)
                                    try:
                                        retrieved: list[HedgeOpportunity] = \
                                            await repository.hedge_opportunity.find_by_user(bet_slip.user_key)
                                        self.assertIsNotNone(retrieved)
                                        if (count := len(retrieved)) != 1:
                                            self.fail(count)
                                        else:
                                            self.assertEqual(hedge_opportunity.key, retrieved[0].key)
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

    async def test_hedge_opportunity_repository_gets_hedge_opportunity_record_async(self):
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
                                        retrieved: HedgeOpportunity = await repository.hedge_opportunity.try_get(
                                            hedge_opportunity.key
                                        )
                                        self.assertIsNotNone(retrieved)
                                        self.assertEqual(hedge_opportunity.key, retrieved.key)
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

    async def test_hedge_opportunity_repository_updates_opportunity_record_async(self):
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
                                        hedge_opportunity.status = HedgeOpportunityStatus.EXPIRED
                                        hedge_opportunity.expiration_time = datetime.datetime.now(
                                            datetime.timezone.utc
                                        )
                                        updated: HedgeOpportunity = await repository.hedge_opportunity.update(
                                            hedge_opportunity
                                        )
                                        self.assertIsNotNone(updated)
                                        self.assertEqual(hedge_opportunity.key, updated.key)
                                        self.assertEqual(hedge_opportunity.status, updated.status)
                                        self.assertEqual(hedge_opportunity.expiration_time, updated.expiration_time)
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
