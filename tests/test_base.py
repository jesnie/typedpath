from pathlib import Path

from typedpath.base import BytesFile, TextFile


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
