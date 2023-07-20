import json
from typing import Any, Mapping, Sequence

from typedpath.base import PathLikeLike, TypedFile

ReadOnlyJSON = (
    int | float | bool | str | None | Sequence["ReadOnlyJSON"] | Mapping[str, "ReadOnlyJSON"]
)
JSON = int | float | bool | str | None | list["JSON"] | dict[str, "JSON"]


class JSONFile(TypedFile):
    """A file containing JSON."""

    default_suffix = ".json"

    def __init__(self, path: PathLikeLike, *, encoding: str = "utf-8") -> None:
        super().__init__(path)

        self._encoding = encoding

    def write(self, data: ReadOnlyJSON, **kwargs: Any) -> None:
        """
        Sets the contents of this file.

        :param kwargs: Key-word arguments to pass to `json.dump`.
        """
        with open(self.write_path(), "wt", encoding=self._encoding) as fp:
            json.dump(data, fp, **kwargs)

    def read(self, **kwargs: Any) -> JSON:
        """
        Gets the contents of this file.

        :param kwargs: Key-word arguments to pass to `json.load`.
        """
        with open(self.read_path(), "rt", encoding=self._encoding) as fp:
            return json.load(fp, **kwargs)  # type: ignore[no-any-return]
