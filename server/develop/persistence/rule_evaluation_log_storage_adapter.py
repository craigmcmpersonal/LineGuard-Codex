from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar

from develop.persistence.base_storage_adapter import BaseStorageAdapter
from develop.persistence.model.rule_evaluation_log import RuleEvaluationLog


class RuleEvaluationLogStorageAdapter(BaseStorageAdapter[RuleEvaluationLog]):

    _SELECT_COLUMNS: ClassVar[str] = """
key,
hedge_rule_key,
bet_slip_key,
evaluation_time,
inputs,
output,
hedge_opportunity_key
"""

    _SQL_CREATE: ClassVar[str] = f"""
INSERT INTO public."Rule_Evaluation_Log" (
    hedge_rule_key,
    bet_slip_key,
    evaluation_time,
    inputs,
    output,
    hedge_opportunity_key
)
VALUES ($1, $2, COALESCE($3, now()), $4, $5, $6)
RETURNING {_SELECT_COLUMNS};
"""

    _SQL_DELETE: ClassVar[str] = """
DELETE FROM public."Rule_Evaluation_Log"
WHERE key = $1
RETURNING key;
"""

    _SQL_FIND_BY_BET_SLIP: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Rule_Evaluation_Log"
WHERE bet_slip_key = $1
ORDER BY evaluation_time DESC;
"""

    _SQL_FIND_BY_HEDGE_RULE: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Rule_Evaluation_Log"
WHERE hedge_rule_key = $1
ORDER BY evaluation_time DESC
LIMIT 1;
"""

    _SQL_TRY_GET: ClassVar[str] = f"""
SELECT {_SELECT_COLUMNS}
FROM public."Rule_Evaluation_Log"
WHERE key = $1;
"""

    def __init__(self, connection: Any):
        super().__init__(connection, RuleEvaluationLog)

    async def create(
        self,
        hedge_rule_key: int,
        bet_slip_key: int,
        inputs: Any,
        output: Any,
        *,
        evaluation_time: datetime | None = None,
        hedge_opportunity_key: int | None = None,
    ) -> RuleEvaluationLog | None:
        result: RuleEvaluationLog | None = await self._fetch_row(
            self._SQL_CREATE,
            hedge_rule_key,
            bet_slip_key,
            evaluation_time,
            inputs,
            output,
            hedge_opportunity_key,
        )
        return result

    async def find_by_bet_slip(self, bet_slip_key: int) -> list[RuleEvaluationLog]:
        result: list[RuleEvaluationLog] = await self._fetch_all(self._SQL_FIND_BY_BET_SLIP, bet_slip_key)
        return result

    async def find_by_hedge_rule(self, hedge_rule_key: int) -> list[RuleEvaluationLog]:
        result: list[RuleEvaluationLog] = await self._fetch_all(self._SQL_FIND_BY_HEDGE_RULE, hedge_rule_key)
        return result

    async def try_delete(self, evaluation_log: RuleEvaluationLog | int) -> bool:
        key = evaluation_log.key if isinstance(evaluation_log, RuleEvaluationLog) else evaluation_log
        result: bool = await self._execute(self._SQL_DELETE, key)
        return result

    async def try_get(self, key: int) -> RuleEvaluationLog | None:
        result: RuleEvaluationLog | None = await self._fetch_row(self._SQL_TRY_GET, key)
        return result
