import pickle
from typing import Any, Generic, Type, TypeVar, get_origin

from typedpath.base import PathLikeLike, TypedFile

T = TypeVar("T")


class PickleFile(TypedFile, Generic[T]):
    default_suffix = ".pickle"

    def __init__(self, path: PathLikeLike, value_type: Type[T]) -> None:
        super().__init__(path)

        self._value_type = value_type

    def write(self, data: T, **kwargs: Any) -> None:
        with open(self.write_path(), "wb") as fp:
            pickle.dump(data, fp, **kwargs)

    def read(self, **kwargs: Any) -> T:
        with open(self.read_path(), "rb") as fp:
            result: T = pickle.load(fp, **kwargs)
            origin = get_origin(self._value_type)
            if origin is not None:
                assert isinstance(result, origin)
            return result
