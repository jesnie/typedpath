from typing import Any, Generic, TypeVar

from typedpath import PathLikeLike, TypedDir, TypedFile

T = TypeVar("T")
U = TypeVar("U")


class TestFile(TypedFile):
    default_suffix = ".test"

    def __init__(self, path: PathLikeLike, **kwargs: Any) -> None:
        super().__init__(path)
        self.kwargs = kwargs

    def write(self, data: str) -> int:
        return self.write_path().write_text(data, encoding="utf-8")

    def read(self) -> str:
        return self.read_path().read_text(encoding="utf-8")


class TestGenericDir(TypedDir, Generic[T, U]):
    default_suffix = ""

    def __init__(self, path: PathLikeLike, t: type[T], u: type[U], **kwargs: Any) -> None:
        super().__init__(path)
        self.t = t
        self.u = u
        self.kwargs = kwargs

    @property
    def file(self) -> TestFile:
        return TestFile(self.pretty_path() / "file.test")
