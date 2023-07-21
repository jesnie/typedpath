from typing import TypeVar, get_args, get_origin

from typedpath.args import Args
from typedpath.base import PathLikeLike, TypedPath

TP = TypeVar("TP", bound=TypedPath)


def make(t: type[TP], path: PathLikeLike, args: Args) -> TP:
    """
    Create a new instance of type `t`, using `path` and `args`.
    """
    origin_type = get_origin(t) or t
    type_args = get_args(t)
    return origin_type(path, *type_args, **args.kwargs)
