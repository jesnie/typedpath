from dataclasses import dataclass
from typing import Any, Final, Mapping


@dataclass(frozen=True)
class Args:
    kwargs: Mapping[str, Any]


def withargs(**kwargs: Any) -> Any:
    return Args(kwargs)


NO_ARGS: Final[Args] = withargs()
