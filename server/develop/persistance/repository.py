from typing import Any

from develop.persistance.bet_leg_odds_history_repository import BetLegOddsHistoryRepository
from develop.persistance.bet_leg_repository import BetLegRepository
from develop.persistance.bet_slip_repository import BetSlipRepository
from develop.persistance.book_repository import BookRepository
from develop.persistance.entrant_repository import EntrantRepository
from develop.persistance.event_repository import EventRepository
from develop.persistance.hedge_opportunity_leg_repository import HedgeOpportunityLegRepository
from develop.persistance.hedge_opportunity_repository import HedgeOpportunityRepository
from develop.persistance.hedge_rule_filter_repository import HedgeRuleFilterRepository
from develop.persistance.hedge_rule_repository import HedgeRuleRepository
from develop.persistance.market_repository import MarketRepository
from develop.persistance.market_type_repository import MarketTypeRepository
from develop.persistance.odds_movement_repository import OddsMovementRepository
from develop.persistance.odds_snapshot_repository import OddsSnapshotRepository
from develop.persistance.race_result_repository import RaceResultRepository
from develop.persistance.rule_evaluation_log_repository import RuleEvaluationLogRepository
from develop.persistance.selection_repository import SelectionRepository
from develop.persistance.sport_repository import SportRepository
from develop.persistance.user_alert_repository import UserAlertRepository
from develop.persistance.user_hedge_profile_repository import UserHedgeProfileRepository


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
            self.hedge_opportunity = HedgeOpportunityRepository(connection)
            self.hedge_opportunity_leg = HedgeOpportunityLegRepository(connection)
            self.hedge_rule = HedgeRuleRepository(connection)
            self.hedge_rule_filter = HedgeRuleFilterRepository(connection)
            self.market = MarketRepository(connection)
            self.market_type = MarketTypeRepository(connection)
            self.odds_snapshot = OddsSnapshotRepository(connection)
            self.odds_movement = OddsMovementRepository(connection)
            self.race_result = RaceResultRepository(connection)
            self.rule_evaluation_log = RuleEvaluationLogRepository(connection)
            self.selection = SelectionRepository(connection)
            self.sport = SportRepository(connection)
            self.user_alert = UserAlertRepository(connection)
            self.user_hedge_profile = UserHedgeProfileRepository(connection)