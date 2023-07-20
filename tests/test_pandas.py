from pathlib import Path

import pandas as pd
import pytest

from typedpath import PandasCsvFile, PandasFeatherFile, PandasParquetFile

_DF = pd.DataFrame(
    {
        "a": [0, 1, 2],
        "b": ["foo", "bar", "baz"],
    }
)
_DATA = [
    pd.DataFrame([], columns=["a", "b"]),
    _DF,
]


@pytest.mark.parametrize("data", _DATA)
def test_pandas_csv_file(tmp_path: Path, data: pd.DataFrame) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.csv"

    f = PandasCsvFile(p)
    f.write(data)

    assert d.exists()
    pd.testing.assert_frame_equal(data, pd.read_csv(p))
    pd.testing.assert_frame_equal(data, f.read())


def test_pandas_csv_file__append(tmp_path: Path) -> None:
    data = _DF

    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.csv"

    f = PandasCsvFile(p)
    for i in range(len(data)):
        f.append(data.iloc[i : i + 1])

    assert d.exists()
    pd.testing.assert_frame_equal(data, pd.read_csv(p))
    pd.testing.assert_frame_equal(data, f.read())


@pytest.mark.parametrize("data", _DATA)
def test_pandas_feather_file(tmp_path: Path, data: pd.DataFrame) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.feather"

    f = PandasFeatherFile(p)
    f.write(data)

    assert d.exists()
    pd.testing.assert_frame_equal(data, pd.read_feather(p))
    pd.testing.assert_frame_equal(data, f.read())


@pytest.mark.parametrize("data", _DATA)
def test_pandas_parquet_file(tmp_path: Path, data: pd.DataFrame) -> None:
    d = tmp_path / "dir"
    assert not d.exists()
    p = d / "test.parquet"

    f = PandasParquetFile(p)
    f.write(data)

    assert d.exists()
    pd.testing.assert_frame_equal(data, pd.read_parquet(p))
    pd.testing.assert_frame_equal(data, f.read())
