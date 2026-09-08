from cvaugmentor.adapters.augmentations.frames import as_pixels, grayscale
from cvaugmentor.domain.schemas.media import Frame


class Grayscale:

    """

    Drains the colour from a frame, leaving it in RGB.


    Usage
    -----
    All three channels are set to the same luminance, so the result keeps the
    shape every other augmentation expects and can be chained after this one.
    The luminance is the BT.601 one the codecs already agree on, weighted in
    integers so nothing rounds twice.
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
            If `frame` is not an HxWx3 uint8 array in RGB order.

        """

        return grayscale(as_pixels(frame))


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
