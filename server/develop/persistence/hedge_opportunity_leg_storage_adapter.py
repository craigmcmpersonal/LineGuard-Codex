from __future__ import annotations

from typing import Any, ClassVar

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.hedge_opportunity_leg import HedgeOpportunityLeg


class HedgeOpportunityLegStorageAdapter(BaseStorageAdapter[HedgeOpportunityLeg]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
hedge_opportunity_key,
bet_leg_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Hedge_Opportunity_Leg" (
    hedge_opportunity_key,
    bet_leg_key
)
VALUES ($1, $2)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Hedge_Opportunity_Leg"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND_OPPORTUNITY: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Opportunity_Leg"
WHERE hedge_opportunity_key = $1
ORDER BY bet_leg_key;
"""

    _SQL_FIND_LEG: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Opportunity_Leg"
WHERE bet_leg_key = $1
ORDER BY hedge_opportunity_key;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Opportunity_Leg"
WHERE key = $1;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, HedgeOpportunityLeg)

    async def create(self, hedge_opportunity_key: int, bet_leg_key: int) -> HedgeOpportunityLeg | None:
        result: HedgeOpportunityLeg | None = await self._fetch_row(
            self._SQL_CREATE,
            hedge_opportunity_key,
            bet_leg_key,
        )
        return result

    async def find_by_hedge_opportunity(self, hedge_opportunity_key: int) -> list[HedgeOpportunityLeg]:
        result: list[HedgeOpportunityLeg] = await self._fetch_all(
            self._SQL_FIND_OPPORTUNITY,
            hedge_opportunity_key,
        )
        return result

    async def find_by_bet_leg(self, bet_leg_key: int) -> list[HedgeOpportunityLeg]:
        result: list[HedgeOpportunityLeg] = await self._fetch_all(self._SQL_FIND_LEG, bet_leg_key)
        return result

    async def try_delete(self, opportunity_leg: HedgeOpportunityLeg | int) -> bool:
        key = opportunity_leg.key if isinstance(opportunity_leg, HedgeOpportunityLeg) else opportunity_leg
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> HedgeOpportunityLeg | None:
        result: HedgeOpportunityLeg | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result
