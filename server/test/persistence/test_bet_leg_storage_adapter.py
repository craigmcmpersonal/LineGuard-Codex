import datetime
import unittest
from decimal import Decimal

from asyncpg.pool import Pool

from develop.persistence.model.bet_leg import BetLeg
from develop.persistence.model.bet_leg_status import BetLegStatus
from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.book import Book
from develop.persistence.model.entrant import Entrant
from develop.persistence.model.event import Event
from develop.persistence.model.market import Market
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.selection import Selection
from develop.persistence.model.sport import Sport
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestBetLegStorageAdapter(BaseStorageAdapterTest):
    async def test_bet_leg_storage_adapter_creates_bet_leg_record_async(self):
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
                                selection: Selection = await self._create_selection(
                                    storage_adapter,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(storage_adapter)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                        try:
                                            bet_leg: BetLeg = await storage_adapter.bet_leg.create(
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
                                                await storage_adapter.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await storage_adapter.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await storage_adapter.book.try_delete(book)
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

    async def test_bet_leg_storage_adapter_finds_bet_leg_record_by_bet_slip_async(self):
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
                                selection: Selection = await self._create_selection(
                                    storage_adapter,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(storage_adapter)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                        try:
                                            bet_leg: BetLeg = await storage_adapter.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: list[BetLeg] = await storage_adapter.bet_leg.find_by_bet_slip(
                                                    bet_slip.key
                                                )
                                                self.assertIsNotNone(retrieved)
                                                if (count := len(retrieved)) != 1:
                                                    self.fail(count)
                                                else:
                                                    self.assertEqual(bet_leg.key, retrieved[0].key)
                                            finally:
                                                await storage_adapter.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await storage_adapter.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await storage_adapter.book.try_delete(book)
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

    async def test_bet_leg_storage_adapter_finds_bet_leg_record_by_selection_status_async(self):
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
                                selection: Selection = await self._create_selection(
                                    storage_adapter,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(storage_adapter)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                        try:
                                            bet_leg: BetLeg = await storage_adapter.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: list[BetLeg] = \
                                                    await storage_adapter.bet_leg.find_by_selection_status(
                                                        selection.key,
                                                        bet_leg.status
                                                )
                                                self.assertIsNotNone(retrieved)
                                                if (count := len(retrieved)) != 1:
                                                    self.fail(count)
                                                else:
                                                    self.assertEqual(bet_leg.key, retrieved[0].key)
                                            finally:
                                                await storage_adapter.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await storage_adapter.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await storage_adapter.book.try_delete(book)
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

    async def test_bet_leg_storage_adapter_finds_bet_leg_record_by_public_key_async(self):
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
                                selection: Selection = await self._create_selection(
                                    storage_adapter,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(storage_adapter)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                        try:
                                            bet_leg: BetLeg = await storage_adapter.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: BetLeg = await storage_adapter.bet_leg.try_find(
                                                        bet_leg.public_key
                                                )
                                                self.assertIsNotNone(retrieved)
                                                self.assertEqual(bet_leg.key, retrieved.key)
                                            finally:
                                                await storage_adapter.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await storage_adapter.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await storage_adapter.book.try_delete(book)
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

    async def test_bet_leg_storage_adapter_get_bet_leg_record_async(self):
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
                                selection: Selection = await self._create_selection(
                                    storage_adapter,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(storage_adapter)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                        try:
                                            bet_leg: BetLeg = await storage_adapter.bet_leg.create(
                                                bet_slip.key,
                                                selection.key,
                                                Decimal(2.5),
                                                0
                                            )
                                            self.assertIsNotNone(bet_leg)
                                            self.assertIsNotNone(bet_leg.key)
                                            try:
                                                retrieved: BetLeg = await storage_adapter.bet_leg.try_get(bet_leg.key)
                                                self.assertIsNotNone(retrieved)
                                                self.assertEqual(bet_leg.public_key, retrieved.public_key)
                                            finally:
                                                await storage_adapter.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await storage_adapter.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await storage_adapter.book.try_delete(book)
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

    async def test_bet_leg_storage_adapter_updates_bet_leg_record_async(self):
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
                                selection: Selection = await self._create_selection(
                                    storage_adapter,
                                    event,
                                    market,
                                    entrant
                                )
                                try:
                                    book: Book = await self._create_book(storage_adapter)
                                    try:
                                        bet_slip: BetSlip = await self._create_bet_slip(storage_adapter, book)
                                        try:
                                            bet_leg: BetLeg = await storage_adapter.bet_leg.create(
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
                                                updated: BetLeg = await storage_adapter.bet_leg.update(bet_leg)
                                                self.assertIsNotNone(updated)
                                                self.assertEqual(bet_leg.key, updated.key)
                                                self.assertEqual(bet_leg.status, updated.status)
                                                self.assertEqual(bet_leg.settled_time, updated.settled_time)
                                            finally:
                                                await storage_adapter.bet_leg.try_delete(bet_leg)
                                        finally:
                                            await storage_adapter.bet_slip.try_delete(bet_slip)
                                    finally:
                                        await storage_adapter.book.try_delete(book)
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
