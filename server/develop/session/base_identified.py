from __future__ import annotations

from pathlib import Path
from typing import Any, Union

from develop.data_model import DataModel

class BaseIdentified(DataModel):
    def __init__(
            self,
            /,
            identifier: str = None,
            path: Union[str, Path] = None,
            data: dict[str, Any] = None,
            **kwargs: Any
    ):
        if identifier is not None:
            super().__init__(path, data, **kwargs)
        else:
            super().__init__(identifier=identifier)

    identifier: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BaseIdentified):
            return NotImplemented
        elif not self.identifier:
            return False
        elif not other.identifier:
            return False
        elif self.identifier == other.identifier:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.identifier}"

