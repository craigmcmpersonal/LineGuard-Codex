import logging
import csv
import io
from typing import Any

import contextvars

import develop.constants as constants
from develop.monitoring.stack_tracing_formatter import StackTracingFormatter


class CommaSeparatedValuesLoggingFormatter(StackTracingFormatter):
    def __init__(self, context: contextvars.ContextVar):
        super().__init__()
        self._context: contextvars.ContextVar = context

    def format(self, record: logging.LogRecord) -> str:
        log_time: str = self.formatTime(record=record)
        activity: str = self._context.get().get(constants.CONTEXT_KEY_ACTIVITY, constants.UNKNOWN)
        command: str = self._context.get().get(constants.CONTEXT_KEY_COMMAND, constants.UNKNOWN)
        phase: str = self._context.get().get(constants.CONTEXT_KEY_PHASE, constants.UNKNOWN)
        module: str = self._context.get().get(constants.CONTEXT_KEY_MODULE, constants.UNKNOWN)
        file: str = self._context.get().get(constants.CONTEXT_KEY_FILE, constants.UNKNOWN)
        tool: str = self._context.get().get(constants.CONTEXT_KEY_TOOL, constants.UNKNOWN)
        log_message: str = record.getMessage()
        stack_trace: str = StackTracingFormatter.get_stack_trace(record=record)
        output: io.StringIO = io.StringIO()
        writer: Any = csv.writer(output, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [
                log_time,
                activity,
                command,
                phase,
                module,
                file,
                tool,
                log_message,
                stack_trace
            ]
        )
        result: str = output.getvalue().strip()
        return result

