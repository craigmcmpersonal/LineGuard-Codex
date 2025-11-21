from typing import Any

from develop.repository.bet_leg_odds_history_repository import BetLegOddsHistoryRepository
from develop.repository.bet_leg_repository import BetLegRepository
from develop.repository.bet_slip_repository import BetSlipRepository
from develop.repository.book_repository import BookRepository
from develop.repository.entrant_repository import EntrantRepository
from develop.repository.event_repository import EventRepository
from develop.repository.hedge_rule_repository import HedgeRuleRepository
from develop.repository.market_repository import MarketRepository
from develop.repository.market_type_repository import MarketTypeRepository
from develop.repository.selection_repository import SelectionRepository
from develop.repository.sport_repository import SportRepository
from develop.repository.user_hedge_profile_repository import UserHedgeProfileRepository


class Repository:
    def __init__(self, connection: Any):
        if not connection:
            raise ValueError()
        else:
            self.connection = connection
            self.bet_leg = BetLegRepository(connection)
            self.bet_leg_odds_history = BetLegOddsHistoryRepository(connection)
            self.bet_slip = BetSlipRepository(connection)
            self.book = BookRepository(connection)
            self.entrant = EntrantRepository(connection)
            self.event = EventRepository(connection)
            self.hedge_rule = HedgeRuleRepository(connection)
            self.market = MarketRepository(connection)
            self.market_type = MarketTypeRepository(connection)
            self.selection = SelectionRepository(connection)
            self.sport = SportRepository(connection)
            self.user_hedge_profile = UserHedgeProfileRepository(connection)