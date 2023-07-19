from typing import Any, Mapping, get_type_hints

from typedpath.args import NO_ARGS
from typedpath.base import PathLikeLike, TypedDir, TypedPath
from typedpath.inspect import make


class StructDir(TypedDir):
    default_suffix = ""

    def __init__(
        self,
        path: PathLikeLike,
        globalns: Mapping[str, Any] | None = None,
        localns: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(path)

        globalns_dict = dict(globalns) if globalns is not None else None
        localns_dict = dict(localns) if localns is not None else None
        members = get_type_hints(self, globalns_dict, localns_dict)
        for name, member_type in members.items():
            member_path = self.pretty_path() / name
            args = getattr(self, name, NO_ARGS)
            member: TypedPath = make(member_type, member_path, args)
            setattr(self, name, member)
