import numpy as np
from PIL import Image

from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.schemas.media import Frame

logger = get_logger("adapters.augmentations")

FACTOR_RANGE = (0.3, 1.7)


class Exposure:

    """

    Scales how much light a frame appears to have received.


    Usage
    -----
    Every channel is multiplied by the factor and clipped back into range, so
    1 leaves the frame alone while a large factor blows the highlights out. An
    unspecified factor is drawn once per instance.
    ```python
    from cvaugmentor import augmentations as aug

    exposed = aug.Exposure(1.3).apply(frame)
    ```

    """

    name: str = "exposure"

    exposure_factor: float


    def __init__(self, exposure_factor: int | float | None = None) -> None:

        """

        Constructor for the Exposure class.


        Parameters
        ----------
        exposure_factor : int | float | None, optional
            The multiplier applied to every channel. Drawn from [0.3, 1.7]
            when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `exposure_factor` is not a number, or is negative.

        """

        if exposure_factor is not None and not isinstance(exposure_factor, (int, float)):
            raise ValueError(f"exposure_factor must be a number. Received: {exposure_factor} with type {type(exposure_factor)}")
        if exposure_factor is not None and exposure_factor < 0:
            raise ValueError(f"exposure_factor must not be negative. Received: {exposure_factor} with type {type(exposure_factor)}")


        self._requested_factor = exposure_factor
        self._rng = np.random.default_rng()
        self.reseed()

        if not FACTOR_RANGE[0] <= self.exposure_factor <= FACTOR_RANGE[1]:
            logger.warning(f"An exposure factor outside {FACTOR_RANGE} clips most of the frame. Received: {self.exposure_factor}")


    def apply(self, frame: Frame) -> Frame:

        """

        Rescales the frame's exposure.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The rescaled frame.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        exposed = np.clip(np.asarray(frame, dtype=np.float32) * self.exposure_factor, 0, 255)

        return Image.fromarray(exposed.astype(np.uint8))


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
            self.exposure_factor = float(self._requested_factor)
            return None

        self.exposure_factor = float(self._rng.uniform(*FACTOR_RANGE))

        return None
