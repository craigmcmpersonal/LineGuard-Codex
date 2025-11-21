from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar

from develop.model.bet_leg_odds_history import BetLegOddsHistory
from develop.repository.base_repository import BaseRepository


class BetLegOddsHistoryRepository(BaseRepository[BetLegOddsHistory]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
bet_leg_key,
book_key,
odds,
captured_time
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Bet_Leg_Odds_History" (
    bet_leg_key,
    book_key,
    odds,
    captured_time
)
VALUES ($1, $2, $3, COALESCE($4, now()))
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Bet_Leg_Odds_History"
WHERE key = $1
RETURNING key;
"""

    _SQL_TRY_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Leg_Odds_History"
WHERE bet_leg_key = $1
ORDER BY captured_time DESC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Bet_Leg_Odds_History"
WHERE key = $1;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, BetLegOddsHistory)

    async def create(
        self,
        bet_leg_key: int,
        book_key: str,
        odds: Decimal,
        captured_time: datetime | None = None,
    ) -> BetLegOddsHistory | None:
        result: BetLegOddsHistory | None = await self._fetch_row(
            self._SQL_CREATE,
            bet_leg_key,
            book_key,
            odds,
            captured_time,
        )
        return result

    async def find(self, bet_leg_key: int) -> list[BetLegOddsHistory]:
        result: list[BetLegOddsHistory] = await self._fetch_all(self._SQL_TRY_FIND, bet_leg_key)
        return result

    async def try_get(self, key: int) -> BetLegOddsHistory | None:
        result: BetLegOddsHistory | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def try_delete(self, odds_history: BetLegOddsHistory | int) -> bool:
        result: bool = await self._execute(
            self._SQL_DELETE, odds_history.key if isinstance(
                odds_history,
                BetLegOddsHistory
            ) else odds_history
        )
        return result




