import numpy as np
import numpy.typing as npt

from cvaugmentor.adapters.augmentations.frames import Pixels, as_pixels
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

SHEAR_LIMIT = 1.0
DRAW_RANGE = (-0.5, 0.5)


def _offsets(coefficient: float, count: int) -> npt.NDArray[np.int32]:

    """

    The whole-pixel offset per row or column, in the fixed point Pillow accumulated in.


    Parameters
    ----------
    coefficient : float
        The shear along the axis being offset.

    count : int
        How many rows or columns to produce an offset for.


    Returns
    -------
    npt.NDArray[np.int32]
        One whole-pixel offset per row or column.


    Raises
    ------
    None.

    """

    # Pillow walked each scanline in 16.16 fixed point, rounding the coefficient into it
    # once and stepping by that, so a coordinate landing on a pixel boundary falls a hair
    # to one side rather than wherever double arithmetic puts it. Reproducing the
    # accumulation, rather than the algebra it approximates, is what makes this bit-exact
    # with 1.x over every value tested (see decision 0055).
    step = int(np.rint(coefficient * 65536.0))
    half = (abs(step) + 1) // 2
    if step < 0:
        half = -half

    accumulated = step * np.arange(count, dtype=np.int64) + half + 32768

    return (accumulated >> 16).astype(np.int32)


class Shear:

    """

    Slants a frame along one or both axes.


    Usage
    -----
    The two values slant along x and y, the frame keeps its original size, and
    whatever slides off the canvas is lost to black. An unspecified pair is
    drawn once per instance. The slant takes the nearest source pixel rather
    than blending its neighbours, which is the sampling Pillow's own transform
    defaulted to and what keeps a slanted edge as hard as it started. Passing
    a seed fixes every draw this instance makes, including the ones a later
    redraw asks for, so a dataset built from unspecified settings can be built
    again.
    ```python
    from cvaugmentor import augmentations as aug

    slanted = aug.Shear((0.2, 0.2)).apply(frame)
    repeatable = aug.Shear(seed=7)
    ```

    """

    name: str = "shear"

    shear: tuple[float, float]


    def __init__(self, shear: tuple[int | float, int | float] | None = None, seed: int | None = None) -> None:

        """

        Constructor for the Shear class.


        Parameters
        ----------
        shear : tuple[int | float, int | float] | None, optional
            The slant along x and y, each between -1 and 1. Drawn from
            [-0.5, 0.5] when None.

        seed : int | None, optional
            Fixes every draw this instance makes. Drawn unpredictably when
            None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `shear` is not a pair of numbers within [-1, 1], or `seed` is
            not a non-negative integer.

        """

        if shear is not None:
            if not isinstance(shear, tuple) or len(shear) != 2:
                raise ValueError(f"shear must be a tuple of two numbers. Received: {shear} with type {type(shear)}")
            if not all(isinstance(value, (int, float)) and -SHEAR_LIMIT <= value <= SHEAR_LIMIT for value in shear):
                raise ValueError(f"shear values must be numbers between -{SHEAR_LIMIT} and {SHEAR_LIMIT}. Received: {shear}")
        if seed is not None and not isinstance(seed, int):
            raise ValueError(f"seed must be an integer. Received: {seed} with type {type(seed)}")
        if seed is not None and seed < 0:
            raise ValueError(f"seed must not be negative. Received: {seed} with type {type(seed)}")


        self._requested_shear = shear
        self._rng = np.random.default_rng(seed)
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
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        height, width = pixels.shape[0], pixels.shape[1]
        along_x, along_y = self.shear

        # The source coordinate is the output coordinate plus a per-row or per-column
        # whole-pixel offset, so the whole map reduces to two vectors.
        source_x = np.arange(width, dtype=np.int32)[None, :] + _offsets(along_x, height)[:, None]
        source_y = np.arange(height, dtype=np.int32)[:, None] + _offsets(along_y, width)[None, :]

        accelerated = opencv()
        if accelerated is not None:
            # The maps hold whole numbers, so nearest resampling returns exactly the pixel
            # the map names and OpenCV's own rounding never enters.
            slanted: Pixels = accelerated.remap(pixels,
                                                source_x.astype(np.float32),
                                                source_y.astype(np.float32),
                                                interpolation=accelerated.INTER_NEAREST,
                                                borderMode=accelerated.BORDER_CONSTANT,
                                                borderValue=(0, 0, 0))
            return slanted

        covered = (source_x >= 0) & (source_x < width) & (source_y >= 0) & (source_y < height)

        gathered = np.zeros(pixels.shape, np.uint8)
        gathered[covered] = pixels[source_y[covered], source_x[covered]]

        return gathered


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
