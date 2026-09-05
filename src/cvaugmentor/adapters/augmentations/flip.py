from PIL import Image

from cvaugmentor.domain.schemas.media import Frame

FLIP_TYPES = ("horizontal", "vertical")


class Flip:

    """

    Mirrors a frame across one axis.


    Usage
    -----
    A horizontal flip mirrors left to right, and a vertical flip mirrors top to
    bottom. The axis is a choice rather than a draw, so a flipped video stays
    flipped the same way for its whole length.
    ```python
    from cvaugmentor import augmentations as aug

    flipped = aug.Flip("horizontal").apply(frame)
    ```

    """

    name: str = "flip"

    flip_type: str


    def __init__(self, flip_type: str = "vertical") -> None:

        """

        Constructor for the Flip class.


        Parameters
        ----------
        flip_type : str, optional
            Which axis to mirror across, "horizontal" or "vertical".


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `flip_type` is neither "horizontal" nor "vertical".

        """

        if flip_type not in FLIP_TYPES:
            raise ValueError(f"flip_type must be one of {FLIP_TYPES}. Received: {flip_type} with type {type(flip_type)}")


        self.flip_type = flip_type


    def apply(self, frame: Frame) -> Frame:

        """

        Mirrors the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The mirrored frame.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        if self.flip_type == "horizontal":
            return frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        return frame.transpose(Image.Transpose.FLIP_TOP_BOTTOM)


    def reseed(self) -> None:

        """

        Draws nothing, because the axis is chosen rather than drawn.


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
