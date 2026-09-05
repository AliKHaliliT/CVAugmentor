from collections.abc import Iterable, Iterator

from tqdm import tqdm


class TqdmProgressSink:

    """

    Renders the runner's walks as terminal progress bars.


    Usage
    -----
    The unit names one item, never a plural, because tqdm appends its own rate
    suffix and renders "3.00image/s" from the singular. The runner decides
    which walks are reported; a sink only draws what it is handed.
    ```python
    from cvaugmentor.adapters.progress import TqdmProgressSink

    sink = TqdmProgressSink()
    for item in sink.track([1, 2, 3], "Working", "item", 3):
        pass
    ```

    """

    def track[T](self, items: Iterable[T], description: str, unit: str, total: int | None = None) -> Iterator[T]:

        """

        Wraps an iteration in a progress bar.


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
            The same items, yielded as the bar advances.


        Raises
        ------
        None.

        """

        return iter(tqdm(iterable=items,
                         desc=description,
                         unit=unit,
                         total=total,
                         dynamic_ncols=True))
