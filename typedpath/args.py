# ruff: noqa: ERA001

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Final


@dataclass(frozen=True)
class Args:
    """A set of arguments to be passed to a `TypedPath` later."""

    kwargs: Mapping[str, Any]


def withargs(**kwargs: Any) -> Any:
    """Binds arguments for a `TypedPath` instance."""
    # This returns `Any` so we can do:
    # foo: Foo = withargs(1, 2, 3)
    return Args(kwargs)


NO_ARGS: Final[Args] = withargs()
"""An empty set of arguments."""
