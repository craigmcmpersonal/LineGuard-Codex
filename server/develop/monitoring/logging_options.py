import logging


class LoggingOptions:
    file: str|None = None
    handlers: list[logging.Handler]|None = None
    level: int = logging.INFO
