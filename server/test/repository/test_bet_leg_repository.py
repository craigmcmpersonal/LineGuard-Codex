import datetime
import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.model.bet_leg import BetLeg
from develop.model.bet_leg_status import BetLegStatus
from develop.model.bet_slip import BetSlip
from develop.model.book import Book
from develop.model.entrant import Entrant
from develop.model.event import Event
from develop.model.market import Market
from develop.model.market_type import MarketType
from develop.model.selection import Selection
from develop.model.sport import Sport
from develop.repository.repository import Repository
from develop.repository.postgresql_pool_factory import create_pool_async
from test.repository.base_repository_test import BaseRepositoryTest


class TestBetLegRepository(BaseRepositoryTest):
    async def test_bet_leg_repository_creates_bet_leg_record_async(self):
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
                                selection: Selection = await self._create_selection(
                                    repository,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(repository)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                        try:
                                            bet_leg: BetLeg = await repository.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                serialized: str = bet_leg.model_dump_json()
                                                print(serialized)
                                            finally:
                                                await repository.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await repository.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await repository.book.try_delete(book)
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

    async def test_bet_leg_repository_finds_bet_leg_record_by_bet_slip_async(self):
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
                                selection: Selection = await self._create_selection(
                                    repository,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(repository)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                        try:
                                            bet_leg: BetLeg = await repository.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: list[BetLeg] = await repository.bet_leg.find_by_bet_slip(
                                                    bet_slip.key
                                                )
                                                self.assertIsNotNone(retrieved)
                                                if (count := len(retrieved)) != 1:
                                                    self.fail(count)
                                                else:
                                                    self.assertEqual(bet_leg.key, retrieved[0].key)
                                            finally:
                                                await repository.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await repository.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await repository.book.try_delete(book)
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

    async def test_bet_leg_repository_finds_bet_leg_record_by_selection_status_async(self):
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
                                selection: Selection = await self._create_selection(
                                    repository,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(repository)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                        try:
                                            bet_leg: BetLeg = await repository.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: list[BetLeg] = \
                                                    await repository.bet_leg.find_by_selection_status(
                                                        selection.key,
                                                        bet_leg.status
                                                )
                                                self.assertIsNotNone(retrieved)
                                                if (count := len(retrieved)) != 1:
                                                    self.fail(count)
                                                else:
                                                    self.assertEqual(bet_leg.key, retrieved[0].key)
                                            finally:
                                                await repository.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await repository.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await repository.book.try_delete(book)
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

    async def test_bet_leg_repository_finds_bet_leg_record_by_public_key_async(self):
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
                                selection: Selection = await self._create_selection(
                                    repository,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(repository)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                        try:
                                            bet_leg: BetLeg = await repository.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: BetLeg = await repository.bet_leg.try_find(
                                                        bet_leg.public_key
                                                )
                                                self.assertIsNotNone(retrieved)
                                                self.assertEqual(bet_leg.key, retrieved.key)
                                            finally:
                                                await repository.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await repository.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await repository.book.try_delete(book)
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

    async def test_bet_leg_repository_get_bet_leg_record_async(self):
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
                                selection: Selection = await self._create_selection(
                                    repository,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(repository)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                        try:
                                            bet_leg: BetLeg = await repository.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: BetLeg = await repository.bet_leg.try_get(bet_leg.key)
                                                self.assertIsNotNone(retrieved)
                                                self.assertEqual(bet_leg.public_key, retrieved.public_key)
                                            finally:
                                                await repository.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await repository.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await repository.book.try_delete(book)
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

    async def test_bet_leg_repository_updates_bet_leg_record_async(self):
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
                                selection: Selection = await self._create_selection(
                                    repository,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(repository)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(repository, book)
                                        try:
                                            bet_leg: BetLeg = await repository.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                bet_leg.status = BetLegStatus.WON
                                                bet_leg.settled_time = datetime.datetime.now(datetime.timezone.utc)
                                                updated: BetLeg = await repository.bet_leg.update(bet_leg)
                                                self.assertIsNotNone(updated)
                                                self.assertEqual(bet_leg.key, updated.key)
                                                self.assertEqual(bet_leg.status, updated.status)
                                                self.assertEqual(bet_leg.settled_time, updated.settled_time)
                                            finally:
                                                await repository.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await repository.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await repository.book.try_delete(book)
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
