from pathlib import Path
from typing import Protocol, runtime_checkable

from cvaugmentor.domain.schemas.media import MediaKind, MediaStream


@runtime_checkable
class IMediaCodec(Protocol):

    """

    Interface defining how one medium kind is decoded and encoded.

    """

    kind: MediaKind

    def read(self, source: Path) -> MediaStream: ...

    def write(self, destination: Path, stream: MediaStream) -> None: ...
