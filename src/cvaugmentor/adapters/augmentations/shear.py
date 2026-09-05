import numpy as np
from PIL import Image

from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

SHEAR_LIMIT = 1.0
DRAW_RANGE = (-0.5, 0.5)


class Shear:

    """

    Slants a frame along one or both axes.


    Usage
    -----
    The two values slant along x and y, the frame keeps its original size, and
    whatever slides off the canvas is lost to black. An unspecified pair is
    drawn once per instance.
    ```python
    from cvaugmentor import augmentations as aug

    slanted = aug.Shear((0.2, 0.2)).apply(frame)
    ```

    """

    name: str = "shear"

    shear: tuple[float, float]


    def __init__(self, shear: tuple[int | float, int | float] | None = None) -> None:

        """

        Constructor for the Shear class.


        Parameters
        ----------
        shear : tuple[int | float, int | float] | None, optional
            The slant along x and y, each between -1 and 1. Drawn from
            [-0.5, 0.5] when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `shear` is not a pair of numbers within [-1, 1].

        """

        if shear is not None:
            if not isinstance(shear, tuple) or len(shear) != 2:
                raise ValueError(f"shear must be a tuple of two numbers. Received: {shear} with type {type(shear)}")
            if not all(isinstance(value, (int, float)) and -SHEAR_LIMIT <= value <= SHEAR_LIMIT for value in shear):
                raise ValueError(f"shear values must be numbers between -{SHEAR_LIMIT} and {SHEAR_LIMIT}. Received: {shear}")


        self._requested_shear = shear
        self._rng = np.random.default_rng()
        self.reseed()

        if not all(DRAW_RANGE[0] <= value <= DRAW_RANGE[1] for value in self.shear):
            logger.warning(f"A shear outside {DRAW_RANGE} pushes most of the frame off the canvas. Received: {self.shear}")


    def apply(self, frame: Frame) -> Frame:

        """

        Slants the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The slanted frame, at its original size.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        matrix = (1, self.shear[0], 0, self.shear[1], 1, 0)

        return frame.transform(frame.size, Image.Transform.AFFINE, matrix)


    def reseed(self) -> None:

        """

        Redraws the slant when none was specified.


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

        if self._requested_shear is not None:
            self.shear = (float(self._requested_shear[0]), float(self._requested_shear[1]))
            return None

        self.shear = (float(self._rng.uniform(*DRAW_RANGE)), float(self._rng.uniform(*DRAW_RANGE)))

        return None
