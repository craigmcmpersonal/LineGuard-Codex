from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar

from develop.persistance.model import BetLeg
from develop.persistance.model import BetLegStatus
from develop.persistance.base_repository import BaseRepository


class BetLegRepository(BaseRepository[BetLeg]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
bet_slip_key,
selection_key,
odds,
status,
result,
index,
odds_live,
settled_time,
public_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Bet_Leg" (
    bet_slip_key,
    selection_key,
    odds,
    status,
    index
)
VALUES ($1, $2, $3, $4, $5)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Leg"
WHERE key = $1;
"""

    _SQL_FIND_BET_SLIP: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Leg"
WHERE bet_slip_key = $1
ORDER BY index;
"""

    _SQL_FIND_PUBLIC_KEY: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Leg"
WHERE public_key = $1;
"""

    _SQL_FIND_SELECTION_STATUS: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Leg"
WHERE selection_key = $1
  AND status = $2
ORDER BY index;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Bet_Leg"
SET status=$2,
    odds_live = $3,
    settled_time = COALESCE($4, settled_time),
    result = COALESCE($5, result)
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Bet_Leg"
WHERE key = $1
RETURNING key;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, BetLeg)

    async def create(
        self,
        bet_slip_key: int,
        selection_key: int,
        odds: Decimal,
        index: int,
        status: BetLegStatus = BetLegStatus.PENDING,
    ) -> BetLeg | None:
        result: BetLeg | None = await self._fetch_row(
            self._SQL_CREATE,
            bet_slip_key,
            selection_key,
            odds,
            status.value,
            index,
        )
        return result

    async def find_by_bet_slip(self, bet_slip_key: int) -> list[BetLeg]:
        result: list[BetLeg] = await self._fetch_all(self._SQL_FIND_BET_SLIP, bet_slip_key)
        return result

    async def find_by_selection_status(self, selection_key: int, status: BetLegStatus) -> list[BetLeg]:
        result: list[BetLeg] = await self._fetch_all(self._SQL_FIND_SELECTION_STATUS, selection_key, status.value)
        return result

    async def try_delete(self, bet_leg: BetLeg | int) -> bool:
        key = bet_leg.key if isinstance(bet_leg, BetLeg) else bet_leg
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_find(self, public_key: str) -> BetLeg:
        result: BetLeg = await self._fetch_row(self._SQL_FIND_PUBLIC_KEY, public_key)
        return result

    async def try_get(self, key: int) -> BetLeg | None:
        result: BetLeg | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, bet_leg: BetLeg) -> BetLeg | None:
        result: BetLeg | None = await self._fetch_row(
            self._SQL_UPDATE,
            bet_leg.key,
            bet_leg.status.value,
            bet_leg.odds_live,
            bet_leg.settled_time,
            bet_leg.result
        )
        return result
