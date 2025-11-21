from datetime import datetime, timezone
from logging import LogRecord

from develop import constants
from develop.monitoring.json_logging_formatter import JsonLoggingFormatter


class CoordinatedUniversalTimeLoggingFormatter(JsonLoggingFormatter):
    def formatTime(self, record: LogRecord, datefmt: str|None=None) -> str:
        coordinated_universal_time: datetime = datetime.fromtimestamp(record.created, tz=timezone.utc)
        effective_format: str = datefmt or constants.DATETIME_FORMAT_ROUNDTRIP
        result: str
        try:
            result = coordinated_universal_time.strftime(effective_format)
        except ValueError:
            result = coordinated_universal_time.strftime(constants.DATETIME_FORMAT_ROUNDTRIP)
        return result