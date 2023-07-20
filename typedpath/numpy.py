from typing import Any

from typedpath.base import PathLikeLike, TypedFile

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    from unittest.mock import MagicMock

    np = MagicMock()

    NUMPY_AVAILABLE = False


AnyNDArray = np.ndarray[Any, Any]


class NpyFile(TypedFile):
    default_suffix = ".npy"

    def __init__(self, path: PathLikeLike, *, allow_pickle: bool = False) -> None:
        super().__init__(path)
        assert (
            NUMPY_AVAILABLE
        ), "NumPy does not appear to be installed on this system. Try: pip install numpy"
        assert (
            self.pretty_path().suffix == self.default_suffix
        ), "NumPy requires file to have suffix '{self.default_suffix}'. File: {self.pretty_path()}"

        self._allow_pickle = allow_pickle

    def write(self, data: AnyNDArray) -> None:
        np.save(self.write_path(), data, allow_pickle=self._allow_pickle)

    def read(self) -> AnyNDArray:
        return np.load(  # type: ignore[no-any-return]
            self.read_path(), allow_pickle=self._allow_pickle
        )


class NpzFile(TypedFile):
    default_suffix = ".npz"

    def __init__(self, path: PathLikeLike, *, allow_pickle: bool = False) -> None:
        super().__init__(path)
        assert (
            NUMPY_AVAILABLE
        ), "NumPy does not appear to be installed on this system. Try: pip install numpy"
        assert (
            self.pretty_path().suffix == self.default_suffix
        ), "NumPy requires file to have suffix '{self.default_suffix}'. File: {self.pretty_path()}"

        self._allow_pickle = allow_pickle

    def write(self, data: AnyNDArray) -> None:
        np.savez_compressed(self.write_path(), array=data)

    def read(self) -> AnyNDArray:
        with np.load(self.read_path(), allow_pickle=self._allow_pickle) as npz_file:
            return npz_file["array"]  # type: ignore[no-any-return]
