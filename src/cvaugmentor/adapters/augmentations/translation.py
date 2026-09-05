import numpy as np
from PIL import Image

from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

DRAW_RANGE = (-50.0, 50.0)
ADVISED_LIMIT = 100.0


class Translation:

    """

    Slides a frame across its own canvas.


    Usage
    -----
    The two values are pixel offsets, positive x sliding the frame right and
    positive y sliding it down. The canvas does not move, so whatever slides
    off the edge is lost and black fills in behind it. An unspecified pair is
    drawn once per instance.
    ```python
    from cvaugmentor import augmentations as aug

    slid = aug.Translation((25, -10)).apply(frame)
    ```

    """

    name: str = "translation"

    translate: tuple[float, float]


    def __init__(self, translate: tuple[int | float, int | float] | None = None) -> None:

        """

        Constructor for the Translation class.


        Parameters
        ----------
        translate : tuple[int | float, int | float] | None, optional
            The offset along x and y in pixels. Drawn from [-50, 50] when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `translate` is not a pair of numbers.

        """

        if translate is not None:
            if not isinstance(translate, tuple) or len(translate) != 2:
                raise ValueError(f"translate must be a tuple of two numbers. Received: {translate} with type {type(translate)}")
            if not all(isinstance(value, (int, float)) for value in translate):
                raise ValueError(f"translate values must be numbers. Received: {translate}")


        self._requested_translate = translate
        self._rng = np.random.default_rng()
        self.reseed()

        if not all(abs(value) <= ADVISED_LIMIT for value in self.translate):
            logger.warning(f"A translation beyond {ADVISED_LIMIT} pixels slides most small frames off the canvas. Received: {self.translate}")


    def apply(self, frame: Frame) -> Frame:

        """

        Slides the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The slid frame, at its original size.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        # PIL reads an affine matrix backwards, from output pixel to source pixel, so the
        # offsets are negated to make a positive value slide the frame the way it reads.
        matrix = (1, 0, -self.translate[0], 0, 1, -self.translate[1])

        return frame.transform(frame.size, Image.Transform.AFFINE, matrix)


    def reseed(self) -> None:

        """

        Redraws the offset when none was specified.


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

        if self._requested_translate is not None:
            self.translate = (float(self._requested_translate[0]), float(self._requested_translate[1]))
            return None

        self.translate = (float(self._rng.uniform(*DRAW_RANGE)), float(self._rng.uniform(*DRAW_RANGE)))

        return None
