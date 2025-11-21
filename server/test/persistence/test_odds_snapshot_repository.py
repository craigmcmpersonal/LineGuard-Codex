import unittest
from decimal import Decimal

from asyncpg import Pool

from develop.persistance.model import Book
from develop.persistance.model import Event
from develop.persistance.model import Market
from develop.persistance.model import MarketType
from develop.persistance.model import OddsSnapshot
from develop.persistance.model import Sport
from develop.persistance.postgresql_pool_factory import create_pool_async
from develop.persistance.repository import Repository
import test.test_contants as test_constants
from test.persistence.base_repository_test import BaseRepositoryTest


class TestOddsSnapshotRepository(BaseRepositoryTest):
    async def test_odds_snapshot_repository_creates_odds_snapshot_record(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            market_type: MarketType = await self._create_market_type(repository)
            try:
                sport: Sport = await self._create_sport(repository)
                try:
                    event: Event = await self._create_event(repository, sport)
                    try:
                        market: Market = await self._create_market(repository, event, market_type)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                value: int = 50
                                decimal_value: Decimal = Decimal(value)
                                odds_snapshot: OddsSnapshot = await repository.odds_snapshot.create(
                                    book.key,
                                    market.key,
                                    test_constants.MARKET_PARAMETERS,
                                    live=True,
                                    home_price=value,
                                    away_price=value,
                                    home_spread=decimal_value,
                                    home_spread_price=value,
                                    away_spread=decimal_value,
                                    away_spread_price=value,
                                    over_total=decimal_value,
                                    over_price=value,
                                    under_total=decimal_value,
                                    under_price=value,
                                )
                                self.assertIsNotNone(odds_snapshot)
                                self.assertIsNotNone(odds_snapshot.key)
                                try:
                                    serialized: str = odds_snapshot.model_dump_json()
                                    print(serialized)
                                finally:
                                    await repository.odds_snapshot.try_delete(odds_snapshot)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.market.try_delete(market)
                    finally:
                        await repository.event.try_delete(event)
                finally:
                    await repository.sport.try_delete(sport)
            finally:
                await repository.market_type.try_delete(market_type)

    async def test_odds_snapshot_repository_finds_odds_snapshot_record(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            market_type: MarketType = await self._create_market_type(repository)
            try:
                sport: Sport = await self._create_sport(repository)
                try:
                    event: Event = await self._create_event(repository, sport)
                    try:
                        market: Market = await self._create_market(repository, event, market_type)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                odds_snapshot: OddsSnapshot = await repository.odds_snapshot.create(
                                    book.key,
                                    market.key,
                                    test_constants.MARKET_PARAMETERS,
                                )
                                self.assertIsNotNone(odds_snapshot)
                                self.assertIsNotNone(odds_snapshot.key)
                                try:
                                    retrieved: list[OddsSnapshot] = await repository.odds_snapshot.find(market.key)
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(odds_snapshot.key, retrieved[0].key)
                                finally:
                                    await repository.odds_snapshot.try_delete(odds_snapshot)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.market.try_delete(market)
                    finally:
                        await repository.event.try_delete(event)
                finally:
                    await repository.sport.try_delete(sport)
            finally:
                await repository.market_type.try_delete(market_type)

    async def test_odds_snapshot_repository_gets_odds_snapshot_record(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            market_type: MarketType = await self._create_market_type(repository)
            try:
                sport: Sport = await self._create_sport(repository)
                try:
                    event: Event = await self._create_event(repository, sport)
                    try:
                        market: Market = await self._create_market(repository, event, market_type)
                        try:
                            book: Book = await self._create_book(repository)
                            try:
                                odds_snapshot: OddsSnapshot = await repository.odds_snapshot.create(
                                    book.key,
                                    market.key,
                                    test_constants.MARKET_PARAMETERS,
                                )
                                self.assertIsNotNone(odds_snapshot)
                                self.assertIsNotNone(odds_snapshot.key)
                                try:
                                    retrieved: OddsSnapshot = await repository.odds_snapshot.try_get(odds_snapshot.key)
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(odds_snapshot.key, retrieved.key)
                                finally:
                                    await repository.odds_snapshot.try_delete(odds_snapshot)
                            finally:
                                await repository.book.try_delete(book)
                        finally:
                            await repository.market.try_delete(market)
                    finally:
                        await repository.event.try_delete(event)
                finally:
                    await repository.sport.try_delete(sport)
            finally:
                await repository.market_type.try_delete(market_type)


if __name__ == '__main__':
    unittest.main()
