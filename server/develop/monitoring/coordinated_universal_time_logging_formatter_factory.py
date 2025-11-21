import logging

from develop.monitoring.base_logging_formatter_factory import BaseLoggingFormatterFactory
from develop.monitoring.coordinated_universal_time_logging_formatter import CoordinatedUniversalTimeLoggingFormatter


class CoordinatedUniversalTimeLoggingFormatterFactory(BaseLoggingFormatterFactory):
    def create_formatter(self) -> logging.Formatter:
        result: logging.Formatter = CoordinatedUniversalTimeLoggingFormatter(self.logging_format)
        return result
