import datetime
import unittest

from asyncpg.pool import Pool

from develop.persistence.model.entrant import Entrant
from develop.persistence.model.event import Event
from develop.persistence.model.market import Market
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.outcome import Outcome
from develop.persistence.model.selection import Selection
from develop.persistence.model.selection_status import SelectionStatus
from develop.persistence.model.sport import Sport
from develop.persistence.model.sport_type import SportType
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
import test.test_contants as test_constants


class TestSelectionStorageAdapter(unittest.IsolatedAsyncioTestCase):
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
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await storage_adapter.selection.create(
                                    event.key,
                                    market.key,
                                    entrant.key
                                )
                                self.assertIsNotNone(selection)
                                self.assertIsNotNone(selection.key)
                                try:
                                    self.assertEqual(event.key, selection.event_key)
                                    self.assertEqual(market.key, selection.market_key)
                                    self.assertEqual(entrant.key, selection.entrant_key)
                                    serialized: str = selection.model_dump_json()
                                    print(serialized)
                                finally:
                                    await storage_adapter.selection.try_delete(selection)
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

    async def test_selection_storage_adapter_finds_selection_record_async(self):
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
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await storage_adapter.selection.create(
                                    event.key,
                                    market.key,
                                    entrant.key
                                )
                                self.assertIsNotNone(selection)
                                self.assertIsNotNone(selection.key)
                                try:
                                    retrieved: list[Selection] = await storage_adapter.selection.find(
                                        event.key,
                                        market.key,
                                        entrant.key
                                    )
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(selection.key, retrieved[0].key)
                                finally:
                                    await storage_adapter.selection.try_delete(selection)
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

    async def test_selection_storage_adapter_gets_selection_record_async(self):
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
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await storage_adapter.selection.create(
                                    event.key,
                                    market.key,
                                    entrant.key
                                )
                                self.assertIsNotNone(selection)
                                self.assertIsNotNone(selection.key)
                                try:
                                    retrieved: Selection = await storage_adapter.selection.try_get(selection.key)
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(selection.key, retrieved.key)
                                finally:
                                    await storage_adapter.selection.try_delete(selection)
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
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await storage_adapter.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await storage_adapter.selection.create(
                                    event.key,
                                    market.key,
                                    entrant.key
                                )
                                self.assertIsNotNone(selection)
                                self.assertIsNotNone(selection.key)
                                try:
                                    selection.status = SelectionStatus.SUSPENDED
                                    selection.outcome = Outcome.WON
                                    updated: Selection = await storage_adapter.selection.update(selection)
                                    self.assertIsNotNone(updated)
                                    self.assertEqual(selection.status, updated.status)
                                    self.assertEqual(selection.outcome, updated.outcome)
                                finally:
                                    await storage_adapter.selection.try_delete(selection)
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
