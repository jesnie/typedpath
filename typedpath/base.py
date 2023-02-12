from os import PathLike, fspath
from pathlib import Path
from typing import Generic, TypeAlias

K = TypeVar("K")
PV = TypeVar("PV", bound=TypedPath)


PathLikeLike: TypeAlias = PathLike | str | bytes


class TypedPath:
    def __init__(path: PathLikeLike) -> None:
        self._path = Path(fspath(path))

    def __str__(self) -> str:
        return str(self._path)


class TypedDir(TypedPath):
    pass


class TypedFile(TypedPath):
    def read_path(self) -> Path:
        assert self._path.isfile()
        return self._path

    def write_path(self) -> Path:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        return self._path

    def pretty_path(self) -> Path:
        return self._path


class TextFile(TypedFile):
    def write(self, content: str) -> None:
        self.write_path().write_text(content)

    def read(self) -> str:
        return self.read_path().read_text()


class BytesFile(TypedFile):
    def write(self, content: bytes) -> None:
        self.write_path().write_bytes(content)

    def read(self) -> bytes:
        return self.read_path().read_bytes()
