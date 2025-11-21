import json
import logging
import contextvars
import traceback
from datetime import datetime, timezone
from typing import ClassVar

import develop.constants as constants
from develop.monitoring.stack_tracing_formatter import StackTracingFormatter
from develop.session.session import Session
from develop.session.user import User


class ContextualizingLogFilter(logging.Filter):
    _ATTRIBUTE_COMMAND: ClassVar[str] = "command"
    _ATTRIBUTE_FILE: ClassVar[str] = "file"
    _ATTRIBUTE_MODULE: ClassVar[str] = "module"
    _ATTRIBUTE_PHASE: ClassVar[str] = "phase"
    _ATTRIBUTE_SESSION: ClassVar[str] = "session"
    _ATTRIBUTE_STACK: ClassVar[str] = "stack"
    _ATTRIBUTE_TIME: ClassVar[str] = "time"
    _ATTRIBUTE_TOOL: ClassVar[str] = "tool"
    _ATTRIBUTE_USER: ClassVar[str] = "user"
    _MAPPING: ClassVar[dict[str,str]] = {
        constants.CONTEXT_KEY_COMMAND: _ATTRIBUTE_COMMAND,
        constants.CONTEXT_KEY_FILE: _ATTRIBUTE_FILE,
        constants.CONTEXT_KEY_MODULE: _ATTRIBUTE_MODULE,
        constants.CONTEXT_KEY_PHASE: _ATTRIBUTE_PHASE,
        constants.CONTEXT_KEY_TOOL: _ATTRIBUTE_TOOL
    }

    def __init__(self, context: contextvars.ContextVar):
        super().__init__()
        self._context: contextvars.ContextVar = context

    def _add_context(self, record: logging.LogRecord):
        for context_key, attribute in self._MAPPING.items():
            if (value := self._context.get().get(
                context_key,
                None
            )) is not None and getattr(
                record,
                attribute, None
            ) is None:
                value: str
                setattr(record, attribute, value)

    def _add_session(self, record: logging.LogRecord):
        if (session := self._context.get().get(
            constants.CONTEXT_KEY_SESSION,
            None
        )) is not None:
            session: Session
            if session.identifier is not None and getattr(
                record,
                ContextualizingLogFilter._ATTRIBUTE_SESSION,
                None
            ) is None:
                setattr(record, ContextualizingLogFilter._ATTRIBUTE_SESSION, session.identifier)
            if (user := session.user) is not None and user.identifier is not None and getattr(
                record,
                ContextualizingLogFilter._ATTRIBUTE_USER,
                None
            ) is None:
                user: User
                setattr(record, ContextualizingLogFilter._ATTRIBUTE_USER, user.identifier)

    @staticmethod
    def _add_stack(record: logging.LogRecord):
        if (stack := StackTracingFormatter.filter_stack(
            get_stack_function=traceback.format_stack
        )) and (getattr(
            record,
            ContextualizingLogFilter._ATTRIBUTE_STACK,
            None
        ) is None):
            stack: list[str]
            value: str = json.dumps(stack)
            setattr(record, ContextualizingLogFilter._ATTRIBUTE_STACK, value)

    @staticmethod
    def _add_time(record: logging.LogRecord):
        if (getattr(
            record,
            ContextualizingLogFilter._ATTRIBUTE_TIME,
            None
        ) is None):
            value: float = datetime.now(timezone.utc).timestamp()
            setattr(record, ContextualizingLogFilter._ATTRIBUTE_TIME, value)

    def filter(self, record: logging.LogRecord) -> bool:
        self._add_time(record)
        self._add_session(record)
        ContextualizingLogFilter._add_stack(record)
        self._add_context(record)
        return True