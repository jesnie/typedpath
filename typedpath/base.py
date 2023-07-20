from abc import ABC
from os import PathLike
from pathlib import Path
from typing import TypeAlias

PathLikeLike: TypeAlias = PathLike[str] | str


class TypedPath(ABC):
    """
    Base class for all typed paths.

    Generally the files on disk are created lazily - when data is written to them.
    """

    default_suffix: str
    """
    The default suffix files/dirs of this type have.

    May be empty. If not empty, should start with a `.`.
    """

    def __init__(self, path: PathLikeLike) -> None:
        """
        :param path: Path this object refers to on disk.
        """
        assert self.default_suffix == "" or self.default_suffix.startswith(
            "."
        ), f"Default suffix should be empty or start with '.'. Found: {self.default_suffix}"
        self._path = Path(path)

    def __str__(self) -> str:
        return str(self._path)


class TypedFile(TypedPath):
    """
    Base class for `TypedPath`s representing a file.

    To read the represented file you should access `.read_path()`.
    To write to the represented file you should access `.write_path()`.
    For any other purposes, use `.pretty_path()`.
    """

    def read_path(self) -> Path:
        """
        Returns the path of this file, for reading.

        It is an error if the file does not exist.
        """
        assert self._path.is_file()
        return self._path

    def write_path(self) -> Path:
        """
        Returns the path of this file, for writing.

        This creates any necessary parent directories.
        The file may or may not already exist.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)
        return self._path

    def pretty_path(self) -> Path:
        """
        Returns the path of this file, for printing.
        """
        return self._path


class TypedDir(TypedPath):
    """
    Base class for `TypedPath`s represeting a directory.

    In general subclasses should not create their directories on disk - instead
    `TypedFile.write_path` creates directories as needed.
    """

    def pretty_path(self) -> Path:
        """
        Returns the path of this directory, for printing.
        """
        return self._path
