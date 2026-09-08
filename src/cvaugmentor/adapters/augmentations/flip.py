import numpy as np

from cvaugmentor.adapters.augmentations.frames import as_pixels
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.schemas.media import Frame

FLIP_TYPES = ("horizontal", "vertical")
# OpenCV reads a flip code rather than an axis: zero mirrors about the x axis, which is the
# top-to-bottom flip, and a positive code mirrors about the y axis.
FLIP_CODES = {"horizontal": 1, "vertical": 0}


class Flip:

    """

    Mirrors a frame across one axis.


    Usage
    -----
    A horizontal flip mirrors left to right, and a vertical flip mirrors top to
    bottom. The axis is a choice rather than a draw, so a flipped video stays
    flipped the same way for its whole length. A mirror reorders bytes and
    resamples nothing, so the accelerated and the fallback paths agree to the
    bit.
    ```python
    from cvaugmentor import augmentations as aug

    flipped = aug.Flip("horizontal").apply(frame)
    ```

    """

    name: str = "flip"

    flip_type: str


    def __init__(self, flip_type: str = "vertical") -> None:

        """

        Constructor for the Flip class.


        Parameters
        ----------
        flip_type : str, optional
            Which axis to mirror across, "horizontal" or "vertical".


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `flip_type` is neither "horizontal" nor "vertical".

        """

        if flip_type not in FLIP_TYPES:
            raise ValueError(f"flip_type must be one of {FLIP_TYPES}. Received: {flip_type} with type {type(flip_type)}")


        self.flip_type = flip_type


    def apply(self, frame: Frame) -> Frame:

        """

        Mirrors the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The mirrored frame.


        Raises
        ------
        TypeError
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        accelerated = opencv()
        if accelerated is not None:
            return accelerated.flip(pixels, FLIP_CODES[self.flip_type])

        # A NumPy mirror is a stride trick that hands back a view rather than a frame, and
        # a view is not something a codec downstream can write, so the copy is taken here.
        if self.flip_type == "horizontal":
            return np.ascontiguousarray(pixels[:, ::-1])

        return np.ascontiguousarray(pixels[::-1])


    def reseed(self) -> None:

        """

        Draws nothing, because the axis is chosen rather than drawn.


        Parameters
        ----------
        None.


        Returns
        -------
        None.


        Raises
        ------
        None.

        """

        return None
