import logging
import re
import traceback
from typing import Callable, ClassVar

import develop.constants as constants
from develop.monitoring.coordinated_universal_time_logging_formatter import CoordinatedUniversalTimeLoggingFormatter


class StackTracingFormatter(CoordinatedUniversalTimeLoggingFormatter):
    _DEVELOP_STACK_PATTERN: ClassVar[str] = r"[/\\]{1,2}develop[/\\]{1,2}"
    _DEVELOP_STACK_EXPRESSION: ClassVar[re.Pattern] = re.compile(_DEVELOP_STACK_PATTERN)
    _MONITORING_STACK_PATTERN: ClassVar[str] = r"[/\\]{1,2}develop[/\\]{1,2}monitoring[/\\]{1,2}"
    _MONITORING_STACK_EXPRESSION: ClassVar[re.Pattern] = re.compile(_MONITORING_STACK_PATTERN)

    @staticmethod
    def filter_stack(get_stack_function: Callable[[], list[str]]) -> list[str]:
        result: list[str] = [
            item
            for item in get_stack_function()
            if re.search(StackTracingFormatter._DEVELOP_STACK_EXPRESSION, item) is not None
            if re.search(StackTracingFormatter._MONITORING_STACK_EXPRESSION, item) is None
        ][:-1]
        return result

    @staticmethod
    def get_stack_trace(record: logging.LogRecord) -> str:
        stack_traces: list[str] = StackTracingFormatter.get_stack_traces(record)
        result: str = constants.EMPTY_STRING.join(stack_traces)
        return result

    @staticmethod
    def get_stack_traces(record: logging.LogRecord) -> list[str]:
        result: list[str]
        if record.exc_info:
            exception_type, exception_value, exception_traceback = record.exc_info
            result = traceback.format_exception(exception_type, exception_value, exception_traceback)
        else:
            result = StackTracingFormatter.filter_stack(get_stack_function=traceback.format_stack)
        return result

