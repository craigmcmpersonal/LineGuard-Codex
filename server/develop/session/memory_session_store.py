import uuid
from typing import Iterator

import develop.constants as constants
from develop.session.base_session_store import BaseSessionStore
from develop.session.session import Session
from develop.session.user import User


class MemorySessionStore(BaseSessionStore):
    def __init__(self):
        self._store: dict[str, Session] = {}

    def create(self, user: User) -> Session:
        unique_identifier: uuid.UUID = uuid.uuid4()
        session_identifier: str = str(
            unique_identifier
        )
        session: Session = Session(
            user=user,
            identifier=session_identifier
        )
        session.on_creation()
        _, result = self.store(
            session=session
        )
        return result

    def delete(self, session_identifier: str):
        if self._store.get(session_identifier):
            del self._store[session_identifier]

    def enumerate(self) -> Iterator[Session]:
        for item in self._store.values():
            yield item

    def find(self, user: User) -> list[Session]:
        results: list[Session] = [
            item
            for item in self._store.values()
            if item.user == user
        ]
        return results

    def store(self, session: Session, etag: str|None = None) -> tuple[str, Session]:
        session.on_update()
        self._store[session.identifier] = session
        return constants.EMPTY_STRING, session

    def try_get(self, session_identifier: str) -> Session|None:
        result: Session|None = self._store.get(
            session_identifier
        )
        if result:
            result.on_creation()
        return result
