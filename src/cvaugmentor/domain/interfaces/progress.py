from collections.abc import Iterable, Iterator
from typing import Protocol, runtime_checkable


@runtime_checkable
class IProgressSink(Protocol):

    """

    Interface defining where the runner reports the work it is walking through.

    """

    def track[T](self, items: Iterable[T], description: str, unit: str, total: int | None = None) -> Iterator[T]: ...
