import pickle
from pathlib import Path
from typing import Any, Sequence, TypeVar

import pytest

from typedpath import PickleFile

T = TypeVar("T")

_DATA: Sequence[Any] = [
    42,
    6.28,
    "foo",
    False,
    None,
    {
        "ints": [1, 2, 3, 4],
        "floats": [0.1, 0.2, 0.3, 0.4],
        "strs": ["foo", "bar", "baz"],
        "bools": [True, False],
        "nones": [None, None, None],
        "empties": [[], {}, ""],
    },
]


@pytest.mark.parametrize("data", _DATA)
def test_pickle_file(tmp_path: Path, data: T) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.pickle"

    f = PickleFile(p, type(data))
    f.write(data)

    assert d.exists()
    with open(p, "rb") as fp:
        assert data == pickle.load(fp)
    assert data == f.read()
