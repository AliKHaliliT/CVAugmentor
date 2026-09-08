from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PipelineConfig:

    """

    Immutable configuration for one pipeline.


    Usage
    -----
    This is a plain, frozen value object. As a library, the pipeline never
    reads environment variables or files at import time; the embedding
    application decides where values come from and passes them in explicitly.
    ```python
    from cvaugmentor import PipelineConfig

    config = PipelineConfig(verbose=True, random_state=True)
    ```


    Attributes
    ----------
    verbose : bool
        Whether the walk across a batch reports its progress.

    augmentation_verbose : bool
        Whether the work inside one medium reports its progress.

    warn_verbose : bool
        Whether skipped inputs are reported on the package logger.

    random_state : bool
        Whether every augmentation redraws its unspecified parameters between
        batch items.

    halt_on_error : bool
        Whether one unreadable medium aborts a batch instead of being recorded
        as skipped.

    workers : int | None
        How many threads encode outputs at once. None lets the runner size the
        pool from the machine, and 1 keeps every write on the calling thread.

    """

    verbose: bool = False
    augmentation_verbose: bool = False
    warn_verbose: bool = True
    random_state: bool = False
    halt_on_error: bool = False
    workers: int | None = None

    def __post_init__(self) -> None:

        """

        Rejects a worker count no pool could be built from.

        """

        if self.workers is not None and self.workers < 1:
            raise ValueError(f"workers must be at least 1, or None to size the pool automatically. Received: {self.workers} with type {type(self.workers)}")
