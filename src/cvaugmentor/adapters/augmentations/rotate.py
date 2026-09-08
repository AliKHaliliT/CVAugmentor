import math

import numpy as np

from cvaugmentor.adapters.augmentations.frames import Pixels, as_pixels
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.schemas.media import Frame

FULL_TURN = 360.0
QUARTER_TURN = 90.0
# Pillow rounded both trigonometric terms to fifteen decimals before it built its matrix,
# which is what turns the 6e-17 that the cosine of a right angle really is into the zero a
# quarter turn needs. The rounding is kept here for the same reason: it is what holds a
# quarter turn of a rectangle, which the shortcut below cannot take, on whole pixels.
TERM_DECIMALS = 15


class Rotate:

    """

    Turns a frame about its centre.


    Usage
    -----
    The frame keeps its original size, so a rotation that is not a multiple of
    a quarter turn leaves black corners where the frame no longer covers the
    canvas. A half turn of any frame and a quarter turn of a square one only
    reorder bytes; every other angle takes the nearest source pixel, which is
    the sampling Pillow's own rotation defaulted to and what keeps a turned
    edge as hard as it started.
    ```python
    from cvaugmentor import augmentations as aug

    turned = aug.Rotate(90).apply(frame)
    ```

    """

    name: str = "rotate"

    angle: float


    def __init__(self, angle: int | float = 90) -> None:

        """

        Constructor for the Rotate class.


        Parameters
        ----------
        angle : int | float, optional
            The counter-clockwise angle in degrees.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `angle` is not a number.

        """

        if not isinstance(angle, (int, float)):
            raise ValueError(f"angle must be a number. Received: {angle} with type {type(angle)}")


        self.angle = float(angle)


    def apply(self, frame: Frame) -> Frame:

        """

        Turns the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The turned frame, at its original size.


        Raises
        ------
        TypeError
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        height, width = pixels.shape[0], pixels.shape[1]
        angle = self.angle % FULL_TURN
        turns = int(angle // QUARTER_TURN)

        # A turn that lands the frame back on its own canvas is a reordering of bytes, so it
        # is taken by strides and resamples nothing. A quarter turn of a rectangle keeps the
        # size it started with rather than trading its sides, so it crops, and only the
        # general turn below crops.
        if angle == turns * QUARTER_TURN and (turns % 2 == 0 or width == height):
            return np.ascontiguousarray(np.rot90(pixels, turns))

        # The turn reads from output pixel back to source pixel, which is the direction
        # Pillow's matrix read, about a centre that is the frame's own. Pillow sampled the
        # centre of each output pixel and floored, so the source of the output pixel at
        # (x, y) is floor(a * (x + 0.5) + b * (y + 0.5) + shift) on each axis.
        radians = math.radians(angle)
        cosine = round(math.cos(radians), TERM_DECIMALS)
        sine = round(math.sin(radians), TERM_DECIMALS)
        centre_x, centre_y = width / 2, height / 2
        shift_x = centre_x - cosine * centre_x + sine * centre_y
        shift_y = centre_y - sine * centre_x - cosine * centre_y

        columns = np.arange(width) + 0.5
        rows = np.arange(height) + 0.5
        source_x = np.floor(cosine * columns + (shift_x - sine * rows[:, None])).astype(np.int32)
        source_y = np.floor(sine * columns + (shift_y + cosine * rows[:, None])).astype(np.int32)

        accelerated = opencv()
        if accelerated is not None:
            # The maps hold whole numbers, so nearest resampling returns exactly the pixel
            # the map names and OpenCV's own rounding never enters.
            turned: Pixels = accelerated.remap(pixels,
                                               source_x.astype(np.float32),
                                               source_y.astype(np.float32),
                                               interpolation=accelerated.INTER_NEAREST,
                                               borderMode=accelerated.BORDER_CONSTANT,
                                               borderValue=(0, 0, 0))
            return turned

        covered = (source_x >= 0) & (source_x < width) & (source_y >= 0) & (source_y < height)

        gathered = np.zeros(pixels.shape, np.uint8)
        gathered[covered] = pixels[source_y[covered], source_x[covered]]

        return gathered


    def reseed(self) -> None:

        """

        Draws nothing, because the angle is chosen rather than drawn.


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
