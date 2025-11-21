import datetime
import unittest

from asyncpg.pool import Pool

from develop.persistance.model.entrant import Entrant
from develop.persistance.model import Event
from develop.persistance.model import Market
from develop.persistance.model import MarketType
from develop.persistance.model.outcome import Outcome
from develop.persistance.model import Selection
from develop.persistance.model import SelectionStatus
from develop.persistance.model import Sport
from develop.persistance.model import SportType
from develop.persistance.repository import Repository
from develop.persistance.postgresql_pool_factory import create_pool_async
from develop.utility import compose_unique_identifier
import test.test_contants as test_constants


class TestSelectionRepository(unittest.IsolatedAsyncioTestCase):
    async def test_market_repository_creates_market_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await repository.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await repository.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await repository.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await repository.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await repository.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await repository.selection.create(
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
                                    await repository.selection.try_delete(selection)
                            finally:
                                await repository.entrant.try_delete(entrant)
                        finally:
                            await repository.market.try_delete(market)
                    finally:
                        await repository.market_type.try_delete(market_type)
                finally:
                    await repository.event.try_delete(event)
            finally:
                await repository.sport.try_delete(sport)

    async def test_selection_repository_finds_selection_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await repository.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await repository.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await repository.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await repository.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await repository.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await repository.selection.create(
                                    event.key,
                                    market.key,
                                    entrant.key
                                )
                                self.assertIsNotNone(selection)
                                self.assertIsNotNone(selection.key)
                                try:
                                    retrieved: list[Selection] = await repository.selection.find(
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
                                    await repository.selection.try_delete(selection)
                            finally:
                                await repository.entrant.try_delete(entrant)
                        finally:
                            await repository.market.try_delete(market)
                    finally:
                        await repository.market_type.try_delete(market_type)
                finally:
                    await repository.event.try_delete(event)
            finally:
                await repository.sport.try_delete(sport)

    async def test_selection_repository_gets_selection_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await repository.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await repository.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await repository.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await repository.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await repository.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await repository.selection.create(
                                    event.key,
                                    market.key,
                                    entrant.key
                                )
                                self.assertIsNotNone(selection)
                                self.assertIsNotNone(selection.key)
                                try:
                                    retrieved: Selection = await repository.selection.try_get(selection.key)
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(selection.key, retrieved.key)
                                finally:
                                    await repository.selection.try_delete(selection)
                            finally:
                                await repository.entrant.try_delete(entrant)
                        finally:
                            await repository.market.try_delete(market)
                    finally:
                        await repository.market_type.try_delete(market_type)
                finally:
                    await repository.event.try_delete(event)
            finally:
                await repository.sport.try_delete(sport)

    async def test_market_repository_updates_market_record_async(self):
        sport_name: str = compose_unique_identifier()
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await repository.sport.create(sport_name, active=True, sport_type=SportType.GAME)
            self.assertIsNotNone(sport)
            self.assertIsNotNone(sport.key)
            try:
                event_name: str = compose_unique_identifier()
                start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
                event: Event = await repository.event.create(sport.key, event_name, start_time)
                self.assertIsNotNone(event)
                self.assertIsNotNone(event.key)
                try:
                    market_type_name: str = compose_unique_identifier()
                    market_type: MarketType = await repository.market_type.create(market_type_name)
                    self.assertIsNotNone(market_type)
                    self.assertIsNotNone(market_type.key)
                    try:
                        market: Market = await repository.market.create(
                            event.key,
                            market_type.key,
                            parameters=test_constants.MARKET_PARAMETERS
                        )
                        self.assertIsNotNone(market)
                        self.assertIsNotNone(market.key)
                        try:
                            entrant_name: str = compose_unique_identifier()
                            entrant: Entrant = await repository.entrant.create(entrant_name, event.key)
                            self.assertIsNotNone(entrant)
                            self.assertIsNotNone(entrant.key)
                            try:
                                selection: Selection = await repository.selection.create(
                                    event.key,
                                    market.key,
                                    entrant.key
                                )
                                self.assertIsNotNone(selection)
                                self.assertIsNotNone(selection.key)
                                try:
                                    selection.status = SelectionStatus.SUSPENDED
                                    selection.outcome = Outcome.WON
                                    updated: Selection = await repository.selection.update(selection)
                                    self.assertIsNotNone(updated)
                                    self.assertEqual(selection.status, updated.status)
                                    self.assertEqual(selection.outcome, updated.outcome)
                                finally:
                                    await repository.selection.try_delete(selection)
                            finally:
                                await repository.entrant.try_delete(entrant)
                        finally:
                            await repository.market.try_delete(market)
                    finally:
                        await repository.market_type.try_delete(market_type)
                finally:
                    await repository.event.try_delete(event)
            finally:
                await repository.sport.try_delete(sport)


if __name__ == '__main__':
    unittest.main()
