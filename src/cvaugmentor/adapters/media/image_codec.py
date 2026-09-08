import io
from pathlib import Path

import numpy as np
import numpy.typing as npt

from cvaugmentor.adapters.media.png import decode as decode_png
from cvaugmentor.adapters.media.png import encode as encode_png
from cvaugmentor.core.acceleration import opencv
from cvaugmentor.domain.exceptions import MediaReadError, MediaWriteError
from cvaugmentor.domain.schemas.media import MediaKind, MediaProperties, MediaStream

PNG_SUFFIXES = frozenset({".png"})


class ArrayImageCodec:

    """

    Decodes and encodes still images as RGB arrays, fastest backend first.


    Usage
    -----
    Three paths sit behind one port. A PNG goes through this package's own
    vectorised codec, which beats every installed library on the subset it
    covers. Anything else, and any PNG that subset does not cover, goes to
    OpenCV when it is installed and to Pillow otherwise, so a platform with no
    OpenCV wheel loses speed and never loses a format. Every path yields an
    HxWx3 uint8 array in RGB order, which drops transparency, the price of one
    uniform contract (see decisions 0048 and 0049).
    ```python
    from cvaugmentor.adapters.media import ArrayImageCodec

    codec = ArrayImageCodec()
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
            data = source.read_bytes()
        except OSError as error:
            raise MediaReadError(f"Could not read the image at {source}. {error}") from error

        pixels = decode_png(data) if source.suffix.lower() in PNG_SUFFIXES else None
        if pixels is None:
            pixels = self._decode_generally(source, data)


        properties = MediaProperties(frame_count=1, width=int(pixels.shape[1]), height=int(pixels.shape[0]))

        return MediaStream(properties=properties, frames=iter([pixels]))


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
            If the stream carries no frame, the frame is not an RGB array, or
            the file cannot be written.

        """

        frame = next(stream.frames, None)
        if frame is None:
            raise MediaWriteError(f"Could not write the image at {destination}. The stream carried no frame")

        pixels = np.asarray(frame)
        if pixels.ndim != 3 or pixels.shape[2] != 3 or pixels.dtype != np.uint8:
            raise MediaWriteError(
                f"Could not write the image at {destination}. A frame must be an HxWx3 uint8 array, received shape {pixels.shape} with dtype {pixels.dtype}"
            )

        try:
            if destination.suffix.lower() in PNG_SUFFIXES:
                destination.write_bytes(encode_png(pixels))
                return None
            self._encode_generally(destination, pixels)
        except (OSError, ValueError) as error:
            raise MediaWriteError(f"Could not write the image at {destination}. {error}") from error

        return None


    def _decode_generally(self, source: Path, data: bytes) -> npt.NDArray[np.uint8]:

        """

        Decodes any format the fast path declined, through OpenCV or Pillow.

        """

        accelerated = opencv()
        if accelerated is not None:
            decoded = accelerated.imdecode(np.frombuffer(data, np.uint8), accelerated.IMREAD_COLOR)
            if decoded is None:
                raise MediaReadError(f"Could not read the image at {source}. OpenCV could not decode it")
            converted: npt.NDArray[np.uint8] = accelerated.cvtColor(decoded, accelerated.COLOR_BGR2RGB)
            return converted

        from PIL import Image, UnidentifiedImageError

        try:
            with Image.open(io.BytesIO(data)) as opened:
                return np.asarray(opened.convert("RGB"), dtype=np.uint8)
        except (OSError, UnidentifiedImageError) as error:
            raise MediaReadError(f"Could not read the image at {source}. {error}") from error


    def _encode_generally(self, destination: Path, pixels: npt.NDArray[np.uint8]) -> None:

        """

        Encodes any format the fast path does not own, through OpenCV or Pillow.

        """

        accelerated = opencv()
        if accelerated is not None:
            written, buffer = accelerated.imencode(destination.suffix,
                                                   accelerated.cvtColor(pixels, accelerated.COLOR_RGB2BGR))
            if not written:
                raise ValueError(f"OpenCV could not encode a {destination.suffix} image")
            destination.write_bytes(buffer.tobytes())
            return None

        from PIL import Image

        Image.fromarray(pixels).save(destination)

        return None
