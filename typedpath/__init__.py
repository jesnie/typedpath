"""
A library for describing file-system structure with Python classes.
"""

from typedpath.args import NO_ARGS, Args, withargs
from typedpath.base import PathLikeLike, TypedDir, TypedFile, TypedPath
from typedpath.bytes import BytesFile
from typedpath.dict import DictDir
from typedpath.json import JSON, JSONFile, ReadOnlyJSON
from typedpath.keycodec import (
    BoolKeyCodec,
    KeyCodec,
    StrKeyCodec,
    add_key_codec,
    get_key_codec,
)
from typedpath.numpy import AnyNDArray, NpyFile, NpzFile
from typedpath.pandas import PandasCsvFile, PandasFeatherFile, PandasParquetFile
from typedpath.pickle import PickleFile
from typedpath.struct import StructDir
from typedpath.text import TextFile

__all__ = [
    "AnyNDArray",
    "Args",
    "BoolKeyCodec",
    "BytesFile",
    "DictDir",
    "JSON",
    "JSONFile",
    "KeyCodec",
    "NO_ARGS",
    "NpyFile",
    "NpzFile",
    "PandasCsvFile",
    "PandasFeatherFile",
    "PandasParquetFile",
    "PathLikeLike",
    "PickleFile",
    "ReadOnlyJSON",
    "StrKeyCodec",
    "StructDir",
    "TextFile",
    "TypedDir",
    "TypedFile",
    "TypedPath",
    "add_key_codec",
    "get_key_codec",
    "withargs",
]
