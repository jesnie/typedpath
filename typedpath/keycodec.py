from abc import ABC, abstractmethod
from functools import singledispatch
from typing import Any, Generic, Type, TypeVar

T = TypeVar("T")


class KeyCodec(Generic[T], ABC):
    @abstractmethod
    def encode(self, key: T) -> str:
        ...

    @abstractmethod
    def decode(self, key_str: str, key_type: Type[T]) -> T:
        ...


_ESCAPE_CHAR = "^"
_ESCAPES = {
    "h": _ESCAPE_CHAR,  # Must be first, to avoid escaping the escapings...
    "s": "/",
}


class StrKeyCodec(KeyCodec[Any]):
    def __init__(self, escape: bool = True) -> None:
        self._escape = escape

    def encode(self, key: Any) -> str:
        key_str = str(key)
        if self._escape:
            for escape_seq, seq in _ESCAPES.items():
                key_str = key_str.replace(seq, _ESCAPE_CHAR + escape_seq)
        return key_str

    def decode(self, key_str: str, key_type: Type[Any]) -> Any:
        if self._escape:
            in_tokens = key_str.split(_ESCAPE_CHAR)
            out_tokens = in_tokens[:1]
            for in_token in in_tokens[1:]:
                out_tokens.append(_ESCAPES[in_token[0]])
                out_tokens.append(in_token[1:])
            key_str = "".join(out_tokens)
        return key_type(key_str)


class BoolKeyCodec(KeyCodec[bool]):
    def encode(self, key: bool) -> str:
        return "True" if key else "False"

    def decode(self, key_str: str, key_type: Type[bool]) -> bool:
        assert issubclass(key_type, bool), key_type
        match key_str:
            case "True":
                return True
            case "False":
                return False
        raise AssertionError(f"Don't know how to interpret {key_str} as a bool")


@singledispatch
def _codec_registry(key: T) -> KeyCodec[T]:
    raise AssertionError(f"No KeyCodec for object {key} of type {type(key)}")


def get_key_codec(key_type: Type[T]) -> KeyCodec[T]:
    return _codec_registry.dispatch(key_type)()


def add_key_codec(key_type: Type[T], codec: KeyCodec[T]) -> None:
    _codec_registry.register(key_type)(lambda: codec)


add_key_codec(object, StrKeyCodec())
add_key_codec(bool, BoolKeyCodec())