from pathlib import Path
from typing import TypeVar

import pytest

from typedpath import BoolKeyCodec, KeyCodec, StrKeyCodec, get_key_codec

T = TypeVar("T")


@pytest.mark.parametrize(
    "codec,key,expected",
    [
        # StrKeyCodec()
        (StrKeyCodec(), "", ""),
        (StrKeyCodec(), "abc", "abc"),
        (StrKeyCodec(), "a/^/c", "a^s^h^sc"),
        (StrKeyCodec(), 5, "5"),
        (StrKeyCodec(), -2, "-2"),
        (StrKeyCodec(), 3.1, "3.1"),
        (StrKeyCodec(), Path("/a/b/c"), "^sa^sb^sc"),
        # StrKeyCodec(escape=False)
        (StrKeyCodec(escape=False), "", ""),
        (StrKeyCodec(escape=False), "abc", "abc"),
        (StrKeyCodec(escape=False), "a/^/c", "a/^/c"),
        (StrKeyCodec(escape=False), 5, "5"),
        (StrKeyCodec(escape=False), -2, "-2"),
        (StrKeyCodec(escape=False), 3.1, "3.1"),
        (StrKeyCodec(escape=False), Path("/a/b/c"), "/a/b/c"),
        # BoolKeyCodec()
        (BoolKeyCodec(), True, "True"),
        (BoolKeyCodec(), False, "False"),
    ],
)
def test_key_codec(codec: KeyCodec[T], key: T, expected: str) -> None:
    assert expected == codec.encode(key)
    assert key == codec.decode(expected, type(key))
    assert key == codec.decode(codec.encode(key), type(key))


def test_get_key_codec() -> None:
    assert isinstance(get_key_codec(int), StrKeyCodec)
    assert isinstance(get_key_codec(str), StrKeyCodec)
    assert isinstance(get_key_codec(float), StrKeyCodec)
    assert isinstance(get_key_codec(bool), BoolKeyCodec)
