from pathlib import Path

import numpy as np
import pytest

from typedpath import AnyNDArray, NpyFile, NpzFile

_DATA = [
    np.array([], dtype=np.float32),
    np.array([1, 2, 3], dtype=np.int64),
    np.array([[True, False], [False, True]]),
]


@pytest.mark.parametrize("data", _DATA)
def test_npy_file(tmp_path: Path, data: AnyNDArray) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.npy"

    f = NpyFile(p)
    f.write(data)

    assert d.exists()
    np.testing.assert_array_equal(data, np.load(p), strict=True)
    np.testing.assert_array_equal(data, f.read(), strict=True)


@pytest.mark.parametrize("data", _DATA)
def test_npz_file(tmp_path: Path, data: AnyNDArray) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.npz"

    f = NpzFile(p)
    f.write(data)

    assert d.exists()
    with np.load(p) as npz_file:
        np.testing.assert_array_equal(data, npz_file["array"], strict=True)
    np.testing.assert_array_equal(data, f.read(), strict=True)
