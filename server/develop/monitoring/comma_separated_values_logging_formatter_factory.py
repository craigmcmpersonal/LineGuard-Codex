import logging

import contextvars

from develop.monitoring.base_logging_formatter_factory import BaseLoggingFormatterFactory
from develop.monitoring.comma_separated_values_logging_formatter import CommaSeparatedValuesLoggingFormatter


class CommaSeparatedValuesLoggingFormatterFactory(BaseLoggingFormatterFactory):
    def __init__(self, context: contextvars.ContextVar):
        super().__init__()
        self._context: contextvars.ContextVar = context

    def create_formatter(self) -> logging.Formatter:
        result: logging.Formatter = CommaSeparatedValuesLoggingFormatter(self._context)
        return result