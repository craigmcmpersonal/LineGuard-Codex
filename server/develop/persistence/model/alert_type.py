from enum import Enum


class AlertType(str, Enum):
    HEDGE_OPPORTUNITY = "Hedge Opportunity"
    RULE_TRIGGERED = "Rule Triggered"
    ODDS_MOVEMENT = "Odds Movement"
    BET_STATUS_CHANGE = "Bet Status Change"