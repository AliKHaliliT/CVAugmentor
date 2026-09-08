from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np

from cvaugmentor.core.acceleration import VIDEO_HINT, opencv
from cvaugmentor.domain.exceptions import MediaReadError, MediaWriteError, UnsupportedMediaError
from cvaugmentor.domain.schemas.media import Frame, MediaKind, MediaProperties, MediaStream

FOURCC = "mp4v"


class OpenCvVideoCodec:

    """

    Decodes and encodes moving pictures through OpenCV.


    Usage
    -----
    OpenCV is this package's only video codec, and it publishes no wheel for
    Windows on ARM or for musl distributions. Constructing this codec is
    therefore always safe and the demand for OpenCV is made when video work
    arrives, so an image-only pipeline still builds where OpenCV is absent.
    Frames cross the port as RGB arrays while OpenCV works in BGR, so the codec
    converts in both directions rather than letting an augmentation operate on
    channels it has misread. Decoding is lazy, so a long video never lands in
    memory whole.
    ```python
    from cvaugmentor.adapters.media import OpenCvVideoCodec

    codec = OpenCvVideoCodec()
    stream = codec.read(Path("input.mp4"))
    ```

    """

    kind: MediaKind = "video"


    def __init__(self) -> None:

        """

        Constructor for the OpenCvVideoCodec class.


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

        # Constructing this codec must not require OpenCV, because the builder registers a
        # default codec for every kind and an image-only pipeline would otherwise be
        # unbuildable wherever OpenCV has no wheel. The demand is made when video work
        # actually arrives, which is the first moment the absence matters.
        self._opencv: ModuleType | None = opencv()


    @property
    def _cv(self) -> ModuleType:

        """

        OpenCV, or the error naming what to install to get it.

        """

        if self._opencv is None:
            raise UnsupportedMediaError(VIDEO_HINT)

        return self._opencv


    def read(self, source: Path) -> MediaStream:

        """

        Opens a video and yields its frames as RGB arrays.


        Parameters
        ----------
        source : Path
            The video file to decode.


        Returns
        -------
        MediaStream
            The video's measurements and its lazily decoded frames.


        Raises
        ------
        MediaReadError
            If the video cannot be opened, or reports no usable geometry or rate.

        """

        capture = self._cv.VideoCapture(str(source))
        if not capture.isOpened():
            capture.release()
            raise MediaReadError(f"Could not read the video at {source}. OpenCV could not open it")

        width = int(capture.get(self._cv.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(self._cv.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = float(capture.get(self._cv.CAP_PROP_FPS))
        frame_count = int(capture.get(self._cv.CAP_PROP_FRAME_COUNT))

        if width <= 0 or height <= 0 or frames_per_second <= 0:
            capture.release()
            raise MediaReadError(
                f"Could not read the video at {source}. It reports {width}x{height} at {frames_per_second} fps"
            )


        properties = MediaProperties(frame_count=max(frame_count, 0),
                                     width=width,
                                     height=height,
                                     frames_per_second=frames_per_second)

        return MediaStream(properties=properties, frames=self._decode(capture))


    def write(self, destination: Path, stream: MediaStream) -> None:

        """

        Encodes every frame of the stream into a video file.


        Parameters
        ----------
        destination : Path
            The video file to write.

        stream : MediaStream
            The stream to encode, whose frames must all match its geometry.


        Returns
        -------
        None.


        Raises
        ------
        MediaWriteError
            If the stream carries no rate, the file cannot be opened for
            writing, or a frame does not match the stream's geometry.

        """

        properties = stream.properties
        if properties.frames_per_second is None:
            raise MediaWriteError(f"Could not write the video at {destination}. The stream carries no frame rate")

        expected = (properties.height, properties.width)
        writer = self._cv.VideoWriter(str(destination),
                                      self._cv.VideoWriter.fourcc(*FOURCC),
                                      properties.frames_per_second,
                                      (properties.width, properties.height))
        if not writer.isOpened():
            writer.release()
            raise MediaWriteError(f"Could not write the video at {destination}. OpenCV could not open it for writing")


        try:
            for frame in stream.frames:
                pixels = np.asarray(frame)
                if pixels.ndim != 3 or pixels.shape[2] != 3 or pixels.dtype != np.uint8:
                    raise MediaWriteError(
                        f"Could not write the video at {destination}. A frame must be an HxWx3 uint8 array, received shape {pixels.shape} with dtype {pixels.dtype}"
                    )
                if pixels.shape[:2] != expected:
                    raise MediaWriteError(
                        f"Could not write the video at {destination}. A frame measures {pixels.shape[1]}x{pixels.shape[0]} against the stream's {properties.width}x{properties.height}"
                    )
                writer.write(self._cv.cvtColor(pixels, self._cv.COLOR_RGB2BGR))
        finally:
            writer.release()


    def _decode(self, capture: Any) -> Iterator[Frame]:

        """

        Yields every frame the capture holds, releasing it when the walk ends.

        """

        try:
            while True:
                read, frame = capture.read()
                if not read:
                    break
                yield self._cv.cvtColor(frame, self._cv.COLOR_BGR2RGB)
        finally:
            capture.release()
