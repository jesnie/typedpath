from abc import ABC, abstractmethod
from functools import singledispatch
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
        self._codec = get_key_codec(self._key_type)

    def _key_to_path(self, key: _K) -> Path:
        key_str = self._codec.encode(key)
        key_ = self._codec.decode(key_str, self._key_type)
        assert key_ == key, (
            "DictDir keys does not handle round-trip:" f" decodec(encode({key}))!={key_}."
        )
        assert "/" not in key_str, f"DictDir keys cannot contain '/'. Key: {key_str}"
        key_name = f"{key_str}{self._value_type.default_suffix}"
        return self._path / key_name

    def _path_to_key(self, path: Path) -> _K:
        key_name = path.name
        key_str = key_name[: -len(self._value_type.default_suffix)]
        return self._codec.decode(key_str, self._key_type)

    def __getitem__(self, key: _K) -> _PV:
        item_path = self._key_to_path(key)
        return self._value_type(item_path)

    def __iter__(self) -> Iterator[_K]:
        for item_path in self._path.iterdir():
            yield self._path_to_key(item_path)

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, self._key_type):
            return False
        return self._key_to_path(key).exists()

    def __len__(self) -> int:
        return len(list(self._path.iterdir()))


class KeyCodec(Generic[_K], ABC):
    @abstractmethod
    def encode(self, key: _K) -> str:
        ...

    @abstractmethod
    def decode(self, key_str: str, key_type: Type[_K]) -> _K:
        ...


class StrKeyCodec(KeyCodec[object]):
    ESCAPES = {
        "u": "_",  # Must be first, to avoid escaping the escapings...
        "s": "/",
        "d": ".",
    }

    def encode(self, key: object) -> str:
        key_str = str(key)
        for escape_seq, seq in self.ESCAPES.items():
            key_str = key_str.replace(seq, "_" + escape_seq)
        return key_str

    def decode(self, key_str: str, key_type: Type[object]) -> object:
        in_tokens = key_str.split("_")
        out_tokens = in_tokens[:1]
        for in_token in in_tokens[1:]:
            out_tokens.append(self.ESCAPES[in_token[0]])
            out_tokens.append(in_token[1:])
        key_str = "".join(out_tokens)
        return key_type(key_str)  # type: ignore[call-arg]


class BoolKeyCodec(KeyCodec[bool]):
    def encode(self, key: bool) -> str:
        return "True" if key else "False"

    def decode(self, key_str: str, key_type: Type[object]) -> bool:
        assert issubclass(key_type, bool), key_type
        match key_str:
            case "True":
                return True
            case "False":
                return False
        raise AssertionError(f"Don't know how to interpret {key_str} as a bool")


@singledispatch
def _codec_registry(key: _K) -> KeyCodec[_K]:
    raise AssertionError(f"Not KeyCodec for object {key} of type {type(key)}")


def get_key_codec(key_type: Type[_K]) -> KeyCodec[_K]:
    return _codec_registry.dispatch(key_type)()


def add_key_codec(key_type: Type[_K], codec: KeyCodec[_K]) -> None:
    _codec_registry.register(key_type)(lambda: codec)


add_key_codec(object, StrKeyCodec())
add_key_codec(bool, BoolKeyCodec())
