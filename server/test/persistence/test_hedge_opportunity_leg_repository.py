import unittest

from asyncpg.pool import Pool

from develop.persistance.model import BetLeg
from develop.persistance.model.bet_slip import BetSlip
from develop.persistance.model import Book
from develop.persistance.model.entrant import Entrant
from develop.persistance.model import Event
from develop.persistance.model import HedgeOpportunity
from develop.persistance.model import HedgeOpportunityLeg
from develop.persistance.model.hedge_rule import HedgeRule
from develop.persistance.model import Market
from develop.persistance.model import MarketType
from develop.persistance.model import Selection
from develop.persistance.model import Sport
from develop.persistance.model import UserHedgeProfile
from develop.persistance.repository import Repository
from develop.persistance.postgresql_pool_factory import create_pool_async
from test.persistence.base_repository_test import BaseRepositoryTest


class TestHedgeOpportunityBetLegRepository(BaseRepositoryTest):
    async def test_hedge_opportunity_leg_repository_creates_hedge_opportunity_leg_record_async(self):
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
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        repository,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        repository,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                repository,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await repository.hedge_opportunity_leg.create(
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
                                                                await repository.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await repository.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await repository.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await repository.user_hedge_profile.try_delete(user_hedge_profile)
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

    async def test_hedge_opportunity_leg_repository_finds_hedge_opportunity_leg_record_by_hedge_opportunity_async(self):
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
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        repository,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        repository,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                repository,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await repository.hedge_opportunity_leg.create(
                                                                    hedge_opportunity.key,
                                                                    bet_leg.key
                                                                )
                                                            self.assertIsNotNone(hedge_opportunity_leg)
                                                            self.assertIsNotNone(hedge_opportunity_leg.key)
                                                            try:
                                                                retrieved: list[HedgeOpportunityLeg] = \
                                                                    await \
                                                                        repository.hedge_opportunity_leg.find_by_hedge_opportunity(
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
                                                                await repository.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await repository.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await repository.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await repository.user_hedge_profile.try_delete(user_hedge_profile)
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

    async def test_hedge_opportunity_leg_repository_finds_hedge_opportunity_leg_record_by_bet_leg_async(self):
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
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        repository,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        repository,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                repository,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await repository.hedge_opportunity_leg.create(
                                                                    hedge_opportunity.key,
                                                                    bet_leg.key
                                                                )
                                                            self.assertIsNotNone(hedge_opportunity_leg)
                                                            self.assertIsNotNone(hedge_opportunity_leg.key)
                                                            try:
                                                                retrieved: list[HedgeOpportunityLeg] = \
                                                                    await \
                                                                        repository.hedge_opportunity_leg.find_by_bet_leg(
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
                                                                await repository.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await repository.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await repository.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await repository.user_hedge_profile.try_delete(user_hedge_profile)
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

    async def test_hedge_opportunity_leg_repository_gets_hedge_opportunity_leg_record_async(self):
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
                                                user_hedge_profile: UserHedgeProfile = \
                                                    await self._create_user_hedge_profile(
                                                        repository,
                                                        user_key=bet_slip.user_key
                                                    )
                                                try:
                                                    hedge_rule: HedgeRule = await self._create_hedge_rule(
                                                        repository,
                                                        user_hedge_profile
                                                    )
                                                    try:
                                                        hedge_opportunity: HedgeOpportunity = \
                                                            await self._create_hedge_opportunity(
                                                                repository,
                                                                hedge_rule,
                                                                bet_slip
                                                            )
                                                        try:
                                                            hedge_opportunity_leg: HedgeOpportunityLeg = \
                                                                await repository.hedge_opportunity_leg.create(
                                                                    hedge_opportunity.key,
                                                                    bet_leg.key
                                                                )
                                                            self.assertIsNotNone(hedge_opportunity_leg)
                                                            self.assertIsNotNone(hedge_opportunity_leg.key)
                                                            try:
                                                                retrieved: HedgeOpportunityLeg = \
                                                                    await \
                                                                        repository.hedge_opportunity_leg.try_get(
                                                                            hedge_opportunity_leg.key
                                                                        )
                                                                self.assertIsNotNone(retrieved)
                                                                self.assertEqual(
                                                                    hedge_opportunity_leg.key,
                                                                    retrieved.key
                                                                )
                                                            finally:
                                                                await repository.hedge_opportunity_leg.try_delete(
                                                                    hedge_opportunity_leg
                                                                )
                                                        finally:
                                                            await repository.hedge_opportunity.try_delete(
                                                                hedge_opportunity
                                                            )
                                                    finally:
                                                        await repository.hedge_rule.try_delete(hedge_rule)
                                                finally:
                                                    await repository.user_hedge_profile.try_delete(user_hedge_profile)
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
