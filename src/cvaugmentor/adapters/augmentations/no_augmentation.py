from PIL import Image

from cvaugmentor.domain.schemas.media import Frame


class NoAugmentation:

    """

    Passes a frame through untouched.


    Usage
    -----
    In sequential mode this writes an unaltered copy alongside the augmented
    ones, which is how a dataset keeps its originals beside its variants
    without a separate copy step.
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
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        return frame


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
