import struct
import zlib

import numpy as np
import numpy.typing as npt

from cvaugmentor.core.acceleration import deflate, inflate

SIGNATURE = b"\x89PNG\r\n\x1a\n"

# The filters this module inverts with one vectorised call. None copies, Sub predicts from
# the pixel to the left so its rows are independent of each other, and Up predicts from the
# row above so its columns are. Average and Paeth need a finished neighbour on both axes,
# which is a per-pixel recurrence no array library reaches, so a file using either goes to
# a general decoder instead (see decision 0051).
NONE, SUB, UP = 0, 1, 2
VECTORISABLE = frozenset({NONE, SUB, UP})

TRUECOLOUR = 2
EIGHT_BIT = 8
NOT_INTERLACED = 0


def _chunk(kind: bytes, payload: bytes) -> bytes:

    """

    One length-prefixed, CRC-suffixed PNG chunk.

    """

    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))


def encode(pixels: npt.NDArray[np.uint8], level: int | None = None) -> bytes:

    """

    Encodes RGB pixels to a PNG, losslessly.


    Usage
    -----
    The Up filter is applied with one vectorised subtract, which costs a single
    pass, and the result is deflated by the fastest installed backend. Both
    halves are exactly reversible, so the pixels a reader gets back are the
    pixels handed in.
    ```python
    from cvaugmentor.adapters.media.png import encode

    Path("out.png").write_bytes(encode(pixels))
    ```


    Parameters
    ----------
    pixels : npt.NDArray[np.uint8]
        The HxWx3 uint8 pixels in RGB order.

    level : int | None, optional
        The deflate backend's own level. Defaults to the backend's match for
        speed against size.


    Returns
    -------
    bytes
        The complete PNG file.


    Raises
    ------
    ValueError
        If `pixels` is not an HxWx3 uint8 array.

    """

    if pixels.ndim != 3 or pixels.shape[2] != 3 or pixels.dtype != np.uint8:
        raise ValueError(f"pixels must be an HxWx3 uint8 array. Received: shape {pixels.shape} with dtype {pixels.dtype}")


    height, width = pixels.shape[0], pixels.shape[1]
    flat = np.ascontiguousarray(pixels).reshape(height, width * 3)

    scanlines = np.empty((height, width * 3 + 1), np.uint8)
    scanlines[:, 0] = UP
    scanlines[0, 1:] = flat[0]
    np.subtract(flat[1:], flat[:-1], out=scanlines[1:, 1:], dtype=np.uint8, casting="unsafe")

    header = struct.pack(">IIBBBBB", width, height, EIGHT_BIT, TRUECOLOUR, 0, 0, NOT_INTERLACED)

    return (SIGNATURE
            + _chunk(b"IHDR", header)
            + _chunk(b"IDAT", deflate(scanlines.tobytes(), level))
            + _chunk(b"IEND", b""))


def decode(data: bytes) -> npt.NDArray[np.uint8] | None:

    """

    Decodes a PNG to RGB pixels where the fast path applies.


    Usage
    -----
    This reads the subset a vectorised inverse covers: eight-bit truecolour,
    not interlaced, every scanline carrying the same filter and that filter
    being None, Sub, or Up. Anything else returns None, which tells the calling
    codec to hand the bytes to a general decoder rather than guessing.
    ```python
    from cvaugmentor.adapters.media.png import decode

    pixels = decode(Path("in.png").read_bytes())
    ```


    Parameters
    ----------
    data : bytes
        The PNG file.


    Returns
    -------
    npt.NDArray[np.uint8] | None
        The HxWx3 uint8 RGB pixels, or None where the fast path does not apply.


    Raises
    ------
    None.

    """

    if not data.startswith(SIGNATURE):
        return None

    position = len(SIGNATURE)
    payloads: list[bytes] = []
    header: tuple[int, ...] | None = None

    while position + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[position:position + 8])
        body = data[position + 8:position + 8 + length]
        position += 12 + length
        if kind == b"IHDR" and len(body) >= 13:
            header = struct.unpack(">IIBBBBB", body[:13])
        elif kind == b"IDAT":
            payloads.append(body)
        elif kind == b"IEND":
            break

    if header is None or not payloads:
        return None

    width, height, depth, colour, _, _, interlace = header
    if depth != EIGHT_BIT or colour != TRUECOLOUR or interlace != NOT_INTERLACED:
        return None

    try:
        raw = inflate(b"".join(payloads))
    except zlib.error:
        return None

    stride = width * 3 + 1
    if len(raw) != height * stride:
        return None

    scanlines = np.frombuffer(raw, np.uint8).reshape(height, stride)
    filters = set(scanlines[:, 0].tolist())
    if not filters <= VECTORISABLE or len(filters) != 1:
        return None

    body_bytes = scanlines[:, 1:]
    applied = filters.pop()

    if applied == NONE:
        return np.ascontiguousarray(body_bytes.reshape(height, width, 3))
    if applied == UP:
        return np.cumsum(body_bytes, axis=0, dtype=np.uint8).reshape(height, width, 3)

    return np.cumsum(body_bytes.reshape(height, width, 3), axis=1, dtype=np.uint8)
