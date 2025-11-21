from typing import Any, ClassVar

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.hedge_rule_bet_slip import HedgeRuleBetSlip


class HedgeRuleBetSlipStorageAdapter(BaseStorageAdapter[HedgeRuleBetSlip]):
        _SELECT_COLUMNS: str = """
hedge_rule_key,
bet_slip_key
"""

        _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Hedge_Rule_x_Bet_Slip" (
    hedge_rule_key,
    bet_slip_key
)
VALUES ($1, $2)
RETURNING {_SELECT_COLUMNS};
    """

        _SQL_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Rule_x_Bet_Slip"
WHERE hedge_rule_key = $1
ORDER BY bet_slip_key;
"""

        _SQL_DELETE: ClassVar[str] = f"""
DELETE FROM public."Hedge_Rule_x_Bet_Slip"
WHERE hedge_rule_key = $1 AND bet_slip_key = $2
RETURNING {_SELECT_COLUMNS};
"""

        def __init__(self, connection: Any):
            super().__init__(connection, HedgeRuleBetSlip)

        async def create(self, hedge_rule_key: int, bet_slip_key: int) -> HedgeRuleBetSlip:
            result: HedgeRuleBetSlip = await self._fetch_row(self._SQL_CREATE, hedge_rule_key, bet_slip_key)
            return result

        async def find(self, hedge_rule_key: int) -> list[HedgeRuleBetSlip]:
            result: list[HedgeRuleBetSlip] = await self._fetch_all(self._SQL_FIND, hedge_rule_key)
            return result

        async def try_delete(self, hedge_rule_bet_slip: HedgeRuleBetSlip) -> HedgeRuleBetSlip | None:
            result: HedgeRuleBetSlip = await self._fetch_row(
                self._SQL_DELETE,
                hedge_rule_bet_slip.hedge_rule_key,
                hedge_rule_bet_slip.bet_slip_key
            )
            return result