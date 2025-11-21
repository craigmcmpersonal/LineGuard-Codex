from typing import Iterator

from develop.session.session import Session
from develop.session.user import User


class BaseSessionStore:
    def create(self, user: User) -> Session:
        ...

    def delete(self, session_identifier: str):
        ...

    def enumerate(self) -> Iterator[Session]:
        ...

    def find(self, user: User) -> list[Session]:
        ...

    def store(self, session: Session, etag: str|None = None) -> tuple[str, Session]:
        ...

    def try_get(self, session_identifier: str) -> Session|None:
        ...

