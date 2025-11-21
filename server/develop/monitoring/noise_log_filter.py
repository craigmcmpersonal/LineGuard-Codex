import logging
import re
from typing import ClassVar, Any


class NoiseLogFilter(logging.Filter):
    _ADDRESS_APPLICATION_INSIGHTS: ClassVar[str] = ".applicationinsights.azure.com"
    _PATTERN_PATH_NAME: ClassVar[str] = r"([/\\]{1,2}azure[/\\]{1,2}core[/\\]{1,2}pipeline[/\\]{1,2}policies[/\\]{1,2}_universal.py)|(opentelemetry)"
    _EXPRESSION_PATH_NAME: re.Pattern[str] = re.compile(_PATTERN_PATH_NAME)

    @staticmethod
    def _reject(value: Any) -> bool:
        result: bool = isinstance(value, str) and NoiseLogFilter._ADDRESS_APPLICATION_INSIGHTS in value
        return result

    def filter(self, record: logging.LogRecord) -> bool:
        if record and record.msg is not None and NoiseLogFilter._reject(record.msg):
            return False
        elif record.args and [
            item
            for item in record.args
            if NoiseLogFilter._reject(item)
        ]:
            return False
        elif record.pathname is not None and isinstance(
                record.pathname,
                str
        ) and (NoiseLogFilter._EXPRESSION_PATH_NAME.search(record.pathname) is not None):
                return False
        return True