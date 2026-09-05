from PIL import Image

from cvaugmentor.domain.schemas.media import Frame


class Rotate:

    """

    Turns a frame about its centre.


    Usage
    -----
    The frame keeps its original size, so a rotation that is not a multiple of
    a quarter turn leaves black corners where the frame no longer covers the
    canvas.
    ```python
    from cvaugmentor import augmentations as aug

    turned = aug.Rotate(90).apply(frame)
    ```

    """

    name: str = "rotate"

    angle: float


    def __init__(self, angle: int | float = 90) -> None:

        """

        Constructor for the Rotate class.


        Parameters
        ----------
        angle : int | float, optional
            The counter-clockwise angle in degrees.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `angle` is not a number.

        """

        if not isinstance(angle, (int, float)):
            raise ValueError(f"angle must be a number. Received: {angle} with type {type(angle)}")


        self.angle = float(angle)


    def apply(self, frame: Frame) -> Frame:

        """

        Turns the frame.


        Parameters
        ----------
        frame : Frame
            The frame to augment.


        Returns
        -------
        Frame
            The turned frame, at its original size.


        Raises
        ------
        TypeError
            If `frame` is not a PIL image.

        """

        if not isinstance(frame, Image.Image):
            raise TypeError(f"frame must be an instance of the PIL Image. Received: {frame} with type {type(frame)}")


        return frame.rotate(self.angle)


    def reseed(self) -> None:

        """

        Draws nothing, because the angle is chosen rather than drawn.


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
