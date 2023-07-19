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

    assert "d.a.x" == d.a.x.read()
    assert "d.a.y" == d.a.y.file.read()
    assert "d.b" == d.b.read()
    assert "d.c" == d.c.file.read()


def test_struct_dir__args(tmp_path: Path) -> None:
    class TestDir(StructDir):
        a: TestFile = withargs(arg1=11, arg2=12)
        b: TestGenericDir[str, TestFile] = withargs(arg1=21, arg2=22)

    d = TestDir(tmp_path)
    assert {"arg1": 11, "arg2": 12} == d.a.kwargs
    assert str == d.b.t
    assert TestFile == d.b.u
    assert {"arg1": 21, "arg2": 22} == d.b.kwargs
