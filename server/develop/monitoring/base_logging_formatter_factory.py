import logging


class BaseLoggingFormatterFactory:
    def __init__(self):
        self.logging_format = "[%(asctime)s] [%(levelname)s]: %(message)s"

    def create_formatter(self) -> logging.Formatter:
        ...