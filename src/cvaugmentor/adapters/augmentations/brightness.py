import numpy as np
from PIL import Image, ImageEnhance

from cvaugmentor.domain.schemas.media import Frame

FACTOR_RANGE = (0.0, 0.5)


class Brightness:

    """

    Lightens or darkens a frame.


    Usage
    -----
    The factor is an offset from the frame as it is, so 0 leaves it alone,
    a positive factor lightens it, and -1 takes it to black. An unspecified
    factor is drawn once per instance.
    ```python
    from cvaugmentor import augmentations as aug

    brightened = aug.Brightness(0.25).apply(frame)
    ```

    """

    name: str = "brightness"

    brightness_factor: float


    def __init__(self, brightness_factor: int | float | None = None) -> None:

        """

        Constructor for the Brightness class.


        Parameters
        ----------
        brightness_factor : int | float | None, optional
            The offset applied to the frame's brightness. Drawn from [0, 0.5]
            when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `brightness_factor` is not a number, or is below -1.

        """

        if brightness_factor is not None and not isinstance(brightness_factor, (int, float)):
            raise ValueError(f"brightness_factor must be a number. Received: {brightness_factor} with type {type(brightness_factor)}")
        if brightness_factor is not None and brightness_factor < -1:
            raise ValueError(f"brightness_factor must not be below -1. Received: {brightness_factor} with type {type(brightness_factor)}")


        self._requested_factor = brightness_factor
        self._rng = np.random.default_rng()
        self.reseed()


    def apply(self, frame: Frame) -> Frame:

        """

        Adjusts the frame's brightness.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The adjusted frame.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        return ImageEnhance.Brightness(frame).enhance(1 + self.brightness_factor)


    def reseed(self) -> None:

        """

        Redraws the factor when none was specified.


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

        if self._requested_factor is not None:
            self.brightness_factor = float(self._requested_factor)
            return None

        self.brightness_factor = float(self._rng.uniform(*FACTOR_RANGE))

        return None
