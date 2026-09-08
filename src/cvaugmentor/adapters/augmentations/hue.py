import numpy as np
import numpy.typing as npt

from cvaugmentor.adapters.augmentations.frames import Pixels, as_pixels
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.schemas.media import Frame

SHIFT_LIMIT = 360.0
# The wheel is a full turn of degrees, not the 256 levels Pillow's HSV carried and not the
# 180 an 8-bit OpenCV HSV carries. Both of those quantise the hue, and a quantised wheel
# does not survive a round trip: a zero shift through 8-bit HSV moves a pixel by up to five
# levels. Every path here therefore works in float32, which round-trips the whole 8-bit
# colour cube at zero error.
HUE_WHEEL = 360.0
SECTOR = 60.0
CHANNEL_OFFSETS = np.array([5.0, 3.0, 1.0], np.float32)


def _to_hsv(pixels: Pixels) -> tuple[npt.NDArray[np.float32], npt.NDArray[np.float32], npt.NDArray[np.float32]]:

    """

    Splits a frame into hue in degrees, saturation, and value.


    Parameters
    ----------
    pixels : Pixels
        The frame to split, as an HxWx3 uint8 array in RGB order.


    Returns
    -------
    tuple[npt.NDArray[np.float32], npt.NDArray[np.float32], npt.NDArray[np.float32]]
        The hue over [0, 360), the saturation over [0, 1], and the value on the
        scale the frame arrived on.


    Raises
    ------
    None.

    """

    channels = pixels.astype(np.float32)
    red, green, blue = channels[..., 0], channels[..., 1], channels[..., 2]
    value = channels.max(2)
    chroma = value - channels.min(2)
    # A grey pixel has no hue and would divide by zero, so it is given a divisor it never
    # uses and a hue of zero, which is the convention OpenCV's own conversion follows.
    span = np.where(chroma == 0.0, 1.0, chroma)
    hue = np.where(value == red, (green - blue) / span,
                   np.where(value == green, (blue - red) / span + 2.0,
                            (red - green) / span + 4.0))
    hue = np.where(chroma == 0.0, 0.0, hue * SECTOR) % HUE_WHEEL
    saturation = np.where(value == 0.0, 0.0, chroma / np.where(value == 0.0, 1.0, value))

    return hue.astype(np.float32), saturation.astype(np.float32), value


def _to_rgb(hue: npt.NDArray[np.float32], saturation: npt.NDArray[np.float32], value: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:

    """

    Rebuilds RGB from hue in degrees, saturation, and value.


    Parameters
    ----------
    hue : npt.NDArray[np.float32]
        The hue in degrees.

    saturation : npt.NDArray[np.float32]
        The saturation over [0, 1].

    value : npt.NDArray[np.float32]
        The value, on the scale the result is wanted on.


    Returns
    -------
    npt.NDArray[np.float32]
        The three channels in RGB order, unrounded.


    Raises
    ------
    None.

    """

    # Each channel is one ramp over the wheel, offset by a third of it, so the three come out
    # of one clip rather than out of a six-way branch on the sector.
    wrapped = (hue[..., None] / SECTOR + CHANNEL_OFFSETS) % 6.0
    ramp = np.clip(np.minimum(wrapped, 4.0 - wrapped), 0.0, 1.0)

    return np.asarray(value[..., None] - (value * saturation)[..., None] * ramp, np.float32)


class Hue:

    """

    Rotates a frame's colours around the hue wheel.


    Usage
    -----
    The shift is given in degrees and wraps, so 0, 360, and -360 all return the
    frame's own bytes untouched. An unspecified shift is drawn once per
    instance. The rotation runs through a float32 HSV either way, because the
    8-bit one holds half a degree per level and would move a pixel even where
    the shift is nothing.
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
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        accelerated = opencv()

        if accelerated is not None:
            # The cast copies, and the conversion allocates again, so the hue is turned in
            # place on a buffer of this method's own and never on the caller's frame.
            hsv = accelerated.cvtColor(pixels.astype(np.float32), accelerated.COLOR_RGB2HSV)
            hsv[..., 0] = np.mod(hsv[..., 0] + self._rotation, HUE_WHEEL)
            # convertScaleAbs rounds to the nearest byte, where a plain cast would truncate
            # and lose the round trip this whole path is built to keep.
            rotated: Pixels = accelerated.convertScaleAbs(accelerated.cvtColor(hsv, accelerated.COLOR_HSV2RGB))
            return rotated

        hue, saturation, value = _to_hsv(pixels)

        return np.clip(np.rint(_to_rgb(np.mod(hue + self._rotation, HUE_WHEEL), saturation, value)), 0.0, 255.0).astype(np.uint8)


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
        else:
            self.hue_shift = float(self._rng.uniform(-SHIFT_LIMIT, SHIFT_LIMIT))

        # Folded here rather than per frame, so a shift of a whole turn is a rotation of
        # nothing by the time any pixel sees it.
        self._rotation = self.hue_shift % HUE_WHEEL

        return None
