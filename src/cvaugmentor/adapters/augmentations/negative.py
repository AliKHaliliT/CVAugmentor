from cvaugmentor.adapters.augmentations.frames import as_pixels
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.schemas.media import Frame


class Negative:

    """

    Inverts every pixel value in a frame.


    Usage
    -----
    Inversion is its own opposite, so applying this augmentation twice returns
    the frame it started from. Subtracting each byte from 255 is exact at every
    level, so the accelerated and the fallback paths agree to the bit.
    ```python
    from cvaugmentor import augmentations as aug

    inverted = aug.Negative().apply(frame)
    ```

    """

    name: str = "negative"


    def apply(self, frame: Frame) -> Frame:

        """

        Inverts the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The inverted frame.


        Raises
        ------
        TypeError
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        pixels = as_pixels(frame)
        accelerated = opencv()
        if accelerated is not None:
            return accelerated.bitwise_not(pixels)

        return 255 - pixels


    def reseed(self) -> None:

        """

        Draws nothing, because this augmentation has no random parameter.


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

        return None
