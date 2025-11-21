from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar
from uuid import UUID

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.hedge_opportunity import HedgeOpportunity
from develop.persistence.model.hedge_opportunity_status import HedgeOpportunityStatus


class HedgeOpportunityStorageAdapter(BaseStorageAdapter[HedgeOpportunity]):
    _SELECT_COLUMN_LIST: ClassVar[list[str]] = [
        "key",
        "bet_slip_key",
        "hedge_rule_key",
        "trigger_reason",
        "original_win_probability",
        "recommended_hedge_stake",
        "optimal_hedge_odds",
        "creation_time",
        "expiration_time",
        "status"
    ]
    _SELECT_COLUMNS: ClassVar[str] = ",".join(_SELECT_COLUMN_LIST)
    _SELECT_COLUMNS_PREFIXED: ClassVar[str] = ",".join([
        "opportunity." + item
        for item in _SELECT_COLUMN_LIST
    ])

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Hedge_Opportunity" (
    bet_slip_key,
    hedge_rule_key,
    trigger_reason,
    original_win_probability,
    recommended_hedge_stake,
    optimal_hedge_odds,
    status
)
VALUES ($1, $2, $3, $4, $5, $6, $7)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Hedge_Opportunity"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND_USER: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS_PREFIXED}
FROM public."Hedge_Opportunity" opportunity
JOIN public."Bet_Slip" slip ON opportunity.bet_slip_key = slip.key
WHERE slip.user_key = $1
ORDER BY opportunity.creation_time DESC;
"""

    _SQL_FIND_BET_SLIP: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Opportunity"
WHERE bet_slip_key = $1
ORDER BY creation_time DESC;
"""

    _SQL_FIND_HEDGE_RULE: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Opportunity"
WHERE hedge_rule_key = $1
ORDER BY creation_time DESC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Opportunity"
WHERE key = $1;
"""

    _SQL_UPDATE_STATUS: ClassVar[str] = f"""
UPDATE public."Hedge_Opportunity"
SET status = $2,
    expiration_time = COALESCE($3, expiration_time)
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, HedgeOpportunity)

    async def create(
        self,
        bet_slip_key: int,
        hedge_rule_key: int,
        *,
        trigger_reason: str | None = None,
        original_win_probability: Decimal | None = None,
        recommended_hedge_stake: Decimal | None = None,
        optimal_hedge_odds: Decimal | None = None,
        status: HedgeOpportunityStatus = HedgeOpportunityStatus.ACTIVE,
    ) -> HedgeOpportunity | None:
        result: HedgeOpportunity | None = await self._fetch_row(
            self._SQL_CREATE,
            bet_slip_key,
            hedge_rule_key,
            trigger_reason,
            original_win_probability,
            recommended_hedge_stake,
            optimal_hedge_odds,
            status.value if status else None,
        )
        return result

    async def find_by_bet_slip(self, bet_slip_key: int) -> list[HedgeOpportunity]:
        result: list[HedgeOpportunity] | None = await self._fetch_all(self._SQL_FIND_BET_SLIP, bet_slip_key)
        return result

    async def find_by_hedge_rule(self, hedge_rule_key: int) -> list[HedgeOpportunity]:
        result: list[HedgeOpportunity] | None = await self._fetch_all(self._SQL_FIND_HEDGE_RULE, hedge_rule_key)
        return result

    async def find_by_user(self, user_key: UUID) -> list[HedgeOpportunity]:
        result: list[HedgeOpportunity] = await self._fetch_all(self._SQL_FIND_USER, user_key)
        return result

    async def try_delete(self, opportunity: HedgeOpportunity | int) -> bool:
        key = opportunity.key if isinstance(opportunity, HedgeOpportunity) else opportunity
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> HedgeOpportunity | None:
        result: HedgeOpportunity | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, hedge_opportunity: HedgeOpportunity) -> HedgeOpportunity | None:
        result: HedgeOpportunity | None = await self._fetch_row(
            self._SQL_UPDATE_STATUS,
            hedge_opportunity.key,
            hedge_opportunity.status.value,
            hedge_opportunity.expiration_time
        )
        return result
