import sys
import time
from collections.abc import Iterable, Iterator
from typing import TextIO

BAR_WIDTH = 24
MIN_REDRAW_SECONDS = 0.1


class TerminalProgressSink:

    """

    Renders the runner's walks as a single rewritten terminal line.


    Usage
    -----
    Progress is decoration, so this writes to standard error and only when
    that stream is a terminal, which keeps a redirected log free of carriage
    returns and spinner frames. The unit names one item, never a plural,
    because the rate suffix is appended to it. The runner decides which walks
    are reported; a sink only draws what it is handed.
    ```python
    from cvaugmentor.adapters.progress import TerminalProgressSink

    sink = TerminalProgressSink()
    for item in sink.track([1, 2, 3], "Working", "item", 3):
        pass
    ```

    """

    def __init__(self, stream: TextIO | None = None) -> None:

        """

        Constructor for the TerminalProgressSink class.


        Parameters
        ----------
        stream : TextIO | None, optional
            Where the line is drawn. Defaults to standard error.


        Returns
        -------
        None.


        Raises
        ------
        None.

        """

        self._stream = stream


    def track[T](self, items: Iterable[T], description: str, unit: str, total: int | None = None) -> Iterator[T]:

        """

        Wraps an iteration in a progress line.


        Parameters
        ----------
        items : Iterable[T]
            The iteration to report on.

        description : str
            The label shown to the left of the bar.

        unit : str
            The singular name of one item.

        total : int | None, optional
            How many items are expected, where the iteration cannot say.


        Returns
        -------
        Iterator[T]
            The same items, yielded as the line advances.


        Raises
        ------
        None.

        """

        stream = self._stream if self._stream is not None else sys.stderr
        if not (hasattr(stream, "isatty") and stream.isatty()):
            return iter(items)

        return self._draw(items, description, unit, total, stream)


    def _draw[T](self, items: Iterable[T], description: str, unit: str, total: int | None, stream: TextIO) -> Iterator[T]:

        """

        Yields every item, rewriting one line no more often than the redraw floor.

        """

        started = time.monotonic()
        last = 0.0
        done = 0

        try:
            for item in items:
                yield item
                done += 1
                now = time.monotonic()
                if now - last >= MIN_REDRAW_SECONDS:
                    last = now
                    self._render(stream, description, unit, done, total, now - started)
        finally:
            self._render(stream, description, unit, done, total, time.monotonic() - started)
            stream.write("\n")
            stream.flush()


    def _render(self, stream: TextIO, description: str, unit: str, done: int, total: int | None, elapsed: float) -> None:

        """

        Writes one carriage-returned line describing where the walk has reached.

        """

        rate = f"{done / elapsed:.2f}{unit}/s" if elapsed > 0 else f"0.00{unit}/s"

        if total:
            share = min(done / total, 1.0)
            filled = int(share * BAR_WIDTH)
            bar = "#" * filled + "-" * (BAR_WIDTH - filled)
            body = f"{description}: {share * 100:5.1f}% |{bar}| {done}/{total} [{rate}]"
        else:
            body = f"{description}: {done}{unit} [{rate}]"

        stream.write(f"\r{body}")
        stream.flush()

        return None
