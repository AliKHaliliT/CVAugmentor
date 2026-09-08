import numpy as np
import numpy.typing as npt

from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.schemas.media import Frame

Pixels = npt.NDArray[np.uint8]

# OpenCV's own BT.601 luminance coefficients in its own fixed point, the weights over
# 2^14 with half a unit added before the shift, rather than equivalent-looking integers of
# our own. Matching its arithmetic narrows the gap between the two paths to one level on
# roughly one pixel in a hundred, where OpenCV's vectorised kernel rounds differently from
# its documented scalar formula. It does not close the gap, so the suites pin a tolerance
# rather than equality (see decision 0054). Saturation blends against this grey and
# amplifies the gap by its own factor, which is why the coefficients live here once.
LUMINANCE = np.array([4899, 9617, 1868], np.uint32)
LUMINANCE_SHIFT = 14
LUMINANCE_HALF = 1 << (LUMINANCE_SHIFT - 1)


def as_pixels(frame: Frame) -> Pixels:

    """

    The frame as a validated HxWx3 uint8 RGB array, or a TypeError naming what arrived.

    """

    if not isinstance(frame, np.ndarray) or frame.ndim != 3 or frame.shape[2] != 3 or frame.dtype != np.uint8:
        raise TypeError(f"frame must be an HxWx3 uint8 array in RGB order. Received: {type(frame)} with shape {getattr(frame, 'shape', None)} and dtype {getattr(frame, 'dtype', None)}")

    return frame


def curve(mapping: npt.NDArray[np.uint8], pixels: Pixels) -> Pixels:

    """

    One 256-entry table applied to every channel, which is a table lookup either way.

    """

    accelerated = opencv()
    if accelerated is not None:
        looked_up: Pixels = accelerated.LUT(pixels, mapping)
        return looked_up

    return mapping[pixels]


def grayscale(pixels: Pixels) -> Pixels:

    """

    The luminance of every pixel, broadcast back across three channels.

    """

    accelerated = opencv()
    if accelerated is not None:
        spread: Pixels = accelerated.cvtColor(accelerated.cvtColor(pixels, accelerated.COLOR_RGB2GRAY),
                                              accelerated.COLOR_GRAY2RGB)
        return spread

    # broadcast_to returns a view, so the three channels cost one buffer rather than three.
    weighted = np.einsum("ijk,k->ij", pixels, LUMINANCE, dtype=np.uint32)
    weighted += LUMINANCE_HALF
    luminance = (weighted >> LUMINANCE_SHIFT).astype(np.uint8)

    return np.ascontiguousarray(np.broadcast_to(luminance[:, :, None], pixels.shape))


def _running_mean(values: npt.NDArray[np.uint32], radius: int, axis: int) -> npt.NDArray[np.uint32]:

    """

    A box mean along one axis through a running sum, whose cost ignores the radius.

    """

    length = values.shape[axis]
    lead = radius + 1
    padded_shape = list(values.shape)
    padded_shape[axis] = length + 2 * radius + 1
    padded = np.empty(padded_shape, np.uint32)

    inner: list[slice] = [slice(None)] * values.ndim
    edge: list[slice] = [slice(None)] * values.ndim
    inner[axis] = slice(lead, lead + length)
    padded[tuple(inner)] = values
    inner[axis] = slice(0, lead)
    edge[axis] = slice(0, 1)
    padded[tuple(inner)] = values[tuple(edge)]
    inner[axis] = slice(lead + length, None)
    edge[axis] = slice(length - 1, length)
    padded[tuple(inner)] = values[tuple(edge)]

    np.cumsum(padded, axis=axis, out=padded)

    high: list[slice] = [slice(None)] * values.ndim
    low: list[slice] = [slice(None)] * values.ndim
    high[axis] = slice(2 * radius + 1, 2 * radius + 1 + length)
    low[axis] = slice(0, length)
    # OpenCV's box filter rounds its mean where integer division would floor it, and three
    # passes turn that half-level into several, so the half is added before dividing.
    span = 2 * radius + 1
    windowed = padded[tuple(high)] - padded[tuple(low)]
    windowed += span // 2
    windowed //= span

    return windowed


def blur(pixels: Pixels, radius: float) -> Pixels:

    """

    Three box passes, which is what Pillow's Gaussian blur has always been underneath.

    """

    span = max(1, int(round(radius)))
    accelerated = opencv()
    if accelerated is not None:
        window = (2 * span + 1, 2 * span + 1)
        # OpenCV reflects at the border by default while the fallback replicates the edge
        # row, and three passes turn that disagreement into tens of levels along every
        # margin. Naming the border here is what keeps the two paths inside the tolerance.
        border = accelerated.BORDER_REPLICATE
        once = accelerated.blur(pixels, window, borderType=border)
        twice = accelerated.blur(once, window, borderType=border)
        softened: Pixels = accelerated.blur(twice, window, borderType=border)
        return softened

    working = pixels.astype(np.uint32)
    for _ in range(3):
        working = _running_mean(_running_mean(working, span, 0), span, 1)

    return working.astype(np.uint8)
