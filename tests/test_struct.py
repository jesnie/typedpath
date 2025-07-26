from pathlib import Path

from tests.utils import TestFile, TestGenericDir
from typedpath import StructDir, withargs


def test_struct_dir(tmp_path: Path) -> None:
    class TestDir1(StructDir):
        x: TestFile
        y: TestGenericDir[int, float]

    class TestDir2(StructDir):
        a: TestDir1
        b: TestFile
        c: TestGenericDir[bool, str]

    d = TestDir2(tmp_path)
    d.a.x.write("d.a.x")
    d.a.y.file.write("d.a.y")
    d.b.write("d.b")
    d.c.file.write("d.c")

    assert (tmp_path / "a/x.test").exists()
    assert (tmp_path / "a/y/file.test").exists()
    assert (tmp_path / "b.test").exists()
    assert (tmp_path / "c/file.test").exists()

    assert d.a.x.read() == "d.a.x"
    assert d.a.y.file.read() == "d.a.y"
    assert d.b.read() == "d.b"
    assert d.c.file.read() == "d.c"


def test_struct_dir__args(tmp_path: Path) -> None:
    class TestDir(StructDir):
        a: TestFile = withargs(arg1=11, arg2=12)
        b: TestGenericDir[str, TestFile] = withargs(arg1=21, arg2=22)

    d = TestDir(tmp_path)
    assert d.a.kwargs == {"arg1": 11, "arg2": 12}
    assert str is d.b.t
    assert TestFile == d.b.u
    assert d.b.kwargs == {"arg1": 21, "arg2": 22}
