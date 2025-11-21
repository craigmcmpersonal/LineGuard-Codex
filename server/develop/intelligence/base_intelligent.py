from develop.intelligence.base_language_model_adapter import BaseLanguageModelAdapter
from develop.monitoring.base_monitored import BaseMonitored
from develop.monitoring.logging_options import LoggingOptions


class BaseIntelligent(BaseMonitored):
    def __init__(self, language_model: BaseLanguageModelAdapter, logging_options: LoggingOptions|None = None):
        super().__init__(logging_options=logging_options)
        self.language_model: BaseLanguageModelAdapter = language_model