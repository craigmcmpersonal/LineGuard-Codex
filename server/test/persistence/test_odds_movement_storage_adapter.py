import unittest
from decimal import Decimal

from asyncpg import Pool

from develop.persistence.model.book import Book
from develop.persistence.model.event import Event
from develop.persistence.model.market import Market
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.odds_movement import OddsMovement
from develop.persistence.model.sport import Sport
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.persistence.storage_adapter import StorageAdapter
from develop.utility import compose_unique_identifier
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestOddsMovementStorageAdapter(BaseStorageAdapterTest):
    async def test_odds_movement_storage_adapter_creates_odds_movement_record(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            market_type: MarketType = await self._create_market_type(storage_adapter)
            try:
                sport: Sport = await self._create_sport(storage_adapter)
                try:
                    event: Event = await self._create_event(storage_adapter, sport)
                    try:
                        market: Market = await self._create_market(storage_adapter, event, market_type)
                        try:
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                value: int = 50
                                decimal_value: Decimal = Decimal(value)
                                odds_movement: OddsMovement = await storage_adapter.odds_movement.create(
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
                                    await storage_adapter.odds_movement.try_delete(odds_movement)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.event.try_delete(event)
                finally:
                    await storage_adapter.sport.try_delete(sport)
            finally:
                await storage_adapter.market_type.try_delete(market_type)

    async def test_odds_movement_storage_adapter_finds_odds_movement_record(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            market_type: MarketType = await self._create_market_type(storage_adapter)
            try:
                sport: Sport = await self._create_sport(storage_adapter)
                try:
                    event: Event = await self._create_event(storage_adapter, sport)
                    try:
                        market: Market = await self._create_market(storage_adapter, event, market_type)
                        try:
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                value: int = 50
                                decimal_value: Decimal = Decimal(value)
                                odds_movement: OddsMovement = await storage_adapter.odds_movement.create(
                                    book.key,
                                    market.key,
                                    compose_unique_identifier(),
                                    decimal_value,
                                    old_value=decimal_value,
                                    change_percentage=decimal_value
                                )
                                try:
                                    retrieved: list[OddsMovement] = await storage_adapter.odds_movement.find(market.key)
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(odds_movement.key, retrieved[0].key)
                                finally:
                                    await storage_adapter.odds_movement.try_delete(odds_movement)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.event.try_delete(event)
                finally:
                    await storage_adapter.sport.try_delete(sport)
            finally:
                await storage_adapter.market_type.try_delete(market_type)

    async def test_odds_movement_storage_adapter_gets_odds_movement_record(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            market_type: MarketType = await self._create_market_type(storage_adapter)
            try:
                sport: Sport = await self._create_sport(storage_adapter)
                try:
                    event: Event = await self._create_event(storage_adapter, sport)
                    try:
                        market: Market = await self._create_market(storage_adapter, event, market_type)
                        try:
                            book: Book = await self._create_book(storage_adapter)
                            try:
                                value: int = 50
                                decimal_value: Decimal = Decimal(value)
                                odds_movement: OddsMovement = await storage_adapter.odds_movement.create(
                                    book.key,
                                    market.key,
                                    compose_unique_identifier(),
                                    decimal_value,
                                    old_value=decimal_value,
                                    change_percentage=decimal_value
                                )
                                try:
                                    retrieved: OddsMovement = await storage_adapter.odds_movement.try_get(
                                        odds_movement.key
                                    )
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(odds_movement.key, retrieved.key)
                                finally:
                                    await storage_adapter.odds_movement.try_delete(odds_movement)
                            finally:
                                await storage_adapter.book.try_delete(book)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.event.try_delete(event)
                finally:
                    await storage_adapter.sport.try_delete(sport)
            finally:
                await storage_adapter.market_type.try_delete(market_type)


if __name__ == '__main__':
    unittest.main()
