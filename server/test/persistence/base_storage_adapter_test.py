import datetime
import unittest
import uuid
from decimal import Decimal

import develop.constants as constants
import test.test_contants as test_constants
from develop.persistence.model.bet_leg import BetLeg
from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.model.bet_slip_source import BetSlipSource
from develop.persistence.model.bet_slip_status import BetSlipStatus
from develop.persistence.model.book import Book
from develop.persistence.model.entrant import Entrant
from develop.persistence.model.event import Event
from develop.persistence.model.hedge_opportunity import HedgeOpportunity
from develop.persistence.model.hedge_rule import HedgeRule
from develop.persistence.model.market import Market
from develop.persistence.model.market_type import MarketType
from develop.persistence.model.selection import Selection
from develop.persistence.model.sport import Sport
from develop.persistence.model.sport_type import SportType
from develop.persistence.model.user_hedge_profile import UserHedgeProfile
from develop.persistence.storage_adapter import StorageAdapter
from develop.utility import compose_unique_identifier


class BaseStorageAdapterTest(unittest.IsolatedAsyncioTestCase):
    async def _create_bet_leg(self, storage_adapter: StorageAdapter, bet_slip: BetSlip, selection: Selection) -> BetLeg:
        result: BetLeg = await storage_adapter.bet_leg.create(
            bet_slip.key,
            selection.key,
            Decimal(2.5),
            0
        )
        return result

    async def _create_bet_slip(
            self,
            storage_adapter: StorageAdapter,
            book: Book,
            user_key: uuid.UUID|None = uuid.uuid4()
    ) -> BetSlip:
        text: str = compose_unique_identifier()
        external_identifier: str = compose_unique_identifier()
        original: bytes = text.encode(constants.ENCODING_UTF8)
        result: BetSlip = await storage_adapter.bet_slip.create(
            user_key,
            book.key,
            0,
            0,
            BetSlipStatus.PLACED,
            original,
            BetSlipSource.SYNC,
            external_identifier=external_identifier
        )
        return result

    async def _create_book(self, storage_adapter: StorageAdapter):
        name: str = compose_unique_identifier()
        result: Book = await storage_adapter.book.create(name)
        return result

    async def _create_entrant(self, storage_adapter: StorageAdapter, event: Event) -> Entrant:
        name: str = compose_unique_identifier()
        result: Entrant = await storage_adapter.entrant.create(name, event.key)
        return result

    async def _create_event(self, storage_adapter: StorageAdapter, sport: Sport) -> Event:
        event_name: str = compose_unique_identifier()
        start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        result: Event = await storage_adapter.event.create(sport.key, event_name, start_time)
        return result

    async def _create_hedge_opportunity(
            self,
            storage_adapter,
            hedge_rule: HedgeRule,
            bet_slip: BetSlip
    ) -> HedgeOpportunity:
        result: HedgeOpportunity = await storage_adapter.hedge_opportunity.create(
            bet_slip.key,
            hedge_rule.key
        )
        return result

    async def _create_hedge_rule(
            self,
            storage_adapter: StorageAdapter,
            user_hedge_profile: UserHedgeProfile
    ) -> HedgeRule:
        rule_name: str = compose_unique_identifier()
        original: str = compose_unique_identifier()
        result: HedgeRule = await storage_adapter.hedge_rule.create(
            user_hedge_profile.key,
            rule_name,
            original
        )
        return result

    async def _create_market(self, storage_adapter: StorageAdapter, event: Event, market_type: MarketType) -> Market:
        result: Market = await storage_adapter.market.create(
            event.key,
            market_type.key,
            parameters=test_constants.MARKET_PARAMETERS
        )
        return result

    async def _create_market_type(self, storage_adapter: StorageAdapter) -> MarketType:
        name: str = compose_unique_identifier()
        result: MarketType = await storage_adapter.market_type.create(name)
        return result

    async def _create_selection(
            self,
            storage_adapter: StorageAdapter,
            event: Event,
            market: Market,
            entrant: Entrant
    ) -> Selection:
        result: Selection = await storage_adapter.selection.create(
            event.key,
            market.key,
            entrant.key
        )
        return result

    async def _create_sport(self, storage_adapter: StorageAdapter) -> Sport:
        sport_name: str = compose_unique_identifier()
        result: Sport = await storage_adapter.sport.create(sport_name, active=True, sport_type=SportType.GAME)
        return result

    async def _create_user_hedge_profile(
            self,
            storage_adapter: StorageAdapter,
            user_key: uuid.UUID|None = uuid.uuid4()
    ) -> UserHedgeProfile:
        result: UserHedgeProfile = await storage_adapter.user_hedge_profile.create(user_key)
        return result
