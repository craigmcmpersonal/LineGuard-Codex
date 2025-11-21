from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Union

from pydantic import Field

from develop.session.base_identified import BaseIdentified
from develop.session.session_state_key import SessionStateKey
from develop.session.user import User
from develop.utility import now


class Session(BaseIdentified):
    def __init__(
            self,
            /,
            user: User = None,
            identifier: str = None,
            path: Union[str, Path] = None,
            data: dict[str, Any] = None,
            **kwargs: Any
    ):
        exception_parameters: str = \
            "Provide either both 'user' and 'identifier', or only one of 'path', 'data', or keyword arguments."

        count_native_arguments: int = (user is not None) + (identifier is not None)
        if 0 == count_native_arguments:
            super().__init__(path, data, **kwargs)
        elif 1 == count_native_arguments:
            raise ValueError(exception_parameters)
        else:
            super().__init__(user=user, identifier=identifier)

    identifier: str
    description: str|None = Field(default=None)
    state: dict[str, Any] = Field(default={})
    time_created: str|None = Field(default=now())
    time_last_read: str | None = Field(default=None)
    time_last_updated: str | None = Field(default=None)
    user: User

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Session):
            return NotImplemented
        if not super().__eq__(other):
            return False
        elif not self.user:
            return False
        elif not other.user:
            return False
        elif self.user == other.user:
            return True
        else:
            return False

    def __str__(self):
        states: str = None if self.state is None else self.state.get(SessionStateKey.STATES)
        return f"{self.identifier}.{self.user}->{states}"

    def clone(self) -> Session:
        data: dict[str, Any] = self.model_dump()
        result: Session = Session(data=data)
        return result

    @classmethod
    def create(cls, user: User) -> Session:
        session_unique_identifier: uuid.UUID = uuid.uuid4()
        session_identifier: str = str(session_unique_identifier)
        result: Session = Session(user=user, identifier=session_identifier)
        return result

    def describe(self, label: str | None = None):
        if self.description is None and label:
            self.description = label

    def on_creation(self):
        if not self.time_created:
            self.time_created = now()

    def on_retrieval(self):
        self.time_last_read = now()

    def on_update(self):
        self.time_last_updated = now()

    def remove_state(self, key_or_keys: str | list[str]):
        if isinstance(key_or_keys, str) and self.state.get(key_or_keys):
            del self.state[key_or_keys]
        elif isinstance(key_or_keys, list):
            for current_key in key_or_keys:
                current_key: str
                self.remove_state(key_or_keys=current_key)
