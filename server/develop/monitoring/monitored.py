import logging
from argparse import Namespace
from typing import ClassVar

from opentelemetry import trace
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler, LogRecordProcessor
from opentelemetry.sdk._logs._internal.export import LogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter, AzureMonitorTraceExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter

from develop.monitoring.base_monitored import BaseMonitored, CONTEXT
from develop.monitoring.contextualizing_log_filter import ContextualizingLogFilter
from develop.monitoring.logging_options import LoggingOptions
from develop.monitoring.noise_log_filter import NoiseLogFilter


class Monitored(BaseMonitored):
    _KEY_OPEN_TELEMETRY_SERVICE_NAME: ClassVar[str] = "service.name"

    def __init__(self, arguments: Namespace):
        Monitored._configure_tracing(arguments=arguments)
        logging_options: LoggingOptions = Monitored._configure_logging(arguments=arguments)
        super().__init__(logging_options=logging_options)

    @staticmethod
    def _configure_logging(arguments: Namespace) -> LoggingOptions:
        result: LoggingOptions = LoggingOptions()
        result.level = BaseMonitored.NAMED_LOG_LEVELS[arguments.log_level]
        if arguments.azure_insights:
            provider: LoggerProvider = LoggerProvider()
            set_logger_provider(provider)
            exporter: LogExporter = AzureMonitorLogExporter.from_connection_string(arguments.azure_insights)
            processor: LogRecordProcessor = BatchLogRecordProcessor(exporter)
            provider.add_log_record_processor(processor)
            handler: logging.Handler = LoggingHandler(level=result.level, logger_provider=provider)
            noise_filter: logging.Filter = NoiseLogFilter()
            handler.addFilter(noise_filter)
            contextualizing_filter: logging.Filter = ContextualizingLogFilter(context=CONTEXT)
            handler.addFilter(contextualizing_filter)
            result.handlers = [handler]
        return result

    @staticmethod
    def _configure_tracing(arguments: Namespace):
        if arguments.azure_insights:
            provider: TracerProvider = TracerProvider(
                resource=Resource.create(
                    {
                        Monitored._KEY_OPEN_TELEMETRY_SERVICE_NAME: arguments.path
                    }
                )
            )
            trace.set_tracer_provider(provider)
            exporter: SpanExporter = AzureMonitorTraceExporter.from_connection_string(arguments.azure_insights)
            provider.add_span_processor(BatchSpanProcessor(exporter))
