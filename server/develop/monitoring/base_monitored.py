import contextvars
import logging
import sys
import threading

import time

from pathlib import Path
from typing import ClassVar

from develop import constants
from develop.monitoring.comma_separated_values_logging_formatter_factory import \
    CommaSeparatedValuesLoggingFormatterFactory
from develop.monitoring.compressing_timed_rotating_log_file_handler import CompressingTimedRotatingLogFileHandler
from develop.monitoring.noise_log_filter import NoiseLogFilter
from develop.monitoring.service_logging_formatter_factory import ServiceLoggingFormatterFactory
from develop.monitoring.logging_options import LoggingOptions

CONTEXT: contextvars.ContextVar = contextvars.ContextVar(
    constants.CONTEXT_VARIABLE_CONTEXT,
    default={}
)

class BaseMonitored:
    _CURRENT_LOG_LEVEL: ClassVar[int | None] = None
    _CURRENT_LOG_FILE: ClassVar[str | None] = None
    _BASE_MONITORED_LOCK: ClassVar[threading.RLock] = threading.RLock()
    _DEFAULT_LOGGING_FORMATTER: ClassVar[logging.Formatter] = \
        CommaSeparatedValuesLoggingFormatterFactory(context=CONTEXT).create_formatter()
    _FILE_LOGGING_FORMATTER: ClassVar[logging.Formatter] = ServiceLoggingFormatterFactory(CONTEXT).create_formatter()

    NAMED_LOG_LEVELS: ClassVar[dict[str, int]] = {
        name: level for name, level in vars(
            logging
        ).items() if isinstance(
            level,
            int
        ) and logging.CRITICAL >= level >= logging.DEBUG
    }
    LOG_LEVELS: ClassVar[dict[str,int]] = {
        level: name
        for level, name in NAMED_LOG_LEVELS.items()
    }
    LOG_LEVEL_NAMES: ClassVar[list[str]] = [
        item for item in NAMED_LOG_LEVELS.keys()
    ]
    ALL_LOG_LEVEL_NAMES: ClassVar[str] = constants.SEPARATOR_COMMA_SPACE.join(LOG_LEVEL_NAMES)

    def __init__(self, logging_options: LoggingOptions|None = None):
        effective_logging_options = BaseMonitored._calculate_logging_options(logging_options=logging_options)
        with BaseMonitored._BASE_MONITORED_LOCK:
            if BaseMonitored._CURRENT_LOG_LEVEL is None:
                BaseMonitored._initialize_logging(options=effective_logging_options)
            else:
                if not BaseMonitored._CURRENT_LOG_FILE and effective_logging_options.file:
                    file_handler: logging.Handler = self._construct_file_handler(
                        logging_options=effective_logging_options
                    )
                    logging.getLogger().addHandler(file_handler)
                    file_handler.setFormatter(BaseMonitored._FILE_LOGGING_FORMATTER)
                for handler in effective_logging_options.handlers or []:
                    handler: logging.Handler
                    if handler not in logging.getLogger().handlers:
                        logging.getLogger().addHandler(handler)

    @staticmethod
    def _calculate_logging_options(logging_options: LoggingOptions|None = None) -> LoggingOptions:
        result: LoggingOptions = LoggingOptions()
        if logging_options:
            if logging_options.level:
                result.level = logging_options.level
            if logging_options.file:
                result.file = logging_options.file
            if logging_options.handlers:
                result.handlers = logging_options.handlers
        return result

    @staticmethod
    def _construct_file_handler(logging_options: LoggingOptions|None = None) -> logging.Handler:
        file_path: Path = Path(
            logging_options.file
        )
        extension: str = constants.EMPTY_STRING if file_path.suffix == constants.EXTENSION_COMMA_SEPARATED_VALUES else \
            constants.EXTENSION_COMMA_SEPARATED_VALUES
        file_name: str = str(file_path) + extension
        result: logging.Handler = CompressingTimedRotatingLogFileHandler(
            filename=file_name,
            when=constants.LOG_FILE_ROTATION_TIME_MIDNIGHT,
            interval=constants.LOG_FILE_ROTATION_TIME_INTERVAL_DAILY,
            backupCount=constants.LOG_FILE_MAXIMUM_BACKUP_COUNT,
            encoding=constants.ENCODING_UTF8,
            utc=True
        )
        return result

    @staticmethod
    def _initialize_logging(options: LoggingOptions) :
        console_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(BaseMonitored._DEFAULT_LOGGING_FORMATTER)
        handlers: list[logging.Handler] = [
            console_handler
        ]

        if options.file:
            file_handler: logging.Handler = BaseMonitored._construct_file_handler(logging_options=options)
            handlers.append(file_handler)
        if options.handlers:
            handlers.extend(options.handlers)

        logger: logging.Logger = logging.getLogger()
        noise_log_filter: logging.Filter = NoiseLogFilter()
        logger.addFilter(noise_log_filter)
        logger.setLevel(options.level)
        BaseMonitored._CURRENT_LOG_LEVEL = options.level
        logging.Formatter.converter = time.gmtime
        for handler in handlers:
            handler.addFilter(noise_log_filter)
            logger.addHandler(handler)
            if isinstance(handler, logging.FileHandler):
                handler.setFormatter(BaseMonitored._FILE_LOGGING_FORMATTER)
        if options.file:
            BaseMonitored._CURRENT_LOG_FILE = options.file








