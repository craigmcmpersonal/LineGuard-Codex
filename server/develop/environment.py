import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()

KEY_CHAT_KEY: tuple[str,str|None] = ("CHAT_KEY",None)
KEY_CHAT_MODEL: tuple[str,str|None] = ("CHAT_MODEL_BASELINE","gpt-5.1")
KEY_POSTGRES_HOST: tuple[str,str|None] = ("POSTGRES_HOST","localhost")
KEY_POSTGRES_PORT: tuple[str,int|None] = ("POSTGRES_PORT",5432)
KEY_POSTGRES_DATABASE: tuple[str,str|None] = ("POSTGRES_DATABASE","lineguard")
KEY_POSTGRES_USER: tuple[str,str|None] = ("POSTGRES_USER",None)
KEY_POSTGRES_PASSWORD: tuple[str,str|None] = ("POSTGRES_PASSWORD",None)
KEY_WEB_SERVICE_PORT: tuple[str,int|None] = ("WEB_SERVICE_PORT",5000)

def try_get_value(key: tuple[str,Any|None]) -> Any:
    result: Any|None = os.environ.get(key[0], key[1])
    return result

