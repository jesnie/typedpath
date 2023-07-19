"""
A library for describing file-system structure with Python classes.
"""

from typedpath.args import NO_ARGS, Args, withargs
from typedpath.base import PathLikeLike, TypedDir, TypedFile, TypedPath
from typedpath.bytes import BytesFile
from typedpath.dict import DictDir
from typedpath.keycodec import (
    BoolKeyCodec,
    KeyCodec,
    StrKeyCodec,
    add_key_codec,
    get_key_codec,
)
from typedpath.struct import StructDir
from typedpath.text import TextFile

__all__ = [
    "Args",
    "BoolKeyCodec",
    "BytesFile",
    "DictDir",
    "KeyCodec",
    "NO_ARGS",
    "PathLikeLike",
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
