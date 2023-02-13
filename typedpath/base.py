from os import PathLike
from pathlib import Path
from typing import TypeAlias, TypeVar

K = TypeVar("K")
PV = TypeVar("PV", bound="TypedPath")


PathLikeLike: TypeAlias = PathLike[str] | str


class TypedPath:
    def __init__(self, path: PathLikeLike) -> None:
        self._path = Path(path)

    def __str__(self) -> str:
        return str(self._path)


class TypedDir(TypedPath):
    pass


class TypedFile(TypedPath):
    def read_path(self) -> Path:
        assert self._path.is_file()
        return self._path

    def write_path(self) -> Path:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        return self._path

    def pretty_path(self) -> Path:
        return self._path


class TextFile(TypedFile):
    def write(
        self,
        data: str,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> int:
        return self.write_path().write_text(data, encoding=encoding, errors=errors, newline=newline)

    def read(self, encoding: str | None = None, errors: str | None = None) -> str:
        return self.read_path().read_text(encoding=encoding, errors=errors)


class BytesFile(TypedFile):
    def write(self, data: bytes) -> int:
        return self.write_path().write_bytes(data)

    def read(self) -> bytes:
        return self.read_path().read_bytes()
