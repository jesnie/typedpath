from pathlib import Path
from typing import Any, Sequence, Type

import pytest

from tests.utils import TestFile, TestGenericDir
from typedpath import DictDir, StrKeyCodec, withargs


@pytest.mark.parametrize(
    "key_type, keys",
    [
        (int, range(3)),
        (str, "abc"),
        (str, ["abc.def.ghi", "abc/def/ghi", "__/__s__/s/"]),
        (bool, [True, False]),
        (float, [0.1, 6.28, 4.0]),
    ],
)
def test_dict_dir__keys(key_type: Type[Any], keys: Sequence[Any], tmp_path: Path) -> None:
    data = {k: str(i) for i, k in enumerate(keys)}
    d = DictDir(tmp_path, key_type, TestFile)
    assert not d
    assert len(d) == 0
    assert not d.keys()
    assert not d.values()
    assert not d.items()
    for k in keys:
        assert k not in d

    for k, v in data.items():
        d[k].write(v)

    assert d
    assert len(d) == len(keys)
    assert set(d.keys()) == set(keys)
    assert set(v.read() for v in d.values()) == set(data.values())
    assert {k: v.read() for k, v in d.items()} == data
    for k, v in data.items():
        assert k in d
        assert v == d[k].read()


def test_dict_dir__nested(tmp_path: Path) -> None:
    data = {
        1: {
            "one": "11",
            "two": "12",
        },
        2: {
            "three": "23",
            "four": "24",
        },
    }
    d = DictDir(tmp_path, int, DictDir[str, TestGenericDir[int, bool]])
    assert not d
    assert len(d) == 0
    assert not d.keys()
    assert not d.values()
    assert not d.items()
    for k in data:
        assert k not in d

    for k1, v1 in data.items():
        for k2, v2 in v1.items():
            d[k1][k2].file.write(v2)

    assert d
    assert len(d) == len(data)
    assert set(d.keys()) == set(data)
    assert len(d.values()) == len(data)
    assert len(d.items()) == len(data)
    for k1, v1_ in d.items():
        for k2, v2_ in v1_.items():
            assert data[k1][k2] == v2_.file.read()

    for k1, v1 in data.items():
        assert k1 in d
        v1_ = d[k1]
        assert v1_
        assert len(v1_) == len(v1)
        assert set(v1_.keys()) == set(v1)
        assert len(v1_.values()) == len(v1)
        assert len(v1_.items()) == len(v1)
        for k2, v2 in v1.items():
            assert k2 in v1_
            assert v2 == v1_[k2].file.read()


def test_dict_dir__subdirs(tmp_path: Path) -> None:
    data = {
        "a": "1",
        "a/b": "2",
        "a/b/c": "3",
        "a/b/d": "4",
    }
    d = DictDir(tmp_path, str, TestFile, key_codec=StrKeyCodec(escape=False), allow_subdirs=True)

    with pytest.raises(AssertionError):
        bool(d)

    with pytest.raises(AssertionError):
        len(d)

    with pytest.raises(AssertionError):
        next(iter(d.keys()))

    with pytest.raises(AssertionError):
        next(iter(d.values()))

    with pytest.raises(AssertionError):
        next(iter(d.items()))

    for k in data:
        assert k not in d

    for k, v in data.items():
        d[k].write(v)

    for k, v in data.items():
        assert k in d
        assert v == d[k].read()


def test_dict_dir__args(tmp_path: Path) -> None:
    d1 = DictDir(tmp_path / "1", str, TestFile, value_args=withargs(foo=1, bar=2))
    assert {"foo": 1, "bar": 2} == d1["test"].kwargs

    d2 = DictDir(tmp_path / "2", str, TestGenericDir[int, str], value_args=withargs(foo=1, bar=2))
    assert int == d2["test"].t
    assert str == d2["test"].u
    assert {"foo": 1, "bar": 2} == d2["test"].kwargs
