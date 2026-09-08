import numpy as np

from cvaugmentor.adapters.augmentations.frames import as_pixels, blur
from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

RADIUS_RANGE = (0.0, 5.0)


class Blur:

    """

    Softens a frame with three box passes.


    Usage
    -----
    The radius is the standard deviation the softening approximates, and an
    unspecified one is drawn once per instance, so every frame of a video is
    softened by the same amount. Three box passes converge on a Gaussian and
    cost the same at every radius, which is the construction Pillow's own
    Gaussian blur uses underneath. Passing a seed fixes every draw this
    instance makes, including the ones a later redraw asks for, so a dataset
    built from unspecified settings can be built again.
    ```python
    from cvaugmentor import augmentations as aug

    blurred = aug.Blur(2.5).apply(frame)
    repeatable = aug.Blur(seed=7)
    ```

    """

    name: str = "blur"

    radius: float


    def __init__(self, radius: int | float | None = None, seed: int | None = None) -> None:

        """

        Constructor for the Blur class.


        Parameters
        ----------
        radius : int | float | None, optional
            The kernel's standard deviation. Drawn from [0, 5] when None.

        seed : int | None, optional
            Fixes every draw this instance makes. Drawn unpredictably when
            None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `radius` is not a number or is negative, or `seed` is not a
            non-negative integer.

        """

        if radius is not None and not isinstance(radius, (int, float)):
            raise ValueError(f"radius must be a number. Received: {radius} with type {type(radius)}")
        if radius is not None and radius < 0:
            raise ValueError(f"radius must not be negative. Received: {radius} with type {type(radius)}")
        if seed is not None and not isinstance(seed, int):
            raise ValueError(f"seed must be an integer. Received: {seed} with type {type(seed)}")
        if seed is not None and seed < 0:
            raise ValueError(f"seed must not be negative. Received: {seed} with type {type(seed)}")


        self._requested_radius = radius
        self._rng = np.random.default_rng(seed)
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
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        return blur(as_pixels(frame), self.radius)


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
