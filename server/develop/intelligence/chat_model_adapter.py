from langchain_core.language_models import BaseChatModel


class ChatModelAdapter:
    def __init__(self, model: BaseChatModel, version: str):
        self.model: BaseChatModel = model
        self.version: str = version