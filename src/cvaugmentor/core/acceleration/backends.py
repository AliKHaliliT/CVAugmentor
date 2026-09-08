import zlib
from types import ModuleType
from typing import Any, cast

_OPENCV: ModuleType | None
try:
    import cv2 as _cv2
except ImportError:
    _OPENCV = None
else:
    _OPENCV = _cv2

_DEFLATE: ModuleType
_DEFLATE_NAME: str
# Each backend raises its own error class and ISA-L's is not a zlib.error subclass, so a
# caller catching the obvious type would let a corrupt stream through on exactly the
# install where the accelerator is present. Both are collected here and inflate translates
# to the standard one, leaving callers a single type to catch.
_DEFLATE_FAILURES: tuple[type[BaseException], ...]
try:
    from isal import isal_zlib as _isal
except ImportError:
    _DEFLATE = zlib
    _DEFLATE_NAME = "zlib"
    _DEFLATE_FAILURES = (zlib.error,)
else:
    _DEFLATE = _isal
    _DEFLATE_NAME = "isal"
    _DEFLATE_FAILURES = (zlib.error, cast(type[BaseException], _isal.error), ValueError)

# ISA-L's own levels top out at 3 and mean different things from zlib's nine. Level 2 of
# ISA-L compresses a filtered scanline block smaller than zlib's level 1 and roughly six
# times faster, so each backend is asked for the setting that matches the other's output
# rather than for the same number (see decision 0050).
DEFLATE_LEVEL: int = 2 if _DEFLATE_NAME == "isal" else 1

INSTALL_HINT = 'Install the accelerators with: pip install "cvaugmentor[fast]"'
VIDEO_HINT = 'Video needs OpenCV: pip install "cvaugmentor[video]"'



def opencv() -> ModuleType | None:

    """

    Returns the OpenCV module when it is installed.


    Usage
    -----
    OpenCV carries this package's fast paths and its only video codec, and it
    publishes no wheel for Windows on ARM or for musl distributions, so every
    caller treats it as absent-until-proven-present. An operation that has a
    NumPy fallback asks here and takes it; one that has none raises with
    `INSTALL_HINT`.
    ```python
    from cvaugmentor.core.acceleration import opencv

    accelerated = opencv()
    if accelerated is not None:
        frame = accelerated.bitwise_not(frame)
    ```


    Parameters
    ----------
    None.


    Returns
    -------
    ModuleType | None
        The `cv2` module, or None where it is not installed.


    Raises
    ------
    None.

    """

    return _OPENCV


def deflate(payload: bytes, level: int | None = None) -> bytes:

    """

    Compresses a payload to a zlib stream through the fastest installed backend.


    Parameters
    ----------
    payload : bytes
        The bytes to compress.

    level : int | None, optional
        The backend's own compression level. Defaults to `DEFLATE_LEVEL`.


    Returns
    -------
    bytes
        The zlib stream, readable by any zlib decompressor either way.


    Raises
    ------
    None.

    """

    return cast(bytes, _DEFLATE.compress(payload, DEFLATE_LEVEL if level is None else level))


def inflate(stream: bytes) -> bytes:

    """

    Decompresses a zlib stream through the fastest installed backend.


    Parameters
    ----------
    stream : bytes
        The zlib stream to decompress.


    Returns
    -------
    bytes
        The original bytes.


    Raises
    ------
    zlib.error
        If the stream is not a readable zlib stream, whichever backend read it.

    """

    try:
        return cast(bytes, _DEFLATE.decompress(stream))
    except zlib.error:
        raise
    except _DEFLATE_FAILURES as failure:
        raise zlib.error(str(failure)) from failure


def report() -> dict[str, Any]:

    """

    Returns which backends resolved, for a caller diagnosing its own speed.


    Parameters
    ----------
    None.


    Returns
    -------
    dict[str, Any]
        The resolved OpenCV version or None, and the deflate backend's name.


    Raises
    ------
    None.

    """

    return {
        "opencv": None if _OPENCV is None else str(_OPENCV.__version__),
        "deflate": _DEFLATE_NAME,
        "deflate_level": DEFLATE_LEVEL,
    }
