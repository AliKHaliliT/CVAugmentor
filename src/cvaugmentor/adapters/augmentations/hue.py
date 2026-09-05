import numpy as np
from PIL import Image

from cvaugmentor.domain.schemas.media import Frame

SHIFT_LIMIT = 360.0
HUE_WHEEL = 256


class Hue:

    """

    Rotates a frame's colours around the hue wheel.


    Usage
    -----
    The shift is given in degrees and wraps, so 360 and -360 both return the
    frame's own colours. An unspecified shift is drawn once per instance.
    ```python
    from cvaugmentor import augmentations as aug

    shifted = aug.Hue(-120).apply(frame)
    ```

    """

    name: str = "hue"

    hue_shift: float


    def __init__(self, hue_shift: int | float | None = None) -> None:

        """

        Constructor for the Hue class.


        Parameters
        ----------
        hue_shift : int | float | None, optional
            The rotation in degrees, between -360 and 360. Drawn from that
            range when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `hue_shift` is not a number, or falls outside [-360, 360].

        """

        if hue_shift is not None and not isinstance(hue_shift, (int, float)):
            raise ValueError(f"hue_shift must be a number. Received: {hue_shift} with type {type(hue_shift)}")
        if hue_shift is not None and not -SHIFT_LIMIT <= hue_shift <= SHIFT_LIMIT:
            raise ValueError(f"hue_shift must fall between -{SHIFT_LIMIT} and {SHIFT_LIMIT}. Received: {hue_shift} with type {type(hue_shift)}")


        self._requested_shift = hue_shift
        self._rng = np.random.default_rng()
        self.reseed()


    def apply(self, frame: Frame) -> Frame:

        """

        Rotates the frame's hues.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The rotated frame, in RGB.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        hue, saturation, value = frame.convert("HSV").split()
        rotated = np.mod(np.asarray(hue, dtype=np.int16) + self.hue_shift, HUE_WHEEL).astype(np.uint8)

        return Image.merge("HSV", (Image.fromarray(rotated, mode="L"), saturation, value)).convert("RGB")


    def reseed(self) -> None:

        """

        Redraws the shift when none was specified.


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

        if self._requested_shift is not None:
            self.hue_shift = float(self._requested_shift)
            return None

        self.hue_shift = float(self._rng.uniform(-SHIFT_LIMIT, SHIFT_LIMIT))

        return None
