import numpy as np
from PIL import Image

from cvaugmentor.domain.schemas.media import Frame

COUNT_RANGE = (1, 6)
SIZE_DIVISOR = 4
SEED_LIMIT = 2**32


class Cutout:

    """

    Punches black squares out of a frame.


    Usage
    -----
    Every square is drawn from one seeded generator, so a count above one
    really does place that many squares in different spots, and a video of one
    size loses the same squares on every frame. An unspecified size is scaled
    to the frame it lands on.
    ```python
    from cvaugmentor import augmentations as aug

    punched = aug.Cutout(max_size=64, max_count=6).apply(frame)
    ```

    """

    name: str = "cutout"

    max_count: int


    def __init__(self, max_size: int | None = None, max_count: int | None = None) -> None:

        """

        Constructor for the Cutout class.


        Parameters
        ----------
        max_size : int | None, optional
            The side of each square in pixels. Scaled to a quarter of the
            frame's shorter side when None.

        max_count : int | None, optional
            How many squares to punch. Drawn from [1, 5] when None.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `max_size` or `max_count` is not a positive integer.

        """

        if max_size is not None and (not isinstance(max_size, int) or max_size < 1):
            raise ValueError(f"max_size must be a positive integer. Received: {max_size} with type {type(max_size)}")
        if max_count is not None and (not isinstance(max_count, int) or max_count < 1):
            raise ValueError(f"max_count must be a positive integer. Received: {max_count} with type {type(max_count)}")


        self.max_size = max_size
        self._requested_count = max_count
        self._rng = np.random.default_rng()
        self._seed = int(self._rng.integers(0, SEED_LIMIT))
        self.reseed()


    def apply(self, frame: Frame) -> Frame:

        """

        Punches the squares out of the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The punched frame.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        rng = np.random.default_rng(self._seed)
        channels = np.array(frame)
        height, width = channels.shape[0], channels.shape[1]

        if self.max_size is not None:
            side = self.max_size
        else:
            side = int(rng.integers(1, max(min(width, height) // SIZE_DIVISOR, 2)))
        side = min(side, width, height)

        for _ in range(self.max_count):
            top = int(rng.integers(0, height - side + 1))
            left = int(rng.integers(0, width - side + 1))
            channels[top:top + side, left:left + side] = 0

        return Image.fromarray(channels)


    def reseed(self) -> None:

        """

        Redraws the count when none was specified, and the placement always.


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

        if self._requested_count is not None:
            self.max_count = self._requested_count
            return None

        self.max_count = int(self._rng.integers(*COUNT_RANGE))

        return None
