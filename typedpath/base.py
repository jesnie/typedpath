from abc import ABC
from os import PathLike
from pathlib import Path
from typing import TypeAlias

PathLikeLike: TypeAlias = PathLike[str] | str


class TypedPath(ABC):
    default_suffix: str

    def __init__(self, path: PathLikeLike) -> None:
        self._path = Path(path)

    def __str__(self) -> str:
        return str(self._path)


class TypedFile(TypedPath):
    def read_path(self) -> Path:
        assert self._path.is_file()
        return self._path

    def write_path(self) -> Path:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        return self._path

    def pretty_path(self) -> Path:
        return self._path


class TypedDir(TypedPath):
    def pretty_path(self) -> Path:
        return self._path
