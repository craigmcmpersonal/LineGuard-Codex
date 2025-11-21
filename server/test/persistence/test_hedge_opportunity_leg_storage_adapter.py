import unittest

from asyncpg.pool import Pool

from develop.persistence.model.bet_leg import BetLeg
from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.book import Book
from develop.persistence.model.entrant import Entrant
from develop.persistence.model.event import Event
from develop.persistence.model.hedge_opportunity import HedgeOpportunity
from develop.persistence.model.hedge_opportunity_leg import HedgeOpportunityLeg
from develop.persistence.model.hedge_rule import HedgeRule
from develop.persistence.model.market import Market
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.selection import Selection
from develop.persistence.model.sport import Sport
from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.storage_adapter import StorageAdapter
from develop.persistence.postgresql_pool_factory import create_pool_async
from test.persistence.base_storage_adapter_test import BaseStorageAdapterTest


class TestHedgeOpportunityBetLegStorageAdapter(BaseStorageAdapterTest):
    async def test_hedge_opportunity_leg_storage_adapter_creates_hedge_opportunity_leg_record_async(self):
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
                                            bet_leg: BetLeg = await self._create_bet_leg(
                                                storage_adapter,
                                                bet_slip,
                                                selection)
                                            try:
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        storage_adapter,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        storage_adapter,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                storage_adapter,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await storage_adapter.hedge_opportunity_leg.create(
                                                                    hedge_opportunity.key,
                                                                    bet_leg.key
                                                                )
                                                            self.assertIsNotNone(hedge_opportunity_leg)
                                                            self.assertIsNotNone(hedge_opportunity_leg.key)
                                                            try:
                                                                serialized: str = \
                                                                    hedge_opportunity_leg.model_dump_json()
                                                                print(serialized)
                                                            finally:
                                                                await storage_adapter.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await storage_adapter.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await storage_adapter.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
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

    async def test_hedge_opportunity_leg_storage_adapter_finds_hedge_opportunity_leg_record_by_hedge_opportunity_async(self):
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
                                            bet_leg: BetLeg = await self._create_bet_leg(
                                                storage_adapter,
                                                bet_slip,
                                                selection)
                                            try:
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        storage_adapter,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        storage_adapter,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                storage_adapter,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await storage_adapter.hedge_opportunity_leg.create(
                                                                    hedge_opportunity.key,
                                                                    bet_leg.key
                                                                )
                                                            self.assertIsNotNone(hedge_opportunity_leg)
                                                            self.assertIsNotNone(hedge_opportunity_leg.key)
                                                            try:
                                                                retrieved: list[HedgeOpportunityLeg] = \
                                                                    await \
                                                                        storage_adapter.hedge_opportunity_leg.find_by_hedge_opportunity(
                                                                            hedge_opportunity.key
                                                                        )
                                                                self.assertIsNotNone(retrieved)
                                                                if (count := len(retrieved)) != 1:
                                                                    self.fail(count)
                                                                else:
                                                                    self.assertEqual(
                                                                        hedge_opportunity_leg.key,
                                                                        retrieved[0].key
                                                                    )
                                                            finally:
                                                                await storage_adapter.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await storage_adapter.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await storage_adapter.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
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

    async def test_hedge_opportunity_leg_storage_adapter_finds_hedge_opportunity_leg_record_by_bet_leg_async(self):
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
                                            bet_leg: BetLeg = await self._create_bet_leg(
                                                storage_adapter,
                                                bet_slip,
                                                selection)
                                            try:
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        storage_adapter,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        storage_adapter,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                storage_adapter,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await storage_adapter.hedge_opportunity_leg.create(
                                                                    hedge_opportunity.key,
                                                                    bet_leg.key
                                                                )
                                                            self.assertIsNotNone(hedge_opportunity_leg)
                                                            self.assertIsNotNone(hedge_opportunity_leg.key)
                                                            try:
                                                                retrieved: list[HedgeOpportunityLeg] = \
                                                                    await \
                                                                        storage_adapter.hedge_opportunity_leg.find_by_bet_leg(
                                                                            bet_leg.key
                                                                        )
                                                                self.assertIsNotNone(retrieved)
                                                                if (count := len(retrieved)) != 1:
                                                                    self.fail(count)
                                                                else:
                                                                    self.assertEqual(
                                                                        hedge_opportunity_leg.key,
                                                                        retrieved[0].key
                                                                    )
                                                            finally:
                                                                await storage_adapter.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await storage_adapter.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await storage_adapter.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
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

    async def test_hedge_opportunity_leg_storage_adapter_gets_hedge_opportunity_leg_record_async(self):
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
                                            bet_leg: BetLeg = await self._create_bet_leg(
                                                storage_adapter,
                                                bet_slip,
                                                selection)
                                            try:
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        storage_adapter,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        storage_adapter,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                storage_adapter,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await storage_adapter.hedge_opportunity_leg.create(
                                                                    hedge_opportunity.key,
                                                                    bet_leg.key
                                                                )
                                                            self.assertIsNotNone(hedge_opportunity_leg)
                                                            self.assertIsNotNone(hedge_opportunity_leg.key)
                                                            try:
                                                                retrieved: HedgeOpportunityLeg = \
                                                                    await \
                                                                        storage_adapter.hedge_opportunity_leg.try_get(
                                                                            hedge_opportunity_leg.key
                                                                        )
                                                                self.assertIsNotNone(retrieved)
                                                                self.assertEqual(
                                                                    hedge_opportunity_leg.key,
                                                                    retrieved.key
                                                                )
                                                            finally:
                                                                await storage_adapter.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await storage_adapter.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await storage_adapter.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await storage_adapter.user_hedge_profile.try_delete(user_hedge_profile)
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
