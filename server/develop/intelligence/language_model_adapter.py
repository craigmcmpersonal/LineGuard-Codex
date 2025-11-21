from __future__ import annotations

from typing import Optional, ClassVar, Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

import develop.constants as constants
from develop import environment
from develop.monitoring.logger import Logger
from develop.intelligence.callback_handler import CallbackHandler
from develop.intelligence.chat_model_adapter import ChatModelAdapter
from develop.intelligence.base_language_model_adapter import BaseLanguageModelAdapter


class LanguageModelAdapter:
    _INITIALIZED: ClassVar[bool] = False
    _KEY_MODEL_NAME: ClassVar[str] = "model_name"
    _KEY_TOKEN_USAGE: ClassVar[str] = "usage_metadata"
    _KEY_TOTAL_TOKENS: ClassVar[str] = "total_tokens"
    _SINGLETON: ClassVar[Optional[LanguageModelAdapter]] = None

    class _Implementation(BaseLanguageModelAdapter):
        def __init__(
                self,
                provider: str,
                model_chat: ChatModelAdapter,
                input_limit: int,
                model_reason: ChatModelAdapter|None=None,
                response_acceptance_function: Callable[[BaseMessage], bool]=None,
                usage_monitoring_function: Callable[[BaseMessage, str], None] = None,
        ):
            if not LanguageModelAdapter._INITIALIZED:
                super().__init__(
                    provider=provider,
                    model_chat=model_chat,
                    input_limit=input_limit,
                    model_reason=model_reason,
                    response_acceptance_function=response_acceptance_function,
                    usage_monitoring_function=usage_monitoring_function

                )
                LanguageModelAdapter._INITIALIZED = True

    def __new__(cls, *args, **kwargs):
        if cls._SINGLETON is None:
            cls._SINGLETON = super().__new__(cls)
            logging_handler: CallbackHandler = CallbackHandler()
            if (openai_key := environment.try_get_value(environment.KEY_CHAT_KEY)) is not None:
                openai_key: SecretStr
                model_version_chat: str = environment.try_get_value(environment.KEY_CHAT_MODEL) or \
                                          constants.LANGUAGE_MODEL_OPEN_AI_CHAT_DEFAULT
                model_chat: BaseChatModel = ChatOpenAI(
                    model=model_version_chat,
                    temperature=constants.OPEN_AI_TEMPERATURE_DEFAULT \
                        if model_version_chat != constants.LANGUAGE_MODEL_OPEN_AI_O3 \
                        else constants.OPEN_AI_TEMPERATURE_03,
                    api_key=openai_key,
                    store=True,
                    callbacks=[logging_handler],
                    timeout=constants.OPEN_AI_TIMEOUT_IN_SECONDS
                )
                model_adapter_chat: ChatModelAdapter = ChatModelAdapter(
                    model=model_chat,
                    version=model_version_chat
                )
                cls._SINGLETON.model = LanguageModelAdapter._Implementation(
                    provider=constants.LANGUAGE_MODEL_PROVIDER_OPEN_AI,
                    model_chat=model_adapter_chat,
                    input_limit=constants.LANGUAGE_MODEL_OPEN_AI_INPUT_LIMIT,
                    response_acceptance_function=LanguageModelAdapter._accept_open_ai_response,
                    usage_monitoring_function=LanguageModelAdapter._monitor_open_ai_usage
                )
            else:
                raise RuntimeError()
        return cls._SINGLETON

    @staticmethod
    def _accept_open_ai_response(message: BaseMessage) -> bool:
        if message is None:
            return False
        elif message.response_metadata is None:
            return False
        elif (finish_reason := message.response_metadata.get(constants.FINISH_REASON_KEY_OPEN_AI, None)) is None:
            return False
        elif constants.FINISH_REASON_LENGTH in finish_reason:
            return False
        elif constants.FINISH_REASON_CONTENT_FILTER in finish_reason:
            return False
        else:
            return True

    @staticmethod
    def _monitor_local_model_usage(message: BaseMessage, model_version: str):
        if message is None:
            return
        elif not hasattr(message,LanguageModelAdapter. _KEY_TOKEN_USAGE):
            return
        elif  message.usage_metadata is None:
            return
        elif message.response_metadata is None:
            return
        elif (total_tokens := message.usage_metadata.get(LanguageModelAdapter._KEY_TOTAL_TOKENS, None)) is None:
            return
        else:
            effective_model_version = message.response_metadata.get(
                LanguageModelAdapter._KEY_MODEL_NAME,
                None
            ) or model_version
            total_tokens: int
            Logger.instance().info(f"${effective_model_version}: {total_tokens}")

    @staticmethod
    def _monitor_open_ai_usage(message: BaseMessage, model_version: str):
        if message is None:
            return
        elif message.response_metadata is None:
            return
        elif (token_usage := message.response_metadata.get(LanguageModelAdapter._KEY_TOKEN_USAGE, None)) is None:
            return
        elif (total_tokens := token_usage.get(LanguageModelAdapter._KEY_TOTAL_TOKENS, None)) is None:
            return
        else:
            effective_model_version = message.response_metadata.get(
                LanguageModelAdapter._KEY_MODEL_NAME,
                None
            ) or model_version
            total_tokens: int
            Logger.instance().info(f"${effective_model_version}: {total_tokens}")

    @classmethod
    def instance(cls) -> LanguageModelAdapter:
        if cls._SINGLETON is None:
            cls._SINGLETON = cls()
        return cls._SINGLETON
