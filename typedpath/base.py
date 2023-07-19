from abc import ABC
from os import PathLike
from pathlib import Path
from typing import (
    Any,
    Generic,
    Iterator,
    Mapping,
    Type,
    TypeAlias,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

from typedpath.args import NO_ARGS, Args
from typedpath.key_codec import KeyCodec, get_key_codec

_K = TypeVar("_K")
_PV = TypeVar("_PV", bound="TypedPath")


PathLikeLike: TypeAlias = PathLike[str] | str


class TypedPath(ABC):
    default_suffix: str

    def __init__(self, path: PathLikeLike) -> None:
        self._path = Path(path)

    def __str__(self) -> str:
        return str(self._path)


def _make(t: type[_PV], path: PathLikeLike, args: Args) -> _PV:
    origin_type = get_origin(t) or t
    type_args = get_args(t)
    return origin_type(path, *type_args, **args.kwargs)


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

    def __init__(self, path: PathLikeLike, *, encoding: str | None = None) -> None:
        super().__init__(path)

        self._encoding = encoding

    def write(
        self,
        data: str,
        *,
        errors: str | None = None,
        newline: str | None = None,
    ) -> int:
        return self.write_path().write_text(
            data, encoding=self._encoding, errors=errors, newline=newline
        )

    def read(self, errors: str | None = None) -> str:
        return self.read_path().read_text(encoding=self._encoding, errors=errors)


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

    def __init__(
        self,
        path: PathLikeLike,
        key_type: Type[_K],
        value_type: Type[_PV],
        *,
        key_codec: KeyCodec[_K] | None = None,
        allow_subdirs: bool = False,
        value_args: Args = NO_ARGS,
    ) -> None:
        super().__init__(path)

        self._key_type = key_type
        self._value_type = value_type
        self._codec = key_codec or get_key_codec(self._key_type)
        self._allow_subdirs = allow_subdirs
        self._value_args = value_args

    def _key_to_path(self, key: _K) -> Path:
        key_str = self._codec.encode(key)
        key_ = self._codec.decode(key_str, self._key_type)
        assert key_ == key, (
            "DictDir key did not handle round-trip:" f" decodec(encode({key}))={key_}."
        )
        assert key_str, "DictDir keys cannot be empty."
        if not self._allow_subdirs:
            assert "/" not in key_str, f"DictDir keys cannot contain '/'. Key: {key_str}"
        key_name = f"{key_str}{self._value_type.default_suffix}"
        return self._path / key_name

    def _path_to_key(self, path: Path) -> _K:
        key_name = path.name
        expected_suffix = self._value_type.default_suffix
        assert key_name.endswith(expected_suffix), f"{path} did not have suffix {expected_suffix}."
        key_str = key_name.removesuffix(expected_suffix)
        return self._codec.decode(key_str, self._key_type)

    def __getitem__(self, key: _K) -> _PV:
        item_path = self._key_to_path(key)
        return _make(self._value_type, item_path, self._value_args)

    def __iter__(self) -> Iterator[_K]:
        assert not self._allow_subdirs, "__iter__ is not compatible with allow_subdirs=True."
        for item_path in self._path.iterdir():
            yield self._path_to_key(item_path)

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, self._key_type):
            return False
        return self._key_to_path(key).exists()

    def __len__(self) -> int:
        assert not self._allow_subdirs, "__len__ is not compatible with allow_subdirs=True."
        return len(list(self._path.iterdir()))


class StructDir(TypedDir):
    default_suffix = ""

    def __init__(
        self,
        path: PathLikeLike,
        globalns: Mapping[str, Any] | None = None,
        localns: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(path)

        globalns_dict = dict(globalns) if globalns is not None else None
        localns_dict = dict(localns) if localns is not None else None

        for name, member_type in get_type_hints(self, globalns_dict, localns_dict).items():
            member_path = self.pretty_path() / name
            args = getattr(self, name, NO_ARGS)
            member: TypedPath = _make(member_type, member_path, args)
            setattr(self, name, member)
