import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.persistance.model.entrant import Entrant
from develop.persistance.model import Event
from develop.persistance.model import Market
from develop.persistance.model import MarketType
from develop.persistance.model import RaceResult
from develop.persistance.model import Sport
from develop.persistance.repository import Repository
from develop.persistance.postgresql_pool_factory import create_pool_async
from test.persistence.base_repository_test import BaseRepositoryTest


class TestRaceResultRepository(BaseRepositoryTest):
    async def test_race_result_repository_creates_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                event: Event = await self._create_event(repository, sport)
                try:
                    market_type: MarketType = await self._create_market_type(repository)
                    try:
                        market: Market = await self._create_market(repository, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(repository, event)
                            try:
                                value: int = 3
                                decimal_value: Decimal = Decimal(value)
                                race_result: RaceResult = await repository.race_result.create(
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
                                    await repository.race_result.try_delete(race_result)
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

    async def test_race_result_repository_finds_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                event: Event = await self._create_event(repository, sport)
                try:
                    market_type: MarketType = await self._create_market_type(repository)
                    try:
                        market: Market = await self._create_market(repository, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(repository, event)
                            try:
                                value: int = 3
                                race_result: RaceResult = await repository.race_result.create(
                                    event.key,
                                    entrant.key,
                                    value
                                )
                                try:
                                    retrieved: list[RaceResult] = await repository.race_result.find(event.key)
                                    self.assertIsNotNone(retrieved)
                                    if (count := len(retrieved)) != 1:
                                        self.fail(count)
                                    else:
                                        self.assertEqual(race_result.key, retrieved[0].key)
                                finally:
                                    await repository.race_result.try_delete(race_result)
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

    async def test_race_result_repository_gets_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                event: Event = await self._create_event(repository, sport)
                try:
                    market_type: MarketType = await self._create_market_type(repository)
                    try:
                        market: Market = await self._create_market(repository, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(repository, event)
                            try:
                                value: int = 3
                                race_result: RaceResult = await repository.race_result.create(
                                    event.key,
                                    entrant.key,
                                    value
                                )
                                try:
                                    retrieved: RaceResult = await repository.race_result.try_get(race_result.key)
                                    self.assertIsNotNone(retrieved)
                                    self.assertEqual(race_result.key, retrieved.key)
                                finally:
                                    await repository.race_result.try_delete(race_result)
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

    async def test_race_result_repository_updates_race_result_record_async(self):
        pool: Pool = await create_pool_async()
        async with pool.acquire() as connection:
            repository: Repository = Repository(connection)
            sport: Sport = await self._create_sport(repository)
            try:
                event: Event = await self._create_event(repository, sport)
                try:
                    market_type: MarketType = await self._create_market_type(repository)
                    try:
                        market: Market = await self._create_market(repository, event, market_type)
                        try:
                            entrant: Entrant = await self._create_entrant(repository, event)
                            try:
                                value: int = 3
                                race_result: RaceResult = await repository.race_result.create(
                                    event.key,
                                    entrant.key,
                                    value
                                )
                                try:
                                    race_result.position = race_result.position + 1
                                    race_result.win_payout = Decimal(value)
                                    race_result.place_payout = Decimal(race_result.position)
                                    self.assertNotEqual(race_result.win_payout, race_result.place_payout)
                                    updated: RaceResult = await repository.race_result.update(race_result)
                                    self.assertIsNotNone(updated)
                                    self.assertEqual(race_result.position, updated.position)
                                    self.assertEqual(race_result.win_payout, updated.win_payout)
                                    self.assertEqual(race_result.place_payout, updated.place_payout)
                                finally:
                                    await repository.race_result.try_delete(race_result)
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
