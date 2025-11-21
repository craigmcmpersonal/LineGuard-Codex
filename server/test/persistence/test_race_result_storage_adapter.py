import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.persistence.model.entrant import Entrant
from develop.persistence.model.event import Event
from develop.persistence.model.market import Market
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.race_result import RaceResult
from develop.persistence.model.sport import Sport
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestRaceResultStorageAdapter(BaseStorageAdapterTest):
    async def test_race_result_storage_adapter_creates_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await self._create_sport(storage_adapter)
            try:
                event: Event = await self._create_event(storage_adapter, sport)
                try:
                    market_type: MarketType = await self._create_market_type(storage_adapter)
                    try:
                        market: Market = await self._create_market(storage_adapter, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(storage_adapter, event)
                            try:
                                value: int = 3
                                decimal_value: Decimal = Decimal(value)
                                race_result: RaceResult = await storage_adapter.race_result.create(
                                    event.key,
                                    entrant.key,
                                    value,
                                    win_payout=decimal_value,
                                    place_payout=decimal_value
                                )
                                self.assertIsNotNone(race_result)
                                self.assertIsNotNone(race_result.key)
                                try:
                                    serialized: str = race_result.model_dump_json()
                                    print(serialized)
                                finally:
                                    await storage_adapter.race_result.try_delete(race_result)
                            finally:
                                await storage_adapter.entrant.try_delete(entrant)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.market_type.try_delete(market_type)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_race_result_storage_adapter_finds_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await self._create_sport(storage_adapter)
            try:
                event: Event = await self._create_event(storage_adapter, sport)
                try:
                    market_type: MarketType = await self._create_market_type(storage_adapter)
                    try:
                        market: Market = await self._create_market(storage_adapter, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(storage_adapter, event)
                            try:
                                value: int = 3
                                race_result: RaceResult = await storage_adapter.race_result.create(
                                    event.key,
                                    entrant.key,
                                    value
                                )
                                try:
                                    retrieved: list[RaceResult] = await storage_adapter.race_result.find(event.key)
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(race_result.key, retrieved[0].key)
                                finally:
                                    await storage_adapter.race_result.try_delete(race_result)
                            finally:
                                await storage_adapter.entrant.try_delete(entrant)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.market_type.try_delete(market_type)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_race_result_storage_adapter_gets_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await self._create_sport(storage_adapter)
            try:
                event: Event = await self._create_event(storage_adapter, sport)
                try:
                    market_type: MarketType = await self._create_market_type(storage_adapter)
                    try:
                        market: Market = await self._create_market(storage_adapter, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(storage_adapter, event)
                            try:
                                value: int = 3
                                race_result: RaceResult = await storage_adapter.race_result.create(
                                    event.key,
                                    entrant.key,
                                    value
                                )
                                try:
                                    retrieved: RaceResult = await storage_adapter.race_result.try_get(race_result.key)
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(race_result.key, retrieved.key)
                                finally:
                                    await storage_adapter.race_result.try_delete(race_result)
                            finally:
                                await storage_adapter.entrant.try_delete(entrant)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.market_type.try_delete(market_type)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_race_result_storage_adapter_updates_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await self._create_sport(storage_adapter)
            try:
                event: Event = await self._create_event(storage_adapter, sport)
                try:
                    market_type: MarketType = await self._create_market_type(storage_adapter)
                    try:
                        market: Market = await self._create_market(storage_adapter, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(storage_adapter, event)
                            try:
                                value: int = 3
                                race_result: RaceResult = await storage_adapter.race_result.create(
                                    event.key,
                                    entrant.key,
                                    value
                                )
                                try:
                                    race_result.position = race_result.position + 1
                                    race_result.win_payout = Decimal(value)
                                    race_result.place_payout = Decimal(race_result.position)
                                    self.assertNotEqual(race_result.win_payout, race_result.place_payout)
                                    updated: RaceResult = await storage_adapter.race_result.update(race_result)
                                    self.assertIsNotNone(updated)
                                    self.assertEqual(race_result.position, updated.position)
                                    self.assertEqual(race_result.win_payout, updated.win_payout)
                                    self.assertEqual(race_result.place_payout, updated.place_payout)
                                finally:
                                    await storage_adapter.race_result.try_delete(race_result)
                            finally:
                                await storage_adapter.entrant.try_delete(entrant)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.market_type.try_delete(market_type)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)


if __name__ == '__main__':
    unittest.main()
