from collections.abc import Iterator
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from cvaugmentor.domain.exceptions import MediaReadError, MediaWriteError
from cvaugmentor.domain.schemas.media import Frame, MediaKind, MediaProperties, MediaStream

FOURCC = "mp4v"


class OpenCvVideoCodec:

    """

    Decodes and encodes moving pictures through OpenCV.


    Usage
    -----
    OpenCV hands out frames in BGR order and Pillow reads them as RGB, so this
    codec converts in both directions rather than letting an augmentation
    operate on channels it has misread. Frames are decoded lazily, so a long
    video never lands in memory whole.
    ```python
    from cvaugmentor.adapters.media import OpenCvVideoCodec

    codec = OpenCvVideoCodec()
    stream = codec.read(Path("input.mp4"))
    ```

    """

    kind: MediaKind = "video"


    def read(self, source: Path) -> MediaStream:

        """

        Opens a video and yields its frames as RGB images.


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

        capture = cv2.VideoCapture(str(source))
        if not capture.isOpened():
            capture.release()
            raise MediaReadError(f"Could not read the video at {source}. OpenCV could not open it")

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = float(capture.get(cv2.CAP_PROP_FPS))
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

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

        size = (properties.width, properties.height)
        writer = cv2.VideoWriter(str(destination),
                                 cv2.VideoWriter.fourcc(*FOURCC),
                                 properties.frames_per_second,
                                 size)
        if not writer.isOpened():
            writer.release()
            raise MediaWriteError(f"Could not write the video at {destination}. OpenCV could not open it for writing")


        try:
            for frame in stream.frames:
                if frame.size != size:
                    raise MediaWriteError(
                        f"Could not write the video at {destination}. A frame measures {frame.size} against the stream's {size}"
                    )
                writer.write(cv2.cvtColor(np.asarray(frame.convert("RGB")), cv2.COLOR_RGB2BGR))
        finally:
            writer.release()


    def _decode(self, capture: cv2.VideoCapture) -> Iterator[Frame]:

        """

        Yields every frame the capture holds, releasing it when the walk ends.

        """

        try:
            while True:
                read, frame = capture.read()
                if not read:
                    break
                yield Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        finally:
            capture.release()
