import contextvars
import logging
import csv
import io
from typing import Any

import develop.constants as constants
from develop.monitoring.stack_tracing_formatter import StackTracingFormatter

class ServiceLoggingFormatter(StackTracingFormatter):
    def __init__(self, context: contextvars.ContextVar):
        self._context: contextvars.ContextVar = context
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        log_time: str = self.formatTime(record=record)
        log_message: str = record.getMessage()

        activity_identifier: str = self._context.get().get(constants.CONTEXT_KEY_ACTIVITY, constants.UNKNOWN)
        session: Any|None = self._context.get().get(constants.CONTEXT_KEY_SESSION, None)
        session_identifier: str = session.identifier if session else constants.UNKNOWN
        user_identifier: str = session.user.identifier if session and session.user else constants.UNKNOWN
        user_name: str = session.user.name if session and session.user else constants.UNKNOWN
        stack_trace: str = StackTracingFormatter.get_stack_trace(record=record)

        output: io.StringIO = io.StringIO()
        writer: Any = csv.writer(output, quoting=csv.QUOTE_ALL)
        writer.writerow(
            [log_time, activity_identifier, session_identifier, user_identifier, user_name, log_message, stack_trace]
        )

        result: str = output.getvalue().strip()
        return result

