from pydantic import BaseModel


class Entrant(BaseModel):
    key: int
    name: str
    number: str | None = None
    event_key: int