from cvaugmentor.adapters.augmentations.frames import as_pixels
from cvaugmentor.domain.schemas.media import Frame


class NoAugmentation:

    """

    Passes a frame through untouched.


    Usage
    -----
    In sequential mode this writes an unaltered copy alongside the augmented
    ones, which is how a dataset keeps its originals beside its variants
    without a separate copy step. The frame is still validated on the way
    through, so a carrier no other augmentation would accept is refused here
    too rather than reaching an encoder.
    ```python
    from cvaugmentor import augmentations as aug

    unchanged = aug.NoAugmentation().apply(frame)
    ```

    """

    name: str = "no_augmentation"


    def apply(self, frame: Frame) -> Frame:

        """

        Returns the frame as it arrived.


        Parameters
        ----------
        frame : Frame
            The frame to pass through.


        Returns
        -------
        Frame
            The same frame.


        Raises
        ------
        TypeError
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        return as_pixels(frame)


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
