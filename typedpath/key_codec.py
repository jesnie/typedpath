from abc import ABC, abstractmethod
from functools import singledispatch
from typing import Any, Generic, Type, TypeVar

_K = TypeVar("_K")


class KeyCodec(Generic[_K], ABC):
    @abstractmethod
    def encode(self, key: _K) -> str:
        ...

    @abstractmethod
    def decode(self, key_str: str, key_type: Type[_K]) -> _K:
        ...


class StrKeyCodec(KeyCodec[Any]):
    ESCAPES = {
        "h": "^",  # Must be first, to avoid escaping the escapings...
        "s": "/",
    }

    def encode(self, key: Any) -> str:
        key_str = str(key)
        for escape_seq, seq in self.ESCAPES.items():
            key_str = key_str.replace(seq, "^" + escape_seq)
        return key_str

    def decode(self, key_str: str, key_type: Type[Any]) -> Any:
        in_tokens = key_str.split("^")
        out_tokens = in_tokens[:1]
        for in_token in in_tokens[1:]:
            out_tokens.append(self.ESCAPES[in_token[0]])
            out_tokens.append(in_token[1:])
        key_str = "".join(out_tokens)
        return key_type(key_str)


class RawStrKeyCodec(KeyCodec[Any]):
    def encode(self, key: Any) -> str:
        return str(key)

    def decode(self, key_str: str, key_type: Type[Any]) -> Any:
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
def _codec_registry(key: _K) -> KeyCodec[_K]:
    raise AssertionError(f"No KeyCodec for object {key} of type {type(key)}")


def get_key_codec(key_type: Type[_K]) -> KeyCodec[_K]:
    return _codec_registry.dispatch(key_type)()


def add_key_codec(key_type: Type[_K], codec: KeyCodec[_K]) -> None:
    _codec_registry.register(key_type)(lambda: codec)


add_key_codec(object, StrKeyCodec())
add_key_codec(bool, BoolKeyCodec())
