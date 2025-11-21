import inspect

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from typing import Any, Dict, List, ClassVar

import develop.constants as constants
from develop.monitoring.logger import Logger


class CallbackHandler(BaseCallbackHandler):
    _KEY_NAME: ClassVar[str] = "name"
    _KEY_MODEL_NAME: ClassVar[str] = _KEY_NAME
    _KEY_TOOL_NAME: ClassVar[str] = _KEY_NAME

    def on_error(self, error: BaseException, **kwargs: Any):
        method: str = inspect.currentframe().f_code.co_name
        Logger.instance().error(f"{method}{constants.LINE_BREAK_NEW_LINE}{error}")

    def on_llm_end(self, response: LLMResult, **kwargs: Any):
        method: str = inspect.currentframe().f_code.co_name
        Logger.instance().info(f"{method}{constants.LINE_BREAK_NEW_LINE}{response}")

    def on_llm_new_token(self, token: str, **kwargs: Any):
        method: str = inspect.currentframe().f_code.co_name
        Logger.instance().info(f"{method} {token}")

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any):
        method: str = inspect.currentframe().f_code.co_name
        model: str = serialized.get(CallbackHandler._KEY_MODEL_NAME)
        Logger.instance().info(f"{method} {model}{constants.LINE_BREAK_NEW_LINE}{prompts}")

    def on_tool_end(self, output: str, **kwargs: Any):
        method: str = inspect.currentframe().f_code.co_name
        Logger.instance().info(f"{method}{constants.LINE_BREAK_NEW_LINE}{output}")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any):
        method: str = inspect.currentframe().f_code.co_name
        tool: str = serialized.get(CallbackHandler._KEY_MODEL_NAME)
        Logger.instance().info(f"{method} {tool}{constants.LINE_BREAK_NEW_LINE}{input_str}")

