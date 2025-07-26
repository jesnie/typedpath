from pathlib import Path

from typedpath import TextFile


def test_text_file(tmp_path: Path) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.txt"

    f = TextFile(p)
    f.write("foo")

    assert d.exists()
    assert p.read_text() == "foo"
    assert f.read() == "foo"
