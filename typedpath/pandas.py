from typing import Literal, TypeAlias

from typedpath.base import PathLikeLike, TypedFile

try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    from unittest.mock import MagicMock

    pd = MagicMock()

    PANDAS_AVAILABLE = False


class PandasCsvFile(TypedFile):
    """A file containing comma separated values (CSV)."""

    default_suffix = ".csv"

    def __init__(self, path: PathLikeLike, *, encoding: str = "utf-8") -> None:
        super().__init__(path)
        assert PANDAS_AVAILABLE, (
            "Pandas does not appear to be installed on this system. Try: pip install pandas"
        )

        self._encoding = encoding

    def write(self, data: pd.DataFrame) -> None:
        data.to_csv(self.write_path(), encoding=self._encoding, index=False)

    def append(self, data: pd.DataFrame) -> None:
        if not self.pretty_path().exists():
            self.write(data)
            return

        with open(self.read_path(), "ta", encoding=self._encoding) as fp:
            data.to_csv(fp, index=False, header=False)

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.read_path(), encoding=self._encoding)


class PandasFeatherFile(TypedFile):
    """A file containing data in the Apache Arrow Feather format."""

    default_suffix = ".feather"

    def __init__(self, path: PathLikeLike) -> None:
        super().__init__(path)
        assert PANDAS_AVAILABLE, (
            "Pandas does not appear to be installed on this system. Try: pip install pandas"
        )

    def write(self, data: pd.DataFrame) -> None:
        data.to_feather(self.write_path())

    def read(self) -> pd.DataFrame:
        return pd.read_feather(self.read_path())


ParquetEngine: TypeAlias = Literal["auto", "pyarrow", "fastparquet"]
ParquetCompression: TypeAlias = Literal["snappy", "gzip", "brotli", None]


class PandasParquetFile(TypedFile):
    """A file containing data in the Apache Parquet format."""

    default_suffix = ".parquet"

    def __init__(
        self,
        path: PathLikeLike,
        *,
        engine: ParquetEngine = "auto",
        compression: ParquetCompression = "snappy",
    ) -> None:
        super().__init__(path)
        assert PANDAS_AVAILABLE, (
            "Pandas does not appear to be installed on this system. Try: pip install pandas"
        )

        self._engine = engine
        self._compression = compression

    def write(self, data: pd.DataFrame) -> None:
        data.to_parquet(self.write_path(), engine=self._engine, compression=self._compression)

    def read(self) -> pd.DataFrame:
        return pd.read_parquet(self.read_path(), engine=self._engine)
