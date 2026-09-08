import numpy as np

from cvaugmentor.adapters.augmentations.frames import as_pixels, grayscale
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.schemas.media import Frame

FACTOR_RANGE = (0.0, 0.5)


class Saturation:

    """

    Deepens or drains the colour in a frame.


    Usage
    -----
    The factor is an offset from the frame as it is, so 0 leaves it alone and
    -1 drains it to gray. An unspecified factor is drawn once per instance. The
    frame is blended against its own grayscale and extrapolated past it, which
    is the operation Pillow's colour enhancement always was; going through hue
    instead would quantise it to 180 levels and lose colour the blend keeps.
    Passing a seed fixes every draw this instance makes, including the ones
    a later redraw asks for, so a dataset built from unspecified settings
    can be built again.
    ```python
    from cvaugmentor import augmentations as aug

    saturated = aug.Saturation(0.5).apply(frame)
    repeatable = aug.Saturation(seed=7)
    ```

    """

    name: str = "saturation"

    saturation_factor: float


    def __init__(self, saturation_factor: int | float | None = None, seed: int | None = None) -> None:

        """

        Constructor for the Saturation class.


        Parameters
        ----------
        saturation_factor : int | float | None, optional
            The offset applied to the frame's colour intensity. Drawn from
            [0, 0.5] when None.

        seed : int | None, optional
            Fixes every draw this instance makes. Drawn unpredictably when
            None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `saturation_factor` is not a number or is below -1, or `seed`
            is not a non-negative integer.

        """

        if saturation_factor is not None and not isinstance(saturation_factor, (int, float)):
            raise ValueError(f"saturation_factor must be a number. Received: {saturation_factor} with type {type(saturation_factor)}")
        if saturation_factor is not None and saturation_factor < -1:
            raise ValueError(f"saturation_factor must not be below -1. Received: {saturation_factor} with type {type(saturation_factor)}")
        if seed is not None and not isinstance(seed, int):
            raise ValueError(f"seed must be an integer. Received: {seed} with type {type(seed)}")
        if seed is not None and seed < 0:
            raise ValueError(f"seed must not be negative. Received: {seed} with type {type(seed)}")


        self._requested_factor = saturation_factor
        self._rng = np.random.default_rng(seed)
        self.reseed()


    def apply(self, frame: Frame) -> Frame:

        """

        Adjusts the frame's colour intensity.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The adjusted frame.


        Raises
        ------
        TypeError
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        grey = grayscale(pixels)
        weight = 1.0 + self.saturation_factor

        accelerated = opencv()
        if accelerated is not None:
            return accelerated.addWeighted(pixels, weight, grey, 1.0 - weight, 0.0)

        deepened = grey.astype(np.float32) + (pixels.astype(np.float32) - grey) * weight

        return np.clip(deepened, 0, 255).astype(np.uint8)


    def reseed(self) -> None:

        """

        Redraws the factor when none was specified.


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

        if self._requested_factor is not None:
            self.saturation_factor = float(self._requested_factor)
            return None

        self.saturation_factor = float(self._rng.uniform(*FACTOR_RANGE))

        return None
