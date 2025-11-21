from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.hedge_rule_filter import HedgeRuleFilter


class HedgeRuleFilterStorageAdapter(BaseStorageAdapter[HedgeRuleFilter]):


    _SELECT_COLUMNS: ClassVar[str] = """
key,
hedge_rule_key,
sport_key,
market_type_key,
minimum_odds,
maximum_odds
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Hedge_Rule_Filter" (
    hedge_rule_key,
    sport_key,
    market_type_key,
    minimum_odds,
    maximum_odds
)
VALUES ($1, $2, $3, $4, $5)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Hedge_Rule_Filter"
WHERE key = $1
RETURNING key;
"""

    _SQL_TRY_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Rule_Filter"
WHERE hedge_rule_key = $1
ORDER BY sport_key, market_type_key;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Rule_Filter"
WHERE key = $1;
"""
    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Hedge_Rule_Filter"
SET minimum_odds = $2,
    maximum_odds = $3
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, HedgeRuleFilter)

    async def create(
        self,
        hedge_rule_key: int,
        *,
        sport_key: int | None = None,
        market_type_key: int | None = None,
        minimum_odds: Decimal | None = None,
        maximum_odds: Decimal | None = None,
    ) -> HedgeRuleFilter | None:
        result: HedgeRuleFilter | None = await self._fetch_row(
            self._SQL_CREATE,
            hedge_rule_key,
            sport_key,
            market_type_key,
            minimum_odds,
            maximum_odds,
        )
        return result

    async def find(self, hedge_rule_key: int) -> list[HedgeRuleFilter]:
        result: list[HedgeRuleFilter] = await self._fetch_all(self._SQL_TRY_FIND, hedge_rule_key)
        return result

    async def try_delete(self, hedge_rule_filter: HedgeRuleFilter | int) -> bool:
        key = hedge_rule_filter.key if isinstance(hedge_rule_filter, HedgeRuleFilter) else hedge_rule_filter
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> HedgeRuleFilter | None:
        result: HedgeRuleFilter | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, hedge_rule_filter: HedgeRuleFilter) -> HedgeRuleFilter | None:
        result: HedgeRuleFilter | None = await self._fetch_row(
            self._SQL_UPDATE,
            hedge_rule_filter.key,
            hedge_rule_filter.minimum_odds,
            hedge_rule_filter.maximum_odds,
        )
        return result
