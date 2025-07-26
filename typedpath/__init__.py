"""
A library for describing file-system structure with Python classes.

Example::

    import typedpath as tp


    class Person(tp.StructDir):
        name: tp.TextFile
        config: tp.JSONFile


    class Database(tp.StructDir):
        people: tp.DictDir[str, Person]


    d = Database("database")
    d.people["alice"].name.write("Alice")
    d.people["alice"].config.write({"require_authentication": True})
    d.people["bob"].name.write("Bob")
    d.people["bob"].config.write({"require_authentication": False})

Creates::
    > tree database/
    database/
    └── people
        ├── alice
        │   ├── config.json
        │   └── name.txt
        └── bob
            ├── config.json
            └── name.txt
"""

from typedpath.args import NO_ARGS, Args, withargs
from typedpath.base import PathLikeLike, TypedDir, TypedFile, TypedPath
from typedpath.bytes import BytesFile
from typedpath.dict import DictDir
from typedpath.json import JSON, JSONFile, MutableJSON
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

__version__ = "0.1.0"

__all__ = [
    "JSON",
    "NO_ARGS",
    "AnyNDArray",
    "Args",
    "BoolKeyCodec",
    "BytesFile",
    "DictDir",
    "JSONFile",
    "KeyCodec",
    "MutableJSON",
    "NpyFile",
    "NpzFile",
    "PandasCsvFile",
    "PandasFeatherFile",
    "PandasParquetFile",
    "PathLikeLike",
    "PickleFile",
    "StrKeyCodec",
    "StructDir",
    "TextFile",
    "TypedDir",
    "TypedFile",
    "TypedPath",
    "__version__",
    "add_key_codec",
    "get_key_codec",
    "withargs",
]
