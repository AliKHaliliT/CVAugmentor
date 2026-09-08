import numpy as np
import numpy.typing as npt

from cvaugmentor.adapters.augmentations.frames import SEED_LIMIT, as_pixels
from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

INTENSITY_RANGE = (-1.0, 1.0)
FULL_RANGE = 255.0


class Noise:

    """

    Speckles a frame the way an analogue signal with poor reception does.


    Usage
    -----
    The speckle is drawn once for the first frame's size rather than once per
    frame, so every frame of a video of one size receives the same speckle and
    the result does not crawl between frames. The draw comes from this
    instance's own generator, so nothing another thread does moves it. Passing
    a seed fixes every draw this instance makes, including the ones a later
    redraw asks for, so a dataset built from unspecified settings can be built
    again.
    ```python
    from cvaugmentor import augmentations as aug

    speckled = aug.Noise(0.4).apply(frame)
    repeatable = aug.Noise(seed=7)
    ```

    """

    name: str = "noise"

    intensity: float


    def __init__(self, intensity: int | float | None = None, seed: int | None = None) -> None:

        """

        Constructor for the Noise class.


        Parameters
        ----------
        intensity : int | float | None, optional
            How far the speckle moves a channel, as a fraction of full range.
            Drawn from [-1, 1] when None.

        seed : int | None, optional
            Fixes every draw this instance makes. Drawn unpredictably when
            None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `intensity` is not a number, or `seed` is not a non-negative
            integer.

        """

        if intensity is not None and not isinstance(intensity, (int, float)):
            raise ValueError(f"intensity must be a number. Received: {intensity} with type {type(intensity)}")
        if seed is not None and not isinstance(seed, int):
            raise ValueError(f"seed must be an integer. Received: {seed} with type {type(seed)}")
        if seed is not None and seed < 0:
            raise ValueError(f"seed must not be negative. Received: {seed} with type {type(seed)}")


        self._requested_intensity = intensity
        self._rng = np.random.default_rng(seed)
        self._speckle: npt.NDArray[np.float32] | None = None
        self.reseed()

        if not INTENSITY_RANGE[0] <= self.intensity <= INTENSITY_RANGE[1]:
            logger.warning(f"A noise intensity outside {INTENSITY_RANGE} saturates the frame. Received: {self.intensity}")


    def apply(self, frame: Frame) -> Frame:

        """

        Speckles the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The speckled frame.


        Raises
        ------
        TypeError
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)

        if self._speckle is None or self._speckle.shape != pixels.shape:
            # Built from a value drawn once rather than from the instance's own generator,
            # so two instances holding the same seed stay in step however many frames each
            # has already speckled (see decision 0057).
            self._speckle = np.random.default_rng(self._speckle_seed).random(pixels.shape, dtype=np.float32)

        # The sum promotes to float32 into a buffer of its own, so the frame that arrived is
        # read and never written.
        return np.clip(pixels + self._speckle * (self.intensity * FULL_RANGE), 0.0, FULL_RANGE).astype(np.uint8)


    def reseed(self) -> None:

        """

        Redraws the intensity when none was specified, and the speckle always.


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

        self._speckle = None
        self._speckle_seed = int(self._rng.integers(0, SEED_LIMIT))

        if self._requested_intensity is not None:
            self.intensity = float(self._requested_intensity)
            return None

        self.intensity = float(self._rng.uniform(*INTENSITY_RANGE))

        return None
