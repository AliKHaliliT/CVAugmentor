import numpy as np

from cvaugmentor.adapters.augmentations.frames import as_pixels
from cvaugmentor.domain.schemas.media import Frame

COUNT_RANGE = (1, 6)
SIZE_DIVISOR = 4


class Cutout:

    """

    Punches black squares out of a frame.


    Usage
    -----
    Every square's position is drawn once per redraw and kept as a fraction of
    the room it has, so a count above one really does place that many squares
    in different spots, and a video of one size loses the same squares on every
    frame. An unspecified size is scaled to the frame it lands on.
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
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        height, width = pixels.shape[0], pixels.shape[1]

        if self.max_size is not None:
            side = self.max_size
        else:
            # The draw is held as a fraction rather than a pixel count, because the frame it
            # will be scaled against is not known until one arrives.
            side = 1 + int(self._size_fraction * (max(min(width, height) // SIZE_DIVISOR, 2) - 1))
        side = min(side, width, height)

        # A copy, because a caller's frame is the caller's, and the black is written into it.
        punched = pixels.copy()
        for down, across in self._placements:
            top = int(down * (height - side + 1))
            left = int(across * (width - side + 1))
            punched[top:top + side, left:left + side] = 0

        return punched


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

        if self._requested_count is not None:
            self.max_count = self._requested_count
        else:
            self.max_count = int(self._rng.integers(*COUNT_RANGE))

        self._size_fraction = float(self._rng.random())
        self._placements: list[tuple[float, float]] = [(float(down), float(across)) for down, across in self._rng.random((self.max_count, 2))]

        return None
