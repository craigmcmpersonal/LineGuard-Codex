import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.persistance.model import BetLeg
from develop.persistance.model import BetLegOddsHistory
from develop.persistance.model.bet_slip import BetSlip
from develop.persistance.model import Book
from develop.persistance.model.entrant import Entrant
from develop.persistance.model import Event
from develop.persistance.model import Market
from develop.persistance.model import MarketType
from develop.persistance.model import Selection
from develop.persistance.model import Sport
from develop.persistance.repository import Repository
from develop.persistance.postgresql_pool_factory import create_pool_async
from test.persistence.base_repository_test import BaseRepositoryTest


class TestBetLegOddsHistoryRepository(BaseRepositoryTest):
    async def test_bet_leg_odds_history_repository_creates_bet_leg_odds_history_record_async(self):
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
                                            bet_leg: BetLeg = await self._create_bet_leg(
                                                repository,
                                                bet_slip,
                                                selection)
                                            try:
                                                bet_leg_odds_history: BetLegOddsHistory = \
                                                    await repository.bet_leg_odds_history.create(
                                                        bet_leg.key,
                                                        book.key,
                                                        Decimal(2.5),
                                                    )
                                                self.assertIsNotNone(bet_leg_odds_history)
                                                self.assertIsNotNone(bet_leg_odds_history.key)
                                                try:
                                                    serialized: str = bet_leg_odds_history.model_dump_json()
                                                    print(serialized)
                                                finally:
                                                    await repository.bet_leg_odds_history.try_delete(
                                                        bet_leg_odds_history
                                                    )
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

    async def test_bet_leg_odds_history_repository_finds_bet_leg_odds_history_record_async(self):
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
                                            bet_leg: BetLeg = await self._create_bet_leg(
                                                repository,
                                                bet_slip,
                                                selection)
                                            try:
                                                bet_leg_odds_history: BetLegOddsHistory = \
                                                    await repository.bet_leg_odds_history.create(
                                                        bet_leg.key,
                                                        book.key,
                                                        Decimal(2.5),
                                                    )
                                                self.assertIsNotNone(bet_leg_odds_history)
                                                self.assertIsNotNone(bet_leg_odds_history.key)
                                                try:
                                                    retrieved: list[BetLegOddsHistory] = \
                                                        await repository.bet_leg_odds_history.find(bet_leg.key)
                                                    self.assertIsNotNone(retrieved)
                                                    if (count := len(retrieved)) != 1:
                                                        self.fail(count)
                                                    else:
                                                        self.assertIsNotNone(bet_leg.key, retrieved[0].key)
                                                finally:
                                                    await repository.bet_leg_odds_history.try_delete(
                                                        bet_leg_odds_history
                                                    )
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

    async def test_bet_leg_odds_history_repository_gets_bet_leg_odds_history_record_async(self):
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
                                            bet_leg: BetLeg = await self._create_bet_leg(
                                                repository,
                                                bet_slip,
                                                selection)
                                            try:
                                                bet_leg_odds_history: BetLegOddsHistory = \
                                                    await repository.bet_leg_odds_history.create(
                                                        bet_leg.key,
                                                        book.key,
                                                        Decimal(2.5),
                                                    )
                                                self.assertIsNotNone(bet_leg_odds_history)
                                                self.assertIsNotNone(bet_leg_odds_history.key)
                                                try:
                                                    retrieved: BetLegOddsHistory = \
                                                        await repository.bet_leg_odds_history.try_get(
                                                            bet_leg_odds_history.key
                                                        )
                                                    self.assertIsNotNone(retrieved)
                                                    self.assertIsNotNone(bet_leg.key, retrieved.key)
                                                finally:
                                                    await repository.bet_leg_odds_history.try_delete(
                                                        bet_leg_odds_history
                                                    )
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
