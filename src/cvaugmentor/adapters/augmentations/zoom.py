import numpy as np
from PIL import Image

from cvaugmentor.domain.schemas.media import Frame

NEAR_DIVISOR = 1.5
FAR_DIVISOR = 2.5
SEED_LIMIT = 2**32


class Zoom:

    """

    Crops a window out of a frame and stretches it back to full size.


    Usage
    -----
    The window is placed by a seeded generator, so a video of one size is
    cropped in the same place on every frame. An unspecified window is scaled
    to the frame it lands on, and one larger than the frame is clamped to it.
    ```python
    from cvaugmentor import augmentations as aug

    zoomed = aug.Zoom((128, 128)).apply(frame)
    ```

    """

    name: str = "zoom"


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
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        rng = np.random.default_rng(self._seed)
        width, height = frame.size

        if self.zoom_size is not None:
            window = (min(self.zoom_size[0], width), min(self.zoom_size[1], height))
        else:
            shortest = min(width, height)
            near, far = max(int(shortest / FAR_DIVISOR), 1), max(int(shortest / NEAR_DIVISOR), 2)
            window = (int(rng.integers(near, far)), int(rng.integers(near, far)))

        left = int(rng.integers(0, width - window[0] + 1))
        top = int(rng.integers(0, height - window[1] + 1))
        cropped = frame.crop((left, top, left + window[0], top + window[1]))

        return cropped.resize((width, height), Image.Resampling.BICUBIC)


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
