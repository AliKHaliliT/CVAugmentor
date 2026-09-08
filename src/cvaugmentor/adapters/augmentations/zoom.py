import numpy as np
import numpy.typing as npt

from cvaugmentor.adapters.augmentations.frames import Pixels, as_pixels
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.schemas.media import Frame

NEAR_DIVISOR = 1.5
FAR_DIVISOR = 2.5
SEED_LIMIT = 2**32
# The term that shapes the cubic kernel, and the one OpenCV's own cubic resize carries.
# Pillow's resize carried -0.5, whose negative lobes are shallower, so a stretched window
# now comes out a shade sharper than 1.x drew it. Both paths hold the same term, which is
# what keeps them inside a single level of each other.
CUBIC_TERM = -0.75
# The kernel reaches two pixels each way, so a sample is a blend of four along an axis.
TAP_OFFSETS = np.arange(-1, 3)


def _taps(length: int, source_length: int) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.float32]]:

    """

    The four source pixels each output pixel blends along one axis, and their weights.


    Parameters
    ----------
    length : int
        The number of output pixels along the axis.

    source_length : int
        The number of source pixels along the axis.


    Returns
    -------
    tuple[npt.NDArray[np.intp], npt.NDArray[np.float32]]
        The four source indices per output pixel, and the four weights.


    Raises
    ------
    None.

    """

    # The centre of an output pixel maps onto the centre of the source pixel it came from,
    # which is the alignment both Pillow's resize and OpenCV's hold; aligning the corners
    # instead would slide the whole window by half an output pixel. A kernel that reaches
    # past an edge reads the edge pixel again, and the fraction is left alone while it does,
    # which is what OpenCV's cubic does and its linear does not.
    coordinates = (np.arange(length) + 0.5) * (source_length / length) - 0.5
    base = np.floor(coordinates)
    fraction = (coordinates - base).astype(np.float32)
    taps = np.clip(base[:, None].astype(np.intp) + TAP_OFFSETS, 0, source_length - 1)

    term, ahead = np.float32(CUBIC_TERM), np.float32(1.0) - fraction
    weights = np.empty((length, TAP_OFFSETS.size), np.float32)
    weights[:, 0] = ((term * (fraction + 1) - 5 * term) * (fraction + 1) + 8 * term) * (fraction + 1) - 4 * term
    weights[:, 1] = ((term + 2) * fraction - (term + 3)) * fraction * fraction + 1
    weights[:, 2] = ((term + 2) * ahead - (term + 3)) * ahead * ahead + 1
    # The four weights sum to one, so the last one is what the other three leave rather
    # than a fourth evaluation of the kernel.
    weights[:, 3] = 1 - weights[:, 0] - weights[:, 1] - weights[:, 2]

    return taps, weights


def _stretch(pixels: Pixels, width: int, height: int) -> Pixels:

    """

    Stretches a frame to a size through the cubic kernel, one axis at a time.


    Parameters
    ----------
    pixels : Pixels
        The frame to stretch, as an HxWx3 uint8 array in RGB order.

    width : int
        The width to stretch to.

    height : int
        The height to stretch to.


    Returns
    -------
    Pixels
        The stretched frame, as an HxWx3 uint8 array in RGB order.


    Raises
    ------
    None.

    """

    row_taps, row_weights = _taps(height, pixels.shape[0])
    column_taps, column_weights = _taps(width, pixels.shape[1])

    # The kernel is separable, so the stretch is two passes of four weighted reads rather
    # than one pass of sixteen, and each pass accumulates a tap at a time so the working
    # buffer stays the size of the frame rather than four times it.
    channels = pixels.astype(np.float32)
    along_x = np.zeros((pixels.shape[0], width, 3), np.float32)
    for tap in range(TAP_OFFSETS.size):
        along_x += channels[:, column_taps[:, tap]] * column_weights[None, :, tap, None]

    stretched = np.zeros((height, width, 3), np.float32)
    for tap in range(TAP_OFFSETS.size):
        stretched += along_x[row_taps[:, tap]] * row_weights[:, tap, None, None]

    # The negative lobes of a cubic kernel overshoot both ends of the range at an edge, so
    # the clip is what a saturating cast does for the accelerated path.
    blended: Pixels = np.clip(np.rint(stretched), 0.0, 255.0).astype(np.uint8)

    return blended


class Zoom:

    """

    Crops a window out of a frame and stretches it back to full size.


    Usage
    -----
    The window is placed by a seeded generator, so a video of one size is
    cropped in the same place on every frame. An unspecified window is scaled
    to the frame it lands on, and one larger than the frame is clamped to it.
    The stretch runs through a cubic kernel, which is what Pillow's own resize
    defaulted to and what keeps a magnified window from turning blocky; both
    paths carry the same kernel, so they agree to within a level.
    ```python
    from cvaugmentor import augmentations as aug

    zoomed = aug.Zoom((128, 128)).apply(frame)
    ```

    """

    name: str = "zoom"

    zoom_size: tuple[int, int] | None


    def __init__(self, zoom_size: tuple[int, int] | None = None) -> None:

        """

        Constructor for the Zoom class.


        Parameters
        ----------
        zoom_size : tuple[int, int] | None, optional
            The width and height of the window to crop. Scaled to between a
            half and two fifths of the frame's shorter side when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `zoom_size` is not a pair of positive integers.

        """

        if zoom_size is not None:
            if not isinstance(zoom_size, tuple) or len(zoom_size) != 2:
                raise ValueError(f"zoom_size must be a tuple of two integers. Received: {zoom_size} with type {type(zoom_size)}")
            if not all(isinstance(value, int) and value > 0 for value in zoom_size):
                raise ValueError(f"zoom_size values must be positive integers. Received: {zoom_size}")


        self.zoom_size = zoom_size
        self._rng = np.random.default_rng()
        self._seed = int(self._rng.integers(0, SEED_LIMIT))


    def apply(self, frame: Frame) -> Frame:

        """

        Crops a window and stretches it over the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The zoomed frame, at its original size.


        Raises
        ------
        TypeError
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        rng = np.random.default_rng(self._seed)
        height, width = pixels.shape[0], pixels.shape[1]

        if self.zoom_size is not None:
            window = (min(self.zoom_size[0], width), min(self.zoom_size[1], height))
        else:
            shortest = min(width, height)
            near, far = max(int(shortest / FAR_DIVISOR), 1), max(int(shortest / NEAR_DIVISOR), 2)
            window = (int(rng.integers(near, far)), int(rng.integers(near, far)))

        left = int(rng.integers(0, width - window[0] + 1))
        top = int(rng.integers(0, height - window[1] + 1))
        # The crop is a view, and every path below reads it rather than writing it, so it
        # costs no copy of its own.
        cropped = pixels[top:top + window[1], left:left + window[0]]

        accelerated = opencv()
        if accelerated is not None:
            # A cubic kernel over four samples an axis is what Pillow's resize reached for
            # by default, and dropping to a linear one here would visibly soften a window
            # this method has just magnified.
            stretched: Pixels = accelerated.resize(cropped, (width, height), interpolation=accelerated.INTER_CUBIC)
            return stretched

        return _stretch(cropped, width, height)


    def reseed(self) -> None:

        """

        Redraws where the window lands, and how big it is when unspecified.


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

        self._seed = int(self._rng.integers(0, SEED_LIMIT))

        return None
