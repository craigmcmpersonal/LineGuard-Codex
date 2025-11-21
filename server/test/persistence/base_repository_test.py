import datetime
import unittest
import uuid
from decimal import Decimal

import develop.constants as constants
import test.test_contants as test_constants
from develop.persistance.model import BetLeg
from develop.persistance.model.bet_slip import BetSlip
from develop.persistance.model import BetSlipSource
from develop.persistance.model import BetSlipStatus
from develop.persistance.model import Book
from develop.persistance.model.entrant import Entrant
from develop.persistance.model import Event
from develop.persistance.model import HedgeOpportunity
from develop.persistance.model.hedge_rule import HedgeRule
from develop.persistance.model import Market
from develop.persistance.model import MarketType
from develop.persistance.model import Selection
from develop.persistance.model import Sport
from develop.persistance.model import SportType
from develop.persistance.model import UserHedgeProfile
from develop.persistance.repository import Repository
from develop.utility import compose_unique_identifier


class BaseRepositoryTest(unittest.IsolatedAsyncioTestCase):
    async def _create_bet_leg(self, repository: Repository, bet_slip: BetSlip, selection: Selection) -> BetLeg:
        result: BetLeg = await repository.bet_leg.create(
            bet_slip.key,
            selection.key,
            Decimal(2.5),
            0
        )
        return result

    async def _create_bet_slip(
            self,
            repository: Repository,
            book: Book,
            user_key: uuid.UUID|None = uuid.uuid4()
    ) -> BetSlip:
        text: str = compose_unique_identifier()
        external_identifier: str = compose_unique_identifier()
        original: bytes = text.encode(constants.ENCODING_UTF8)
        result: BetSlip = await repository.bet_slip.create(
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

    async def _create_book(self, repository: Repository):
        name: str = compose_unique_identifier()
        result: Book = await repository.book.create(name)
        return result

    async def _create_entrant(self, repository: Repository, event: Event) -> Entrant:
        name: str = compose_unique_identifier()
        result: Entrant = await repository.entrant.create(name, event.key)
        return result

    async def _create_event(self, repository: Repository, sport: Sport) -> Event:
        event_name: str = compose_unique_identifier()
        start_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        result: Event = await repository.event.create(sport.key, event_name, start_time)
        return result

    async def _create_hedge_opportunity(self, repository, hedge_rule: HedgeRule, bet_slip: BetSlip) -> HedgeOpportunity:
        result: HedgeOpportunity = await repository.hedge_opportunity.create(
            bet_slip.key,
            hedge_rule.key
        )
        return result

    async def _create_hedge_rule(self, repository: Repository, user_hedge_profile: UserHedgeProfile) -> HedgeRule:
        rule_name: str = compose_unique_identifier()
        original: str = compose_unique_identifier()
        result: HedgeRule = await repository.hedge_rule.create(
            user_hedge_profile.key,
            rule_name,
            original
        )
        return result

    async def _create_market(self, repository: Repository, event: Event, market_type: MarketType) -> Market:
        result: Market = await repository.market.create(
            event.key,
            market_type.key,
            parameters=test_constants.MARKET_PARAMETERS
        )
        return result

    async def _create_market_type(self, repository: Repository) -> MarketType:
        name: str = compose_unique_identifier()
        result: MarketType = await repository.market_type.create(name)
        return result

    async def _create_selection(
            self,
            repository: Repository,
            event: Event,
            market: Market,
            entrant: Entrant
    ) -> Selection:
        result: Selection = await repository.selection.create(
            event.key,
            market.key,
            entrant.key
        )
        return result

    async def _create_sport(self, repository: Repository) -> Sport:
        sport_name: str = compose_unique_identifier()
        result: Sport = await repository.sport.create(sport_name, active=True, sport_type=SportType.GAME)
        return result

    async def _create_user_hedge_profile(
            self,
            repository: Repository,
            user_key: uuid.UUID|None = uuid.uuid4()
    ) -> UserHedgeProfile:
        result: UserHedgeProfile = await repository.user_hedge_profile.create(user_key)
        return result
