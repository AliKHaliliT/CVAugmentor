from PIL import Image

from cvaugmentor.domain.schemas.media import Frame


class Grayscale:

    """

    Drains the colour from a frame, leaving it in RGB.


    Usage
    -----
    All three channels are set to the same luminance, so the result keeps the
    shape every other augmentation expects and can be chained after this one.
    ```python
    from cvaugmentor import augmentations as aug

    grayscaled = aug.Grayscale().apply(frame)
    ```

    """

    name: str = "grayscale"


    def apply(self, frame: Frame) -> Frame:

        """

        Converts the frame to grayscale.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The grayscaled frame, in RGB.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        return Image.merge("RGB", (frame.convert("L"),) * 3)


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
