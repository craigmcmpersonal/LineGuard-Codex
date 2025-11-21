from __future__ import annotations

from dataclasses import field
from pathlib import Path
from typing import Any, Union

from develop.session.base_identified import BaseIdentified


class User(BaseIdentified):
    def __init__(
            self,
            /,
            identifier: str = None,
            name: str = None,
            contact: str|None = None,
            path: Union[str, Path] = None,
            data: dict[str, Any] = None,
            **kwargs: Any
    ):
        exception_parameters: str = \
            "Provide either both 'name' and 'identifier', or only one of 'path', 'data', or keyword arguments."

        count_native_arguments: int = (name is not None) + (identifier is not None)
        if 0 == count_native_arguments:
            super().__init__(path, data, **kwargs)
        elif 1 == count_native_arguments:
            raise ValueError(exception_parameters)
        else:
            super().__init__(identifier=identifier, name=name, contact=contact)

    contact: str|None = field(default=None)
    name: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        if not super().__eq__(other):
            return False
        elif not self.name:
            return False
        elif not other.name:
            return False
        elif self.name == other.name:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.identifier}: {self.name} @ {self.contact}"

