from typing import Callable

from langchain_core.messages import BaseMessage

from develop.intelligence.chat_model_adapter import ChatModelAdapter


class BaseLanguageModelAdapter:
    def __init__(
            self,
            provider: str,
            model_chat: ChatModelAdapter,
            input_limit: int,
            model_reason: ChatModelAdapter | None=None,
            response_acceptance_function: Callable[[BaseMessage], bool]=None,
            usage_monitoring_function: Callable[[BaseMessage, str], None]=None
    ):
        self.provider = provider
        self.model_chat: ChatModelAdapter = model_chat
        self.model_reason: ChatModelAdapter = model_reason or model_chat
        self.input_limit: int = input_limit
        self.response_validation_function: Callable[[BaseMessage], bool] = response_acceptance_function
        self.usage_monitoring_function: Callable[[BaseMessage, str], None] = usage_monitoring_function