import io
import struct
import zlib

import numpy as np
import numpy.typing as npt
import pytest
from PIL import Image

from cvaugmentor.adapters.media.png import decode, encode
from cvaugmentor.core.acceleration import opencv

Pixels = npt.NDArray[np.uint8]

SIGNATURE = b"\x89PNG\r\n\x1a\n"
NONE, SUB, UP, AVERAGE, PAETH = 0, 1, 2, 3, 4
GRAYSCALE, TRUECOLOUR, PALETTE = 0, 2, 3
INTERLACED, NOT_INTERLACED = 1, 0

# The shapes are the ones a stride or a filter is most likely to be wrong on: square, wider
# than tall, taller than wide, odd on one axis, odd on both, and a single row or column.
SHAPES = [(8, 8), (6, 10), (10, 6), (7, 5), (3, 3), (1, 1), (1, 9), (9, 1)]
SHAPE_IDS = [f"{height}x{width}" for height, width in SHAPES]

ACCELERATED = opencv()


def pixels(height: int, width: int, seed: int = 0) -> Pixels:

    """Noise, because a gradient would survive a filter applied on the wrong axis."""

    drawn = np.random.default_rng(seed).integers(0, 256, (height, width, 3), dtype=np.uint8)

    return np.ascontiguousarray(drawn)


def chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))


def png(width: int, height: int, depth: int, colour: int, interlace: int, scanlines: bytes) -> bytes:

    """A PNG assembled here, for the headers and filters no writer in this tree emits."""

    header = struct.pack(">IIBBBBB", width, height, depth, colour, 0, 0, interlace)

    return (SIGNATURE
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(scanlines))
            + chunk(b"IEND", b""))


def scanlines_under(source: Pixels, applied: int) -> bytes:

    """The pixels filtered under one of the covered filters, the same one on every row."""

    height, width = source.shape[0], source.shape[1]
    flat = source.reshape(height, width * 3)
    rows = np.empty((height, width * 3 + 1), np.uint8)
    rows[:, 0] = applied

    if applied == NONE:
        rows[:, 1:] = flat
    elif applied == UP:
        rows[0, 1:] = flat[0]
        np.subtract(flat[1:], flat[:-1], out=rows[1:, 1:], dtype=np.uint8, casting="unsafe")
    else:
        rows[:, 1:4] = flat[:, :3]
        np.subtract(flat[:, 3:], flat[:, :-3], out=rows[:, 4:], dtype=np.uint8, casting="unsafe")

    return rows.tobytes()


def predicted(left: int, above: int, corner: int) -> int:
    estimate = left + above - corner
    from_left, from_above, from_corner = (abs(estimate - left), abs(estimate - above),
                                          abs(estimate - corner))

    if from_left <= from_above and from_left <= from_corner:
        return left
    if from_above <= from_corner:
        return above

    return corner


def scanlines_under_paeth(source: Pixels) -> bytes:

    """The pixels filtered under Paeth, whose per-pixel recurrence the fast path declines."""

    height, width = source.shape[0], source.shape[1]
    flat = source.reshape(height, width * 3)
    stride = width * 3
    rows = bytearray()
    above = bytearray(stride)

    for row in range(height):
        current = bytearray(int(value) for value in flat[row])
        rows.append(PAETH)
        rows.extend((current[index] - predicted(current[index - 3] if index >= 3 else 0,
                                                above[index],
                                                above[index - 3] if index >= 3 else 0)) % 256
                    for index in range(stride))
        above = current

    return bytes(rows)


def written_by_pillow(source: Pixels, mode: str = "RGB") -> bytes:
    buffer = io.BytesIO()
    Image.fromarray(source, "RGB").convert(mode).save(buffer, "PNG")

    return buffer.getvalue()


def read_by_pillow(data: bytes) -> Pixels:
    with Image.open(io.BytesIO(data)) as opened:
        return np.asarray(opened.convert("RGB"), dtype=np.uint8)


@pytest.mark.parametrize(("height", "width"), SHAPES, ids=SHAPE_IDS)
def test_a_round_trip_through_this_codec_returns_the_pixels_it_was_given(height: int, width: int) -> None:
    source = pixels(height, width, height * 100 + width)

    returned = decode(encode(source))

    assert returned is not None
    assert np.array_equal(returned, source)


@pytest.mark.parametrize(("height", "width"), SHAPES, ids=SHAPE_IDS)
def test_a_round_trip_returns_a_frame_an_augmentation_can_take_straight_in(height: int, width: int) -> None:
    returned = decode(encode(pixels(height, width, height * 100 + width)))

    assert returned is not None
    assert returned.dtype == np.uint8
    assert returned.shape == (height, width, 3)
    assert returned.flags["C_CONTIGUOUS"]


@pytest.mark.parametrize(("height", "width"), SHAPES, ids=SHAPE_IDS)
def test_what_this_codec_writes_is_read_back_by_pillow_as_the_same_pixels(height: int, width: int) -> None:
    source = pixels(height, width, height * 100 + width)

    assert np.array_equal(read_by_pillow(encode(source)), source)


@pytest.mark.skipif(ACCELERATED is None, reason="OpenCV is an optional backend and is not installed here")
@pytest.mark.parametrize(("height", "width"), SHAPES, ids=SHAPE_IDS)
def test_what_this_codec_writes_is_read_back_by_opencv_as_the_same_pixels(height: int, width: int) -> None:
    assert ACCELERATED is not None
    source = pixels(height, width, height * 100 + width)

    decoded = ACCELERATED.imdecode(np.frombuffer(encode(source), np.uint8), ACCELERATED.IMREAD_COLOR)

    assert np.array_equal(ACCELERATED.cvtColor(decoded, ACCELERATED.COLOR_BGR2RGB), source)


@pytest.mark.skipif(ACCELERATED is None, reason="OpenCV is an optional backend and is not installed here")
def test_the_two_general_readers_agree_on_what_this_codec_wrote() -> None:
    assert ACCELERATED is not None
    written = encode(pixels(9, 7, 11))

    decoded = ACCELERATED.imdecode(np.frombuffer(written, np.uint8), ACCELERATED.IMREAD_COLOR)

    assert np.array_equal(ACCELERATED.cvtColor(decoded, ACCELERATED.COLOR_BGR2RGB),
                          read_by_pillow(written))


@pytest.mark.parametrize("applied", [NONE, SUB, UP], ids=["none", "sub", "up"])
def test_a_png_under_any_covered_filter_decodes_to_the_pixels_it_was_built_from(applied: int) -> None:
    # The scanlines are filtered here rather than by Pillow, which chooses a filter per row
    # and exposes no option, public or internal, that pins the choice to one of the three
    # the fast path covers.
    source = pixels(4, 3, 5)

    built = png(3, 4, 8, TRUECOLOUR, NOT_INTERLACED, scanlines_under(source, applied))

    assert np.array_equal(read_by_pillow(built), source)
    returned = decode(built)
    assert returned is not None
    assert np.array_equal(returned, source)


def test_a_pillow_written_png_inside_the_covered_subset_decodes_to_the_same_pixels() -> None:
    # A single row is the one file Pillow writes that lands inside the subset, because it
    # carries one filter byte by construction and so cannot mix filters across rows.
    source = pixels(1, 11, 9)

    returned = decode(written_by_pillow(source))

    assert returned is not None
    assert np.array_equal(returned, source)


def test_bytes_that_are_not_a_png_are_declined_rather_than_guessed_at() -> None:
    assert decode(b"this is not a png, it is a sentence") is None


def test_a_sixteen_bit_png_is_declined_rather_than_narrowed() -> None:
    deep = b"".join(bytes([NONE]) + struct.pack(">6H", *[(row * 1000 + column * 7) % 65536
                                                         for column in range(6)])
                    for row in range(2))
    built = png(2, 2, 16, TRUECOLOUR, NOT_INTERLACED, deep)

    assert read_by_pillow(built).shape == (2, 2, 3)
    assert decode(built) is None


def test_an_interlaced_png_is_declined_rather_than_read_in_order() -> None:
    # Pillow writes the interlace byte as a literal zero, so it cannot produce this file.
    # One pixel is the whole of Adam7 pass one and leaves the other six passes empty, which
    # makes the shortest interlaced file that is still a real one.
    built = png(1, 1, 8, TRUECOLOUR, INTERLACED, bytes([NONE, 10, 20, 30]))

    assert np.array_equal(read_by_pillow(built), np.array([[[10, 20, 30]]], np.uint8))
    assert decode(built) is None


def test_a_grayscale_png_is_declined_rather_than_spread_across_three_channels() -> None:
    assert decode(written_by_pillow(pixels(4, 3, 7), mode="L")) is None


def test_a_palette_png_is_declined_rather_than_read_as_indices() -> None:
    assert decode(written_by_pillow(pixels(4, 3, 7), mode="P")) is None


def test_a_paeth_filtered_png_is_declined_rather_than_unfiltered_wrongly() -> None:
    source = pixels(4, 3, 13)

    built = png(3, 4, 8, TRUECOLOUR, NOT_INTERLACED, scanlines_under_paeth(source))

    assert np.array_equal(read_by_pillow(built), source)
    assert decode(built) is None
