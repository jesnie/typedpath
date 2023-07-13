from pathlib import Path
from typing import Sequence, Type

import pytest

from typedpath.base import _K, BytesFile, DictDir, TextFile


def test_text_file(tmp_path: Path) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.txt"

    f = TextFile(p)
    f.write("foo")

    assert d.exists()
    assert "foo" == p.read_text()
    assert "foo" == f.read()


def test_bytes_file(tmp_path: Path) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.bin"

    f = BytesFile(p)
    f.write(b"foo")

    assert d.exists()
    assert b"foo" == p.read_bytes()
    assert b"foo" == f.read()


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
def test_dict_dir__keys(key_type: Type[_K], keys: Sequence[_K], tmp_path: Path) -> None:
    d = DictDir(tmp_path, key_type, TextFile)
    assert not d
    assert len(d) == 0
    assert not d.keys()
    assert not d.values()
    assert not d.items()
    for k in keys:
        assert k not in d

    test_dict = {k: str(i) for i, k in enumerate(keys)}
    for k, v in test_dict.items():
        d[k].write(v)

    assert d
    assert len(d) == len(keys)

    assert set(d.keys()) == set(keys)
    assert set(v.read() for v in d.values()) == set(test_dict.values())
    assert {k: v.read() for k, v in d.items()} == test_dict
    for k in keys:
        assert k in d


def test_dict_dir__bytes_file(tmp_path: Path) -> None:
    data = {
        0.1: b"1",
        6.28: b"2",
        31337.0: b"3",
    }
    d = DictDir(tmp_path, float, BytesFile)
    assert not d
    assert len(d) == 0
    assert not d.keys()
    assert not d.values()
    assert not d.items()
    for k in data:
        assert k not in d

    for k, v in data.items():
        d[k].write(v)

    assert d
    assert len(d) == len(data)

    assert set(d.keys()) == set(data)
    assert len(d.values()) == len(data)
    assert len(d.items()) == len(data)
    for k, v_ in d.items():
        assert data[k] == v_.read()
    for k in data:
        assert k in d
