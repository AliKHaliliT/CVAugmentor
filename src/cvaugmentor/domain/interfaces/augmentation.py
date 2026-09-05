from typing import Protocol, runtime_checkable

from cvaugmentor.domain.schemas.media import Frame


@runtime_checkable
class IAugmentation(Protocol):

    """

    Interface defining one transformation the pipeline can apply to a frame.

    """

    name: str

    def apply(self, frame: Frame) -> Frame: ...

    def reseed(self) -> None: ...
