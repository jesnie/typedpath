from pathlib import Path

from typedpath import BytesFile


def test_bytes_file(tmp_path: Path) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.bin"

    f = BytesFile(p)
    f.write(b"foo")

    assert d.exists()
    assert p.read_bytes() == b"foo"
    assert f.read() == b"foo"
