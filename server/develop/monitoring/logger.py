from __future__ import annotations

import logging
import json
import traceback
from typing import ClassVar, Any, Optional

import develop.constants as constants
from develop.monitoring.base_monitored import CONTEXT
from develop.monitoring.stack_tracing_formatter import StackTracingFormatter


class Logger(logging.LoggerAdapter):
    _INITIALIZED: ClassVar[bool] = False
    _KEY_EXTRA: ClassVar[str] = "extra"
    _KEY_STACK: ClassVar[str] = "stack"
    _KEY_USER: ClassVar[str] = "user"
    _SINGLETON: ClassVar[Optional[logging.LoggerAdapter]] = None

    def __init__(self):
        if not self.__class__._INITIALIZED:
            logger: logging.Logger = logging.getLogger()
            super().__init__(logger)
            self.__class__._INITIALIZED = True

    def __new__(cls, *args, **kwargs):
        if cls._SINGLETON is None:
            cls._SINGLETON = super().__new__(cls)
        return cls._SINGLETON

    @classmethod
    def instance(cls) -> logging.LoggerAdapter:
        if cls._SINGLETON is None:
            cls._SINGLETON = cls()
        return cls._SINGLETON

    def process(self, msg, kwargs):
        session: Any | None = CONTEXT.get().get(constants.CONTEXT_KEY_SESSION, None)
        stack: list[str] = StackTracingFormatter.filter_stack(get_stack_function=traceback.format_stack)
        data: dict[str,Any] = {
            Logger._KEY_STACK: json.dumps(stack),
            constants.CONTEXT_KEY_ACTIVITY: CONTEXT.get().get(constants.CONTEXT_KEY_ACTIVITY, constants.UNKNOWN),
            constants.CONTEXT_KEY_SESSION: session.identifier if session else constants.UNKNOWN,
            Logger._KEY_USER: session.user.identifier if session and session.user else constants.UNKNOWN,
            constants.CONTEXT_KEY_PHASE: CONTEXT.get().get(constants.CONTEXT_KEY_PHASE, constants.UNKNOWN),
            constants.CONTEXT_KEY_FILE: CONTEXT.get().get(constants.CONTEXT_KEY_FILE, constants.UNKNOWN),
            constants.CONTEXT_KEY_TOOL: CONTEXT.get().get(constants.CONTEXT_KEY_TOOL, constants.UNKNOWN),
            constants.CONTEXT_KEY_COMMAND: CONTEXT.get().get(constants.CONTEXT_KEY_COMMAND, constants.UNKNOWN),
            constants.CONTEXT_KEY_MODULE: CONTEXT.get().get(constants.CONTEXT_KEY_MODULE, constants.UNKNOWN)
        }
        if (dictionary := kwargs.get(Logger._KEY_EXTRA, None)) is None or not isinstance(dictionary, dict):
            kwargs[Logger._KEY_EXTRA] = data
        else:
            dictionary: dict
            dictionary.update(kwargs)
        return msg, kwargs