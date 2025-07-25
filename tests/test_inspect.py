from pathlib import Path

from tests.utils import TestFile, TestGenericDir
from typedpath import NO_ARGS, withargs
from typedpath.inspect import make


def test_make(tmp_path: Path) -> None:
    f = make(TestFile, tmp_path, NO_ARGS)
    assert isinstance(f, TestFile)
    assert tmp_path == f.pretty_path()
    assert f.kwargs == {}


def test_make__generic(tmp_path: Path) -> None:
    f = make(TestGenericDir[bool, float], tmp_path, NO_ARGS)
    assert isinstance(f, TestGenericDir)
    assert tmp_path == f.pretty_path()
    assert bool is f.t
    assert float is f.u
    assert f.kwargs == {}


def test_make__args(tmp_path: Path) -> None:
    f = make(TestFile, tmp_path, withargs(foo=1, bar=2))
    assert isinstance(f, TestFile)
    assert tmp_path == f.pretty_path()
    assert f.kwargs == {"foo": 1, "bar": 2}


def test_make__generic__args(tmp_path: Path) -> None:
    f = make(TestGenericDir[int, str], tmp_path, withargs(foo=3, bar=4))
    assert isinstance(f, TestGenericDir)
    assert tmp_path == f.pretty_path()
    assert int is f.t
    assert str is f.u
    assert f.kwargs == {"foo": 3, "bar": 4}
