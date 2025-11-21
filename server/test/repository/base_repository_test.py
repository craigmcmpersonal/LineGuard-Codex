import datetime
import unittest
import uuid

import develop.constants as constants
import test.test_contants as test_constants
from develop.model.bet_slip import BetSlip
from develop.model.bet_slip_source import BetSlipSource
from develop.model.bet_slip_status import BetSlipStatus
from develop.model.book import Book
from develop.model.entrant import Entrant
from develop.model.event import Event
from develop.model.market import Market
from develop.model.market_type import MarketType
from develop.model.selection import Selection
from develop.model.sport import Sport
from develop.model.sport_type import SportType
from develop.model.user_hedge_profile import UserHedgeProfile
from develop.repository.repository import Repository
from develop.utility import compose_unique_identifier


class BaseRepositoryTest(unittest.IsolatedAsyncioTestCase):
    async def _create_bet_slip(self, repository: Repository, book: Book) -> BetSlip:
        user_key: uuid.UUID = uuid.uuid4()
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

    async def _create_user_hedge_profile(self, repository: Repository) -> UserHedgeProfile:
        user_key: uuid.UUID = uuid.uuid4()
        result: UserHedgeProfile = await repository.user_hedge_profile.create(user_key)
        return result
