from typing import Any, Mapping, get_type_hints

from typedpath.args import NO_ARGS
from typedpath.base import PathLikeLike, TypedDir, TypedPath
from typedpath.inspect import make


class StructDir(TypedDir):
    """
    A directory containing a fixed number of members, of different types.

    To use this class create a subclass, using type hints to define the members and their types::

        class Person(tp.StructDir):
            name: tp.TextFile
            config: tp.JSONFile

        p = Person("my_path")

    You can use the `withargs` function to pass arguments to the members::

        class Person(tp.StructDir):
            name: tp.TextFile = withargs(encoding="ascii")
            config: tp.JSONFile
    """

    default_suffix = ""

    def __init__(
        self,
        path: PathLikeLike,
        globalns: Mapping[str, Any] | None = None,
        localns: Mapping[str, Any] | None = None,
    ) -> None:
        """
        :param path: Path this object refers to on disk.
        :param globalns: `globalns` to pass to `typing.get_type_hints`. Set this if you need to use
            strings for forward references for the type hints in the member declaration. You do not
            normally need to do this.
        :param localns: `localns` to pass to `typing.get_type_hints`. Set this if you need to use
            strings for forward references for the type hints in the member declaration. You do not
            normally need to do this.
        """
        super().__init__(path)

        globalns_dict = dict(globalns) if globalns is not None else None
        localns_dict = dict(localns) if localns is not None else None
        members = get_type_hints(self, globalns_dict, localns_dict)
        for name, member_type in members.items():
            member_path = self.pretty_path() / f"{name}{member_type.default_suffix}"
            args = getattr(self, name, NO_ARGS)
            member: TypedPath = make(member_type, member_path, args)
            setattr(self, name, member)
