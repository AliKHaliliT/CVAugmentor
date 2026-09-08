from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any, Literal

MediaKind = Literal["image", "video"]

# The opaque pixel payload the codecs and the augmentations agree on, and that nothing in
# the domain or the services ever inspects. Naming the concrete carrier here would drag an
# imaging SDK across the Dependency Rule, so the core moves frames it cannot read
# (see decision 0042). Every shipped adapter now agrees that the carrier is an HxWx3 uint8
# array in RGB order (see decision 0049), but that agreement lives among the adapters and
# never reaches this annotation.
type Frame = Any


@dataclass(frozen=True, slots=True)
class MediaProperties:

    """

    The measurements a decoded medium carries into its re-encoding.


    Attributes
    ----------
    frame_count : int
        The number of frames the medium holds; a still image holds one.

    width : int
        The frame width in pixels.

    height : int
        The frame height in pixels.

    frames_per_second : float | None
        The playback rate, which only a moving medium has.

    """

    frame_count: int
    width: int
    height: int
    frames_per_second: float | None = None

    def __post_init__(self) -> None:

        """

        Rejects geometry no encoder could write back.

        """

        if self.frame_count < 0:
            raise ValueError(f"frame_count must not be negative. Received: {self.frame_count} with type {type(self.frame_count)}")
        if self.width <= 0:
            raise ValueError(f"width must be positive. Received: {self.width} with type {type(self.width)}")
        if self.height <= 0:
            raise ValueError(f"height must be positive. Received: {self.height} with type {type(self.height)}")
        if self.frames_per_second is not None and self.frames_per_second <= 0:
            raise ValueError(f"frames_per_second must be positive. Received: {self.frames_per_second} with type {type(self.frames_per_second)}")


@dataclass(frozen=True)
class MediaStream:

    """

    A decoded medium, holding its measurements and its frames as one iterator.

    A live iterator has nothing to validate and cannot survive a copy, so this
    one schema was already a frozen dataclass before the others were
    (see decision 0043). Reading a medium twice means asking the codec twice.


    Attributes
    ----------
    properties : MediaProperties
        The measurements the encoder needs to write the medium back.

    frames : Iterator[Frame]
        The decoded frames, consumable exactly once.

    """

    properties: MediaProperties
    frames: Iterator[Frame] = field(default_factory=lambda: iter(()))
