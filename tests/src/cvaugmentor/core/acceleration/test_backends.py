import zlib
from types import ModuleType

import pytest

from cvaugmentor.core.acceleration import DEFLATE_LEVEL, deflate, inflate, opencv, report

BACKEND_NAMES = {"zlib", "isal"}

# Every attribute the adapters reach for on the resolved module. One that answered present
# and was missing any of these would fail partway through a directory rather than at the
# resolver, which is the whole reason the resolver is asked once and its answer trusted.
CALLED_NAMES = (
    "BORDER_CONSTANT",
    "CAP_PROP_FPS",
    "CAP_PROP_FRAME_COUNT",
    "CAP_PROP_FRAME_HEIGHT",
    "CAP_PROP_FRAME_WIDTH",
    "COLOR_BGR2RGB",
    "COLOR_GRAY2RGB",
    "COLOR_HSV2RGB",
    "COLOR_RGB2BGR",
    "COLOR_RGB2GRAY",
    "COLOR_RGB2HSV",
    "IMREAD_COLOR",
    "INTER_CUBIC",
    "INTER_NEAREST",
    "LUT",
    "VideoCapture",
    "VideoWriter",
    "WARP_INVERSE_MAP",
    "addWeighted",
    "bitwise_not",
    "blur",
    "convertScaleAbs",
    "cvtColor",
    "flip",
    "getRotationMatrix2D",
    "imdecode",
    "imencode",
    "resize",
    "warpAffine",
)

PAYLOADS = [
    b"",
    b"\x00",
    b"one scanline of nothing much",
    b"\x00" * 4096,
    bytes(range(256)) * 40,
    bytes((index * 37 + index // 7) % 256 for index in range(10007)),
]
PAYLOAD_IDS = ["empty", "one byte", "short text", "run of zeroes", "cycling bytes", "long stir"]


@pytest.mark.parametrize("payload", PAYLOADS, ids=PAYLOAD_IDS)
def test_whatever_backend_answered_writes_a_stream_the_stdlib_reads(payload: bytes) -> None:
    # This is the property that makes the two install shapes interchangeable: a file written
    # on a machine carrying the fast extra is read on one without it, and the other way
    # round, so the level each backend is asked for never reaches a reader.
    assert zlib.decompress(deflate(payload)) == payload


@pytest.mark.parametrize("payload", PAYLOADS, ids=PAYLOAD_IDS)
def test_a_deflate_and_an_inflate_return_the_payload_they_started_from(payload: bytes) -> None:
    assert inflate(deflate(payload)) == payload


@pytest.mark.parametrize("payload", PAYLOADS, ids=PAYLOAD_IDS)
def test_a_stream_the_stdlib_wrote_is_read_by_whatever_backend_answered(payload: bytes) -> None:
    assert inflate(zlib.compress(payload)) == payload


def test_the_report_names_the_resolved_deflate_backend_and_the_level_it_is_asked_for() -> None:
    named = report()

    assert named["deflate"] in BACKEND_NAMES
    assert named["deflate_level"] == DEFLATE_LEVEL


def test_the_report_names_the_resolved_accelerator_or_states_that_none_resolved() -> None:
    named = report()

    assert (named["opencv"] is None) is (opencv() is None)
    assert named["opencv"] is None or isinstance(named["opencv"], str)


def test_the_accelerator_is_either_absent_or_a_module_carrying_every_name_the_adapters_call() -> None:
    accelerated = opencv()

    if accelerated is None:
        pytest.skip("OpenCV is an optional backend and did not resolve here")

    assert isinstance(accelerated, ModuleType)
    assert [name for name in CALLED_NAMES if not hasattr(accelerated, name)] == []


def test_the_resolver_answers_the_same_way_every_time_it_is_asked() -> None:
    # Every accelerated operation asks per call, so an answer that moved would put one frame
    # of a video down the fast path and the next one down the fallback.
    assert opencv() is opencv()
