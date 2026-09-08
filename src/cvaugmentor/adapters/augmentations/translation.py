import math

import numpy as np

from cvaugmentor.adapters.augmentations.frames import as_pixels
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
    drawn once per instance. Taking the nearest source pixel, which is the
    sampling Pillow's own transform defaulted to, lands every offset on a whole
    pixel, so the slide is a block copy into a black canvas and nothing is
    resampled at any offset.
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
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        height, width = pixels.shape[0], pixels.shape[1]

        # The offsets are read from output pixel back to source pixel, which is the
        # direction Pillow's matrix read and why a positive offset subtracts. Pillow
        # sampled at the centre of the output pixel and truncated, and the nearest source
        # pixel of an output pixel at x is therefore x - ceil(offset - 0.5) whatever the
        # offset is, so a fractional offset is a whole-pixel slide too and no interpolation
        # is owed at any offset. The slide is then the overlap block copied into black,
        # which resamples nothing and reads each byte once.
        slide_x = math.ceil(self.translate[0] - 0.5)
        slide_y = math.ceil(self.translate[1] - 0.5)
        span_x = max(width - abs(slide_x), 0)
        span_y = max(height - abs(slide_y), 0)

        slid = np.zeros(pixels.shape, np.uint8)
        if span_x and span_y:
            into_x, from_x = max(slide_x, 0), max(-slide_x, 0)
            into_y, from_y = max(slide_y, 0), max(-slide_y, 0)
            slid[into_y:into_y + span_y, into_x:into_x + span_x] = pixels[from_y:from_y + span_y, from_x:from_x + span_x]

        return slid


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
