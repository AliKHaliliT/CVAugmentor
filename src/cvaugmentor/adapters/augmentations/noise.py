import numpy as np
from PIL import Image

from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

INTENSITY_RANGE = (-1.0, 1.0)
SEED_LIMIT = 2**32


class Noise:

    """

    Speckles a frame the way an analogue signal with poor reception does.


    Usage
    -----
    The seed is drawn once per instance rather than the noise itself, so every
    frame of a video of one size receives the same speckle and the result does
    not crawl between frames.
    ```python
    from cvaugmentor import augmentations as aug

    speckled = aug.Noise(0.4).apply(frame)
    ```

    """

    name: str = "noise"

    intensity: float


    def __init__(self, intensity: int | float | None = None) -> None:

        """

        Constructor for the Noise class.


        Parameters
        ----------
        intensity : int | float | None, optional
            How far the speckle moves a channel, as a fraction of full range.
            Drawn from [-1, 1] when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `intensity` is not a number.

        """

        if intensity is not None and not isinstance(intensity, (int, float)):
            raise ValueError(f"intensity must be a number. Received: {intensity} with type {type(intensity)}")


        self._requested_intensity = intensity
        self._rng = np.random.default_rng()
        self._seed = int(self._rng.integers(0, SEED_LIMIT))
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
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        channels = np.asarray(frame, dtype=np.float32)
        speckle = np.random.default_rng(self._seed).random(channels.shape, dtype=np.float32)
        speckled = np.clip(channels + speckle * self.intensity * 255, 0, 255)

        return Image.fromarray(speckled.astype(np.uint8))


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

        self._seed = int(self._rng.integers(0, SEED_LIMIT))

        if self._requested_intensity is not None:
            self.intensity = float(self._requested_intensity)
            return None

        self.intensity = float(self._rng.uniform(*INTENSITY_RANGE))

        return None
