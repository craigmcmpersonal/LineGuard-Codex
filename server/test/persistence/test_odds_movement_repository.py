import unittest
from decimal import Decimal

from asyncpg import Pool

from develop.persistance.model import Book
from develop.persistance.model import Event
from develop.persistance.model import Market
from develop.persistance.model import MarketType
from develop.persistance.model import OddsMovement
from develop.persistance.model import Sport
from develop.persistance.postgresql_pool_factory import create_pool_async
from develop.persistance.repository import Repository
from develop.utility import compose_unique_identifier
from test.persistence.base_repository_test import BaseRepositoryTest


class TestOddsMovementRepository(BaseRepositoryTest):
    async def test_odds_movement_repository_creates_odds_movement_record(self):
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
                                odds_movement: OddsMovement = await repository.odds_movement.create(
                                    book.key,
                                    market.key,
                                    compose_unique_identifier(),
                                    decimal_value,
                                    old_value=decimal_value,
                                    change_percentage=decimal_value
                                )
                                self.assertIsNotNone(odds_movement)
                                self.assertIsNotNone(odds_movement.key)
                                try:
                                    serialized: str = odds_movement.model_dump_json()
                                    print(serialized)
                                finally:
                                    await repository.odds_movement.try_delete(odds_movement)
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

    async def test_odds_movement_repository_finds_odds_movement_record(self):
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
                                odds_movement: OddsMovement = await repository.odds_movement.create(
                                    book.key,
                                    market.key,
                                    compose_unique_identifier(),
                                    decimal_value,
                                    old_value=decimal_value,
                                    change_percentage=decimal_value
                                )
                                try:
                                    retrieved: list[OddsMovement] = await repository.odds_movement.find(market.key)
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(odds_movement.key, retrieved[0].key)
                                finally:
                                    await repository.odds_movement.try_delete(odds_movement)
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

    async def test_odds_movement_repository_gets_odds_movement_record(self):
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
                                odds_movement: OddsMovement = await repository.odds_movement.create(
                                    book.key,
                                    market.key,
                                    compose_unique_identifier(),
                                    decimal_value,
                                    old_value=decimal_value,
                                    change_percentage=decimal_value
                                )
                                try:
                                    retrieved: OddsMovement = await repository.odds_movement.try_get(
                                        odds_movement.key
                                    )
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(odds_movement.key, retrieved.key)
                                finally:
                                    await repository.odds_movement.try_delete(odds_movement)
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
