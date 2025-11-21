from typing import Any

from develop.persistence.bet_leg_odds_history_storage_adapter import BetLegOddsHistoryStorageAdapter
from develop.persistence.bet_leg_storage_adapter import BetLegStorageAdapter
from develop.persistence.bet_slip_storage_adapter import BetSlipStorageAdapter
from develop.persistence.book_storage_adapter import BookStorageAdapter
from develop.persistence.entrant_storage_adapter import EntrantStorageAdapter
from develop.persistence.event_storage_adapter import EventStorageAdapter
from develop.persistence.hedge_opportunity_leg_storage_adapter import HedgeOpportunityLegStorageAdapter
from develop.persistence.hedge_opportunity_storage_adapter import HedgeOpportunityStorageAdapter
from develop.persistence.hedge_rule_filter_storage_adapter import HedgeRuleFilterStorageAdapter
from develop.persistence.hedge_rule_storage_adapter import HedgeRuleStorageAdapter
from develop.persistence.market_storage_adapter import MarketStorageAdapter
from develop.persistence.market_type_storage_adapter import MarketTypeStorageAdapter
from develop.persistence.odds_movement_storage_adapter import OddsMovementStorageAdapter
from develop.persistence.odds_snapshot_storage_adapter import OddsSnapshotStorageAdapter
from develop.persistence.race_result_storage_adapter import RaceResultStorageAdapter
from develop.persistence.rule_evaluation_log_storage_adapter import RuleEvaluationLogStorageAdapter
from develop.persistence.selection_storage_adapter import SelectionStorageAdapter
from develop.persistence.sport_storage_adapter import SportStorageAdapter
from develop.persistence.user_alert_storage_adapter import UserAlertStorageAdapter
from develop.persistence.user_hedge_profile_storage_adapter import UserHedgeProfileStorageAdapter


class StorageAdapter:
    def __init__(self, connection: Any):
        if not connection:
            raise ValueError()
        else:
            self.connection = connection
            self.bet_leg = BetLegStorageAdapter(connection)
            self.bet_leg_odds_history = BetLegOddsHistoryStorageAdapter(connection)
            self.bet_slip = BetSlipStorageAdapter(connection)
            self.book = BookStorageAdapter(connection)
            self.entrant = EntrantStorageAdapter(connection)
            self.event = EventStorageAdapter(connection)
            self.hedge_opportunity = HedgeOpportunityStorageAdapter(connection)
            self.hedge_opportunity_leg = HedgeOpportunityLegStorageAdapter(connection)
            self.hedge_rule = HedgeRuleStorageAdapter(connection)
            self.hedge_rule_filter = HedgeRuleFilterStorageAdapter(connection)
            self.market = MarketStorageAdapter(connection)
            self.market_type = MarketTypeStorageAdapter(connection)
            self.odds_snapshot = OddsSnapshotStorageAdapter(connection)
            self.odds_movement = OddsMovementStorageAdapter(connection)
            self.race_result = RaceResultStorageAdapter(connection)
            self.rule_evaluation_log = RuleEvaluationLogStorageAdapter(connection)
            self.selection = SelectionStorageAdapter(connection)
            self.sport = SportStorageAdapter(connection)
            self.user_alert = UserAlertStorageAdapter(connection)
            self.user_hedge_profile = UserHedgeProfileStorageAdapter(connection)