# ruff: noqa: S301
import pickle
from typing import Any, Generic, TypeVar, get_origin

from typedpath.base import PathLikeLike, TypedFile

T = TypeVar("T")


class PickleFile(TypedFile, Generic[T]):
    """A file containing pickled data."""

    default_suffix = ".pickle"

    def __init__(self, path: PathLikeLike, value_type: type[T]) -> None:
        super().__init__(path)

        self._value_type = value_type

    def write(self, data: T, **kwargs: Any) -> None:
        """
        Sets the contents of this file.

        :param kwargs: Key-word arguments to pass to `pickle.dump`.
        """
        with open(self.write_path(), "wb") as fp:
            pickle.dump(data, fp, **kwargs)

    def read(self, **kwargs: Any) -> T:
        """
        Gets the contents of this file.

        :param kwargs: Key-word arguments to pass to `pickle.load`.
        """
        with open(self.read_path(), "rb") as fp:
            result: T = pickle.load(fp, **kwargs)
            origin = get_origin(self._value_type)
            if origin is not None:
                assert isinstance(result, origin)
            return result
