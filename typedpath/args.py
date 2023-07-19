from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Args:
    args: Mapping[str, Any]


def withargs(**kwargs: Any) -> Any:
    return Args(kwargs)
