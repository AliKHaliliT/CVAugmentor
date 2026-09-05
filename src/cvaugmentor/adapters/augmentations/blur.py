import numpy as np
from PIL import Image, ImageFilter

from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

RADIUS_RANGE = (0.0, 5.0)


class Blur:

    """

    Softens a frame with a Gaussian kernel.


    Usage
    -----
    The radius is the standard deviation of the kernel, and an unspecified one
    is drawn once per instance, so every frame of a video is softened by the
    same amount.
    ```python
    from cvaugmentor import augmentations as aug

    blurred = aug.Blur(2.5).apply(frame)
    ```

    """

    name: str = "blur"

    radius: float


    def __init__(self, radius: int | float | None = None) -> None:

        """

        Constructor for the Blur class.


        Parameters
        ----------
        radius : int | float | None, optional
            The kernel's standard deviation. Drawn from [0, 5] when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `radius` is not a number, or is negative.

        """

        if radius is not None and not isinstance(radius, (int, float)):
            raise ValueError(f"radius must be a number. Received: {radius} with type {type(radius)}")
        if radius is not None and radius < 0:
            raise ValueError(f"radius must not be negative. Received: {radius} with type {type(radius)}")


        self._requested_radius = radius
        self._rng = np.random.default_rng()
        self.reseed()

        if self.radius > RADIUS_RANGE[1]:
            logger.warning(f"A blur radius above {RADIUS_RANGE[1]} rarely leaves anything legible. Received: {self.radius}")


    def apply(self, frame: Frame) -> Frame:

        """

        Softens the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The softened frame.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        return frame.filter(ImageFilter.GaussianBlur(self.radius))


    def reseed(self) -> None:

        """

        Redraws the radius when none was specified.


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

        if self._requested_radius is not None:
            self.radius = float(self._requested_radius)
            return None

        self.radius = float(self._rng.uniform(*RADIUS_RANGE))

        return None
