import json
from pathlib import Path
from typing import Sequence

import pytest

from typedpath import JSONFile, ReadOnlyJSON

_DATA: Sequence[ReadOnlyJSON] = [
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
def test_json_file(tmp_path: Path, data: ReadOnlyJSON) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.json"

    f = JSONFile(p)
    f.write(data)

    assert d.exists()
    with open(p, "rt", encoding="utf-8") as fp:
        assert data == json.load(fp)
    assert data == f.read()
