from PIL import Image, ImageOps

from cvaugmentor.domain.schemas.media import Frame


class Negative:

    """

    Inverts every pixel value in a frame.


    Usage
    -----
    Inversion is its own opposite, so applying this augmentation twice returns
    the frame it started from.
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
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        return ImageOps.invert(frame.convert("RGB"))


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
