from pathlib import Path
from typing import Protocol, runtime_checkable

from cvaugmentor.domain.schemas.media import MediaKind


@runtime_checkable
class IWorkspace(Protocol):

    """

    Interface defining how the runner reads what a location holds.

    """

    def list_entries(self, directory: Path) -> list[Path]: ...

    def is_kind(self, path: Path, kind: MediaKind) -> bool: ...
