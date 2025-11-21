import datetime
import unittest

from asyncpg.pool import Pool

from develop.persistance.model.bet_slip import BetSlip
from develop.persistance.model import Book
from develop.persistance.model import HedgeOpportunity
from develop.persistance.model.hedge_rule import HedgeRule
from develop.persistance.model import RuleEvaluationLog
from develop.persistance.model import UserHedgeProfile
from develop.persistance.repository import Repository
from develop.persistance.postgresql_pool_factory import create_pool_async
from test.persistence.base_repository_test import BaseRepositoryTest
import test.test_contants as test_constants


class TestHedgeOpportunityBetLegRepository(BaseRepositoryTest):
    async def test_rule_evaluation_log_repository_creates_rule_evaluation_log_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            book: Book = await self._create_book(repository)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            repository,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            repository,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    repository,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await repository.rule_evaluation_log.create(
                                        hedge_rule.key,
                                        bet_slip.key,
                                        evaluation_time=datetime.datetime.now(
                                            datetime.timezone.utc
                                        ),
                                        inputs=test_constants.MARKET_PARAMETERS,
                                        output=test_constants.MARKET_PARAMETERS
                                    )
                                self.assertIsNotNone(rule_evaluation_log)
                                self.assertIsNotNone(rule_evaluation_log.key)
                                try:
                                    serialized: str = \
                                        rule_evaluation_log.model_dump_json()
                                    print(serialized)
                                finally:
                                    await repository.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await repository.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.bet_slip.try_delete(bet_slip)
            finally:
                await repository.book.try_delete(book)

    async def test_rule_evaluation_log_repository_finds_rule_evaluation_log_record_by_bet_slip_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            book: Book = await self._create_book(repository)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            repository,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            repository,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    repository,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await repository.rule_evaluation_log.create(
                                        hedge_rule.key,
                                        bet_slip.key,
                                        evaluation_time=datetime.datetime.now(
                                            datetime.timezone.utc
                                        ),
                                        inputs=test_constants.MARKET_PARAMETERS,
                                        output=test_constants.MARKET_PARAMETERS
                                    )
                                self.assertIsNotNone(rule_evaluation_log)
                                self.assertIsNotNone(rule_evaluation_log.key)
                                try:
                                    retrieved: list[RuleEvaluationLog] = \
                                        await repository.rule_evaluation_log.find_by_bet_slip(
                                        bet_slip.key
                                    )
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(rule_evaluation_log.key, retrieved[0].key)
                                finally:
                                    await repository.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await repository.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.bet_slip.try_delete(bet_slip)
            finally:
                await repository.book.try_delete(book)

    async def test_rule_evaluation_log_repository_finds_rule_evaluation_log_record_by_hedge_rule_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            book: Book = await self._create_book(repository)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            repository,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            repository,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    repository,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await repository.rule_evaluation_log.create(
                                        hedge_rule.key,
                                        bet_slip.key,
                                        evaluation_time=datetime.datetime.now(
                                            datetime.timezone.utc
                                        ),
                                        inputs=test_constants.MARKET_PARAMETERS,
                                        output=test_constants.MARKET_PARAMETERS
                                    )
                                self.assertIsNotNone(rule_evaluation_log)
                                self.assertIsNotNone(rule_evaluation_log.key)
                                try:
                                    retrieved: list[RuleEvaluationLog] = \
                                        await repository.rule_evaluation_log.find_by_hedge_rule(
                                            hedge_rule.key
                                        )
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(rule_evaluation_log.key, retrieved[0].key)
                                finally:
                                    await repository.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await repository.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.bet_slip.try_delete(bet_slip)
            finally:
                await repository.book.try_delete(book)

    async def test_rule_evaluation_log_repository_gets_rule_evaluation_log_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            book: Book = await self._create_book(repository)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            repository,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            repository,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    repository,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await repository.rule_evaluation_log.create(
                                        hedge_rule.key,
                                        bet_slip.key,
                                        evaluation_time=datetime.datetime.now(
                                            datetime.timezone.utc
                                        ),
                                        inputs=test_constants.MARKET_PARAMETERS,
                                        output=test_constants.MARKET_PARAMETERS
                                    )
                                self.assertIsNotNone(rule_evaluation_log)
                                self.assertIsNotNone(rule_evaluation_log.key)
                                try:
                                    retrieved: list[RuleEvaluationLog] = \
                                        await repository.rule_evaluation_log.try_get(
                                            rule_evaluation_log.key
                                        )
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(rule_evaluation_log.key, retrieved.key)
                                finally:
                                    await repository.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await repository.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await repository.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await repository.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await repository.bet_slip.try_delete(bet_slip)
            finally:
                await repository.book.try_delete(book)

if __name__ == '__main__':
    unittest.main()
