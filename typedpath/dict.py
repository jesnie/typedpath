from pathlib import Path
from typing import Generic, Iterator, Mapping, Type, TypeVar

from typedpath.args import NO_ARGS, Args
from typedpath.base import PathLikeLike, TypedDir, TypedPath
from typedpath.inspect import make
from typedpath.keycodec import KeyCodec, get_key_codec

K = TypeVar("K")
TP = TypeVar("TP", bound=TypedPath)


class DictDir(TypedDir, Mapping[K, TP], Generic[K, TP]):
    default_suffix = ""

    def __init__(
        self,
        path: PathLikeLike,
        key_type: Type[K],
        value_type: Type[TP],
        *,
        key_codec: KeyCodec[K] | None = None,
        allow_subdirs: bool = False,
        value_args: Args = NO_ARGS,
    ) -> None:
        super().__init__(path)

        self._key_type = key_type
        self._value_type = value_type
        self._codec = key_codec or get_key_codec(self._key_type)
        self._allow_subdirs = allow_subdirs
        self._value_args = value_args

    def _key_to_path(self, key: K) -> Path:
        key_str = self._codec.encode(key)
        key_ = self._codec.decode(key_str, self._key_type)
        assert key_ == key, (
            "DictDir key did not handle round-trip:" f" decodec(encode({key}))={key_}."
        )
        assert key_str, "DictDir keys cannot be empty."
        if not self._allow_subdirs:
            assert "/" not in key_str, f"DictDir keys cannot contain '/'. Key: {key_str}"
        key_name = f"{key_str}{self._value_type.default_suffix}"
        return self._path / key_name

    def _path_to_key(self, path: Path) -> K:
        key_name = path.name
        expected_suffix = self._value_type.default_suffix
        assert key_name.endswith(expected_suffix), f"{path} did not have suffix {expected_suffix}."
        key_str = key_name.removesuffix(expected_suffix)
        return self._codec.decode(key_str, self._key_type)

    def __getitem__(self, key: K) -> TP:
        item_path = self._key_to_path(key)
        return make(self._value_type, item_path, self._value_args)

    def __iter__(self) -> Iterator[K]:
        assert not self._allow_subdirs, "__iter__ is not compatible with allow_subdirs=True."
        for item_path in self._path.iterdir():
            yield self._path_to_key(item_path)

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, self._key_type):
            return False
        return self._key_to_path(key).exists()

    def __len__(self) -> int:
        assert not self._allow_subdirs, "__len__ is not compatible with allow_subdirs=True."
        return len(list(self._path.iterdir()))
