from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

MediaKind = Literal["image", "video"]

# The opaque pixel payload the codecs and the augmentations agree on, and that nothing in
# the domain or the services ever inspects. Naming the concrete carrier here would drag an
# imaging SDK across the Dependency Rule, so the core moves frames it cannot read
# (see decision 0042).
type Frame = Any


class MediaProperties(BaseModel):

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

    frame_count: int = Field(ge=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    frames_per_second: float | None = Field(default=None, gt=0)

    model_config = ConfigDict(frozen=True)


@dataclass(frozen=True)
class MediaStream:

    """

    A decoded medium, holding its measurements and its frames as one iterator.

    A live iterator has nothing to validate and cannot survive a copy, so this
    one schema is a frozen dataclass while every other is a Pydantic model
    (see decision 0043). Reading a medium twice means asking the codec twice.


    Attributes
    ----------
    properties : MediaProperties
        The measurements the encoder needs to write the medium back.

    frames : Iterator[Frame]
        The decoded frames, consumable exactly once.

    """

    properties: MediaProperties
    frames: Iterator[Frame]
