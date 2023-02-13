from abc import ABC
from os import PathLike
from pathlib import Path
from typing import Generic, Iterator, Mapping, Type, TypeAlias, TypeVar

_K = TypeVar("_K")
_PV = TypeVar("_PV", bound="TypedPath")


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


class TextFile(TypedFile):
    default_suffix = ".txt"

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
    default_suffix = ".bin"

    def write(self, data: bytes) -> int:
        return self.write_path().write_bytes(data)

    def read(self) -> bytes:
        return self.read_path().read_bytes()


class TypedDir(TypedPath):
    def pretty_path(self) -> Path:
        return self._path


class DictDir(TypedDir, Mapping[_K, _PV], Generic[_K, _PV]):
    default_suffix = ""

    def __init__(self, path: PathLikeLike, key_type: Type[_K], value_type: Type[_PV]) -> None:
        super().__init__(path)

        self._key_type = key_type
        self._value_type = value_type

    def _key_to_path(self, key: object) -> Path:
        key_str = str(key)
        key_ = self._key_type(key_str)  # type: ignore[call-arg]
        assert key_ == key, (
            "DictDir keys does not handle round-trip:"
            f" {self._key_type.__name__}(str({key}))!={key_}."
        )
        assert "/" not in key_str, f"DictDir keys cannot contain '/'. Key: {key_str}"
        key_name = f"{key_str}{self._value_type.default_suffix}"
        return self._path / key_name

    def _path_to_key(self, path: Path) -> _K:
        key_name = path.name
        key_str = key_name[: -len(self._value_type.default_suffix)]
        return self._key_type(key_str)  # type: ignore[call-arg]

    def __getitem__(self, key: _K) -> _PV:
        item_path = self._key_to_path(key)
        return self._value_type(item_path)

    def __iter__(self) -> Iterator[_K]:
        for item_path in self._path.iterdir():
            yield self._path_to_key(item_path)

    def __contains__(self, key: object) -> bool:
        return self._key_to_path(key).exists()

    def __len__(self) -> int:
        return len(list(self._path.iterdir()))
