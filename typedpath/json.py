import json
from collections.abc import Mapping, Sequence
from typing import Any, TypeAlias

from typedpath.base import PathLikeLike, TypedFile

JSONPrimitive: TypeAlias = int | float | bool | str | None
JSON = JSONPrimitive | Sequence["JSON"] | Mapping[str, "JSON"]
MutableJSON = JSONPrimitive | list["MutableJSON"] | dict[str, "MutableJSON"]


class JSONFile(TypedFile):
    """A file containing JSON."""

    default_suffix = ".json"

    def __init__(self, path: PathLikeLike, *, encoding: str = "utf-8") -> None:
        super().__init__(path)

        self._encoding = encoding

    def write(self, data: JSON, **kwargs: Any) -> None:
        """
        Sets the contents of this file.

        :param kwargs: Key-word arguments to pass to `json.dump`.
        """
        with open(self.write_path(), "wt", encoding=self._encoding) as fp:
            json.dump(data, fp, **kwargs)

    def read(self, **kwargs: Any) -> MutableJSON:
        """
        Gets the contents of this file.

        :param kwargs: Key-word arguments to pass to `json.load`.
        """
        with open(self.read_path(), "rt", encoding=self._encoding) as fp:
            return json.load(fp, **kwargs)  # type: ignore[no-any-return]
