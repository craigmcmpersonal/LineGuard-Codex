import datetime
import unittest

from asyncpg.pool import Pool

from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.book import Book
from develop.persistence.model.hedge_opportunity import HedgeOpportunity
from develop.persistence.model.hedge_rule import HedgeRule
from develop.persistence.model.rule_evaluation_log import RuleEvaluationLog
from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest
import test.test_contants as test_constants


class TestHedgeOpportunityBetLegStorageAdapter(BaseStorageAdapterTest):
    async def test_rule_evaluation_log_storage_adapter_creates_rule_evaluation_log_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await self._create_book(storage_adapter)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            storage_adapter,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            storage_adapter,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    storage_adapter,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await storage_adapter.rule_evaluation_log.create(
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
                                    await storage_adapter.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await storage_adapter.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

    async def test_rule_evaluation_log_storage_adapter_finds_rule_evaluation_log_record_by_bet_slip_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await self._create_book(storage_adapter)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            storage_adapter,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            storage_adapter,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    storage_adapter,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await storage_adapter.rule_evaluation_log.create(
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
                                        await storage_adapter.rule_evaluation_log.find_by_bet_slip(
                                        bet_slip.key
                                    )
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(rule_evaluation_log.key, retrieved[0].key)
                                finally:
                                    await storage_adapter.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await storage_adapter.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

    async def test_rule_evaluation_log_storage_adapter_finds_rule_evaluation_log_record_by_hedge_rule_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await self._create_book(storage_adapter)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            storage_adapter,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            storage_adapter,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    storage_adapter,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await storage_adapter.rule_evaluation_log.create(
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
                                        await storage_adapter.rule_evaluation_log.find_by_hedge_rule(
                                            hedge_rule.key
                                        )
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(rule_evaluation_log.key, retrieved[0].key)
                                finally:
                                    await storage_adapter.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await storage_adapter.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

    async def test_rule_evaluation_log_storage_adapter_gets_rule_evaluation_log_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            book: Book = await self._create_book(storage_adapter)
            try:
                bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                try:
                    user_hedge_profile: UserHedgeProfile = \
                        await self._create_user_hedge_profile(
                            storage_adapter,
                            user_key=bet_slip.user_key
                        )
                    try:
                        hedge_rule: HedgeRule = await self._create_hedge_rule(
                            storage_adapter,
                            user_hedge_profile
                        )
                        try:
                            hedge_opportunity: HedgeOpportunity = \
                                await self._create_hedge_opportunity(
                                    storage_adapter,
                                    hedge_rule,
                                    bet_slip
                                )
                            try:
                                rule_evaluation_log: RuleEvaluationLog = \
                                    await storage_adapter.rule_evaluation_log.create(
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
                                        await storage_adapter.rule_evaluation_log.try_get(
                                            rule_evaluation_log.key
                                        )
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(rule_evaluation_log.key, retrieved.key)
                                finally:
                                    await storage_adapter.rule_evaluation_log.try_delete(
                                        rule_evaluation_log
                                    )
                            finally:
                                await storage_adapter.hedge_opportunity.try_delete(
                                    hedge_opportunity
                                )
                        finally:
                            await storage_adapter.hedge_rule.try_delete(hedge_rule)
                    finally:
                        await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
                finally:
                    await storage_adapter.bet_slip.try_delete(bet_slip)
            finally:
                await storage_adapter.book.try_delete(book)

if __name__ == '__main__':
    unittest.main()
