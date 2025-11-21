import json
from pathlib import Path
from typing import Any, Union, TextIO
import yaml

from pydantic import BaseModel

from develop import constants


class DataModel(BaseModel):
    def __init__(self, /, path: Union[str, Path] = None, data: dict[str, Any] = None, **kwargs: Any):

        exception_parameters: str = "Provide only one of 'path', 'data', or keyword arguments."

        if (path is not None) + (data is not None) + (bool(
                kwargs
        )) > 1:
            raise ValueError(
                exception_parameters
            )
        elif path is not None:
            with open(path, constants.FILE_MODE_READ, encoding=constants.ENCODING_JSON) as file:
                file: TextIO
                parsed: dict[str, Any] = json.load(file)
                super().__init__(**parsed)
        elif data is not None:
            super().__init__(**data)
        else:
            super().__init__(**kwargs)

    def model_dump_yaml(self) -> str:
        data: dict[str, Any] = self.model_dump()
        result: str = yaml.dump(data, indent=constants.INDENT_JSON, sort_keys=False)
        return result



