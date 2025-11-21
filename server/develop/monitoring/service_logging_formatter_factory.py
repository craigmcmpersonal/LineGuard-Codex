import contextvars
import logging

from develop.monitoring.base_logging_formatter_factory import BaseLoggingFormatterFactory
from develop.monitoring.service_logging_formatter import ServiceLoggingFormatter


class ServiceLoggingFormatterFactory(BaseLoggingFormatterFactory):
    def __init__(self, context: contextvars.ContextVar):
        self._context: contextvars.ContextVar = context
        super().__init__()

    def create_formatter(self) -> logging.Formatter:
        result: logging.Formatter = ServiceLoggingFormatter(self._context)
        return result