import datetime
import unittest
from typing import Any

from asyncpg.pool import Pool
import json

from develop.persistence.model.event import Event
from develop.persistence.model.market import Market
from develop.persistence.model.market_status import MarketStatus
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.sport import Sport
from develop.persistence.model.sport_type import SportType
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
import test.test_contants as test_constants


class TestMarketStorageAdapter(unittest.IsolatedAsyncioTestCase):

    async def test_market_storage_adapter_creates_market_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await storage_adapter.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await storage_adapter.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            self.assertEqual(event.key, market.event_key)
                            self.assertEqual(market_type.key, market.market_type_key)
                            self.assertIsNotNone(market.parameters)
                            _: Any = json.loads(market.parameters)
                            initial_market: str = market.model_dump_json()
                            print(initial_market)
                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.market_type.try_delete(market_type)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_market_storage_adapter_finds_market_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await storage_adapter.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await storage_adapter.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            self.assertEqual(event.key, market.event_key)
                            self.assertEqual(market_type.key, market.market_type_key)
                            self.assertIsNotNone(market.parameters)
                            retrieved: list[Market] = await storage_adapter.market.find(event.key, market_type.key)
                            self.assertIsNotNone(retrieved)
                            if (count := len(retrieved)) != 1:
                                count: int
                                self.fail(count)
                            else:
                                self.assertEqual(market.key, retrieved[0].key)

                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.market_type.try_delete(market_type)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_entrant_storage_adapter_gets_entrant_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await storage_adapter.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await storage_adapter.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            self.assertEqual(event.key, market.event_key)
                            self.assertEqual(market_type.key, market.market_type_key)
                            self.assertIsNotNone(market.parameters)
                            retrieved: Market = await storage_adapter.market.try_get(market.key)
                            self.assertIsNotNone(retrieved)
                            self.assertEqual(market.key, retrieved.key)

                        finally:
                            await storage_adapter.market.try_delete(market)
                    finally:
                        await storage_adapter.market_type.try_delete(market_type)
                finally:
                    await storage_adapter.event.try_delete(event)
            finally:
                await storage_adapter.sport.try_delete(sport)

    async def test_market_storage_adapter_updates_market_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            storage_adapter: StorageAdapter = StorageAdapter(connection)
            sport: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await storage_adapter.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await storage_adapter.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            market.status = MarketStatus.SUSPENDED
                            updated_status: Market = await storage_adapter.market.update(market)
                            self.assertIsNotNone(updated_status)
                            self.assertEqual(market.status, updated_status.status)
                            market.parameters = None
                            updated_parameters: Market = await storage_adapter.market.update(market)
                            self.assertIsNotNone(updated_parameters)
                            self.assertIsNone(updated_parameters.parameters)
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
