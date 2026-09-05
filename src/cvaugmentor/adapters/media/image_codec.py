from pathlib import Path

from PIL import Image, UnidentifiedImageError

from cvaugmentor.domain.exceptions import MediaReadError, MediaWriteError
from cvaugmentor.domain.schemas.media import MediaKind, MediaProperties, MediaStream


class PillowImageCodec:

    """

    Decodes and encodes still images through Pillow.


    Usage
    -----
    Every image is converted to RGB as it is read, so an augmentation never has
    to ask what mode it was handed and a palette or alpha channel never reaches
    one that cannot read it. The conversion drops transparency, which is the
    price of that uniform contract.
    ```python
    from cvaugmentor.adapters.media import PillowImageCodec

    codec = PillowImageCodec()
    stream = codec.read(Path("input.png"))
    ```

    """

    kind: MediaKind = "image"


    def read(self, source: Path) -> MediaStream:

        """

        Decodes one image into a single-frame stream.


        Parameters
        ----------
        source : Path
            The image file to decode.


        Returns
        -------
        MediaStream
            The image as one RGB frame, with its measurements.


        Raises
        ------
        MediaReadError
            If the file cannot be opened or is not a readable image.

        """

        try:
            with Image.open(source) as opened:
                frame = opened.convert("RGB")
        except (OSError, UnidentifiedImageError) as error:
            raise MediaReadError(f"Could not read the image at {source}. {error}") from error


        properties = MediaProperties(frame_count=1, width=frame.width, height=frame.height)

        return MediaStream(properties=properties, frames=iter([frame]))


    def write(self, destination: Path, stream: MediaStream) -> None:

        """

        Encodes the stream's single frame to an image file.


        Parameters
        ----------
        destination : Path
            The image file to write.

        stream : MediaStream
            The stream whose first frame is written.


        Returns
        -------
        None.


        Raises
        ------
        MediaWriteError
            If the stream carries no frame, or the file cannot be written.

        """

        frame = next(stream.frames, None)
        if frame is None:
            raise MediaWriteError(f"Could not write the image at {destination}. The stream carried no frame")

        try:
            frame.save(destination)
        except (OSError, ValueError) as error:
            raise MediaWriteError(f"Could not write the image at {destination}. {error}") from error
