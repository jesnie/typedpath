from pathlib import Path
from typing import Sequence, Type

import pytest

from typedpath.args import withargs
from typedpath.base import _K, BytesFile, DictDir, StructDir, TextFile
from typedpath.key_codec import RawStrKeyCodec


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
    data = {k: str(i) for i, k in enumerate(keys)}
    d = DictDir(tmp_path, key_type, TextFile)
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
    for k, v in data.items():
        assert k in d
        assert v == d[k].read()


def test_dict_dir__subdirs(tmp_path: Path) -> None:
    data = {
        "a": b"1",
        "a/b": b"2",
        "a/b/c": b"3",
        "a/b/d": b"4",
    }
    d = DictDir(tmp_path, str, BytesFile, key_codec=RawStrKeyCodec(), allow_subdirs=True)

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


def test_struct_dir(tmp_path: Path) -> None:
    class TestDir1(StructDir):
        x: TextFile
        y: BytesFile

    class TestDir2(StructDir):
        a: TestDir1
        b: DictDir[int, TextFile]
        c: DictDir[str, TestDir1]

    d = TestDir2(tmp_path, globalns=globals(), localns=locals())
    d.a.x.write("d.a.x")
    d.a.y.write(b"d.a.y")
    d.b[13].write("d.b[13]")
    d.c["foo"].x.write('d.c["foo"].x')
    d.c["foo"].y.write(b'd.c["foo"].y')

    assert "d.a.x" == d.a.x.read()
    assert b"d.a.y" == d.a.y.read()
    assert "d.b[13]" == d.b[13].read()
    assert 'd.c["foo"].x' == d.c["foo"].x.read()
    assert b'd.c["foo"].y' == d.c["foo"].y.read()


def test_struct_dir__withargs(tmp_path: Path) -> None:
    class TestDir(StructDir):
        a: DictDir[str, TextFile] = withargs(
            key_codec=RawStrKeyCodec(), allow_subdirs=True, value_args=withargs(encoding="utf-8")
        )

    d = TestDir(tmp_path)
    d.a["foo/bar"].write('d.a["foo/bar"]')

    assert 'd.a["foo/bar"]' == d.a["foo/bar"].read()
