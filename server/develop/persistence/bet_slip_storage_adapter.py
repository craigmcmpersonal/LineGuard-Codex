from __future__ import annotations

from decimal import Decimal
from typing import Any, ClassVar
from uuid import UUID

from develop.persistence.model.bet_slip import BetSlip
from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.bet_slip_source import BetSlipSource
from develop.persistence.model.bet_slip_status import BetSlipStatus
from develop.utility import compose_unique_identifier


class BetSlipStorageAdapter(BaseStorageAdapter[BetSlip]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
user_key,
total_odds,
stake,
status,
placed_time,
settled_time,
result,
external_identifier,
original,
model,
import_time,
source,
last_update_time,
total_odds_live,
public_key,
will_pay,
book_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Bet_Slip" (
    user_key,
    total_odds,
    stake,
    status,
    external_identifier,
    original,
    model,
    source,
    total_odds_live,
    will_pay,
    book_key
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Bet_Slip"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND_USER_STATUS: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Slip"
WHERE user_key = $1
  AND status = $2
ORDER BY placed_time DESC;
"""

    _SQL_FIND_USER_BOOK_EXTERNAL_IDENTIFIER: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Slip"
WHERE user_key = $1
  AND book_key = $2
  AND external_identifier = $3
ORDER BY placed_time DESC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Slip"
WHERE key = $1;
"""

    _SQL_UPDATE: ClassVar[str] = f"""
UPDATE public."Bet_Slip"
SET total_odds_live = $2,
    status = $3,
    settled_time = $4,
    result=$5,
    will_pay=$6,
    last_update_time = now()
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, BetSlip)

    async def create(
        self,
        user_key: UUID,
        book_key: int,
        total_odds: Decimal,
        stake: Decimal,
        status: BetSlipStatus,
        original: bytes,
        source: BetSlipSource,
        *,
        external_identifier: str | None,
        model: Any | None = None,
        total_odds_live: Decimal | None = None,
        will_pay: Decimal | None = None,
    ) -> BetSlip | None:
        result: BetSlip | None = await self._fetch_row(
            self._SQL_CREATE,
            user_key,
            total_odds,
            stake,
            status.value,
            external_identifier if external_identifier is not None else compose_unique_identifier(),
            original,
            model,
            source.value,
            total_odds_live,
            will_pay,
            book_key,
        )
        return result

    async def find_by_book_identifier(
        self,
        user_key: UUID,
        book_key: int|None = None,
        external_identifier: str|None = None
    ) -> list[BetSlip]:
        result: list[BetSlip] = await self._fetch_all(
            self._SQL_FIND_USER_BOOK_EXTERNAL_IDENTIFIER,
            user_key,
            book_key,
            external_identifier
        )
        return result

    async def find_by_status(
        self,
        user_key: UUID,
        status: BetSlipStatus|None = None,
    ) -> list[BetSlip]:
        result: list[BetSlip] = await self._fetch_all(
            self._SQL_FIND_USER_STATUS,
            user_key,
            status.value,
        )
        return result

    async def try_delete(self, bet_slip: BetSlip | int) -> bool:
        key = bet_slip.key if isinstance(bet_slip, BetSlip) else bet_slip
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> BetSlip | None:
        result: BetSlip | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def update(self, bet_slip: BetSlip) -> BetSlip | None:
        result: BetSlip | None = await self._fetch_row(
            self._SQL_UPDATE,
            bet_slip.key,
            bet_slip.total_odds_live,
            bet_slip.status.value,
            bet_slip.settled_time,
            bet_slip.result,
            bet_slip.will_pay
        )
        return result
