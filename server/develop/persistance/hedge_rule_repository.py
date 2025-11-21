from __future__ import annotations

from typing import ClassVar, Any

from develop.persistance.model.hedge_rule import HedgeRule
from develop.persistance.model import HedgeRuleBetSlip
from develop.persistance.base_repository import BaseRepository
from develop.persistance.hedge_rule_bet_slip_repository import HedgeRuleBetSlipRepository


class HedgeRuleRepository(BaseRepository[HedgeRule]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
user_hedge_profile_key,
rule_name,
original,
model,
priority,
active,
creation_time,
version,
valid_from,
valid_to
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Hedge_Rule" (
    user_hedge_profile_key,
    rule_name,
    original,
    model,
    priority,
    active,
    version
)
VALUES ($1, $2, $3, $4, $5, COALESCE($6, true), COALESCE($7, 1))
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DEACTIVATE: ClassVar[str] = f"""
UPDATE public."Hedge_Rule"
SET active = false,
    valid_to = now()
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Hedge_Rule"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Rule"
WHERE user_hedge_profile_key = $1
  AND active = true
ORDER BY priority ASC, rule_name ASC, creation_time DESC;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Hedge_Rule"
WHERE key = $1;
"""

    _SQL_UPDATE_MODEL: ClassVar[str] = f"""
UPDATE public."Hedge_Rule"
SET model = $2
WHERE key = $1
RETURNING {_SELECT_COLUMNS};
"""

    def __init__(self, connection: Any):
        super().__init__(connection, HedgeRule)
        self._bets_slips = HedgeRuleBetSlipRepository(connection)

    async def add_bet_slip(self, hedge_rule_key: int, bet_slip_key: int) -> HedgeRuleBetSlip:
        result: HedgeRuleBetSlip = await self._bets_slips.create(hedge_rule_key, bet_slip_key)
        return result

    async def create(
        self,
        user_hedge_profile_key: int,
        rule_name: str,
        original: str,
        *,
        model: Any | None = None,
        priority: int = 1,
        active: bool = True,
        version: int = 1,
    ) -> HedgeRule | None:
        result: HedgeRule | None = await self._fetch_row(
            self._SQL_CREATE,
            user_hedge_profile_key,
            rule_name,
            original,
            model,
            priority,
            active,
            version,
        )
        return result

    async def deactivate(self, hedge_rule: HedgeRule) -> HedgeRule | None:
        result: HedgeRule | None = await self._fetch_row(self._SQL_DEACTIVATE, hedge_rule.key)
        return result

    async def find(self, user_hedge_profile_key: int) -> list[HedgeRule]:
        result: list[HedgeRule] = await self._fetch_all(self._SQL_FIND, user_hedge_profile_key)
        return result

    async def find_bet_slips(self, hedge_rule_key: int) -> list[HedgeRuleBetSlip]:
        result: list[HedgeRuleBetSlip] = await self._bets_slips.find(hedge_rule_key)
        return result

    async def try_delete(self, hedge_rule: HedgeRule | int) -> bool:
        key = hedge_rule.key if isinstance(hedge_rule, HedgeRule) else hedge_rule
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> HedgeRule | None:
        result: HedgeRule | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result

    async def remove_bet_slip(self, hedge_rule_bet_slip: HedgeRuleBetSlip) -> HedgeRuleBetSlip|None:
        result: HedgeRuleBetSlip|None = await self._bets_slips.try_delete(hedge_rule_bet_slip)
        return result

    async def update_model(self, hedge_rule: HedgeRule) -> HedgeRule | None:
        result: HedgeRule | None = await self._fetch_row(self._SQL_UPDATE_MODEL, hedge_rule.key, hedge_rule.model)
        return result


