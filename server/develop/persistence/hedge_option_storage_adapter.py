from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.hedge_option import HedgeOption


class HedgeOptionStorageAdapter(BaseStorageAdapter[HedgeOption]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
hedge_opportunity_key,
book,
odds,
required_stake,
guaranteed_profit,
implied_probability,
option_rank,
public_key,
resource_location,
last_update_time
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Hedge_Option" (
    hedge_opportunity_key,
    book,
    odds,
    required_stake,
    guaranteed_profit,
    implied_probability,
    option_rank,
    public_key,
    resource_location,
    last_update_time
)
VALUES ($1, $2, $3, $4, $5, $6, $7, COALESCE($8, gen_random_uuid()), $9, COALESCE($10, now()))
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Hedge_Option"
WHERE key = $1
RETURNING key;
"""

    _SQL_LIST_FOR_OPPORTUNITIES: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Option"
WHERE hedge_opportunity_key = ANY($1::bigint[])
ORDER BY hedge_opportunity_key ASC, option_rank ASC;
"""

    _SQL_TRY_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Option"
WHERE hedge_opportunity_key = $1
  AND option_rank = $2
ORDER BY key DESC
LIMIT 1;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Option"
WHERE key = $1;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, HedgeOption)

    async def create(
        self,
        hedge_opportunity_key: int,
        book: str,
        odds: Decimal,
        required_stake: Decimal,
        guaranteed_profit: Decimal,
        *,
        implied_probability: Decimal | None = None,
        option_rank: int = 1,
        public_key: UUID | None = None,
        resource_location: str | None = None,
        last_update_time: datetime | None = None,
    ) -> HedgeOption | None:
        result: HedgeOption | None = await self._fetch_row(
            self._SQL_CREATE,
            hedge_opportunity_key,
            book,
            odds,
            required_stake,
            guaranteed_profit,
            implied_probability,
            option_rank,
            public_key,
            resource_location,
            last_update_time,
        )
        return result

    async def list_for_opportunities(self, opportunity_keys: Sequence[int]) -> list[HedgeOption]:
        if not opportunity_keys:
            return []
        result: list[HedgeOption] = await self._fetch_all(
            self._SQL_LIST_FOR_OPPORTUNITIES,
            list(opportunity_keys),
        )
        return result

    async def try_delete(self, hedge_option: HedgeOption | int) -> bool:
        key = hedge_option.key if isinstance(hedge_option, HedgeOption) else hedge_option
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_find(self, hedge_opportunity_key: int, option_rank: int) -> HedgeOption | None:
        result: HedgeOption | None = await self._fetch_row(self._SQL_TRY_FIND, hedge_opportunity_key, option_rank)
        return result

    async def try_get(self, key: int) -> HedgeOption | None:
        result: HedgeOption | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result
