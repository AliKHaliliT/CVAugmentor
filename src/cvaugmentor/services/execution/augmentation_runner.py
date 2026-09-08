import os
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from pathlib import Path

from cvaugmentor.core.config import PipelineConfig
from cvaugmentor.core.logging import get_logger
from cvaugmentor.domain.exceptions import AugmentationException, UnsupportedMediaError
from cvaugmentor.domain.interfaces import (IAugmentation, IMediaCodec, IProgressSink,
                                           IWorkspace)
from cvaugmentor.domain.schemas.jobs import AugmentationJob
from cvaugmentor.domain.schemas.media import (Frame, MediaKind, MediaProperties,
                                              MediaStream)
from cvaugmentor.domain.schemas.results import ItemOutcome, JobResult

logger = get_logger("services.augmentation")


class AugmentationRunner:

    """

    Applies an ordered set of augmentations to the media a job names.


    Usage
    -----
    The runner is the orchestration service, and it reads no file and decodes
    no pixel itself. Every medium reaches it through an IMediaCodec, every
    directory listing through an IWorkspace, and every progress bar through an
    IProgressSink, which is what keeps this layer free of an imaging SDK. The
    facade assembles it, so an embedding application builds a Pipeline rather
    than this.
    ```python
    runner = AugmentationRunner(codecs, workspace, progress, augmentations, config)
    result = runner.run(job)
    ```

    """

    def __init__(self,
                 codecs: Sequence[IMediaCodec],
                 workspace: IWorkspace,
                 progress: IProgressSink,
                 augmentations: Mapping[str, IAugmentation],
                 config: PipelineConfig) -> None:

        """

        Constructor for the AugmentationRunner class.


        Parameters
        ----------
        codecs : Sequence[IMediaCodec]
            One codec per medium kind the runner can carry.

        workspace : IWorkspace
            The location reader that lists directories and names media kinds.

        progress : IProgressSink
            Where the runner reports the work it walks through.

        augmentations : Mapping[str, IAugmentation]
            The augmentations to apply, each under the label naming its output,
            in the order they are applied.

        config : PipelineConfig
            The immutable settings governing reporting and reseeding.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `codecs` is empty or holds two codecs for one medium kind.

        """

        if not codecs:
            raise ValueError(f"codecs must hold at least one codec. Received: {codecs} with type {type(codecs)}")

        by_kind: dict[MediaKind, IMediaCodec] = {}
        for codec in codecs:
            if codec.kind in by_kind:
                raise ValueError(f"codecs must hold one codec per kind. Received a second codec for: {codec.kind}")
            by_kind[codec.kind] = codec


        self._codecs = by_kind
        self._workspace = workspace
        self._progress = progress
        self._augmentations = dict(augmentations)
        self._config = config


    def run(self, job: AugmentationJob) -> JobResult:

        """

        Runs the job, augmenting every medium it names.


        Parameters
        ----------
        job : AugmentationJob
            The paths, medium kind, process type, and application mode to run.


        Returns
        -------
        JobResult
            One outcome per input medium, written or skipped.


        Raises
        ------
        UnsupportedMediaError
            If no injected codec carries the job's medium kind.

        """

        codec = self._codecs.get(job.kind)
        if codec is None:
            raise UnsupportedMediaError(f"No codec carries {job.kind} media. Registered kinds: {sorted(self._codecs)}")


        sources = self._sources(job)
        outcomes: list[ItemOutcome] = []

        walked = self._walk(sources,
                            "Overall progress",
                            job.kind,
                            len(sources),
                            self._config.verbose and job.process_type == "batch")

        # Encoding dominates a sequential-mode pass and every codec here releases the GIL
        # while it compresses, so the writes are the one place threads pay (see decision
        # 0052). One pool serves the whole job, and a worker count of one skips it outright.
        with self._pool() as pool:
            for source in walked:
                outcomes.append(self._augment_one(codec, job, source, pool))
                if self._config.random_state:
                    for augmentation in self._augmentations.values():
                        augmentation.reseed()

        return JobResult(kind=job.kind, mode=job.mode, outcomes=outcomes)


    def _pool(self) -> ThreadPoolExecutor | nullcontext[None]:

        """

        The write pool for one job, or a no-op context when threads are not wanted.

        """

        workers = self._config.workers
        if workers is None:
            workers = min(8, max(1, (os.cpu_count() or 1)))
        if workers == 1 or len(self._augmentations) < 2:
            return nullcontext()

        return ThreadPoolExecutor(max_workers=min(workers, len(self._augmentations)))


    def _sources(self, job: AugmentationJob) -> list[Path]:

        """

        The input media a job names, one for a file and many for a directory.

        """

        if job.process_type == "single":
            return [job.source]

        return self._workspace.list_entries(job.source)


    def _augment_one(self, codec: IMediaCodec, job: AugmentationJob, source: Path, pool: ThreadPoolExecutor | None) -> ItemOutcome:

        """

        Augments one input medium, or reports why it was passed over.

        """

        if job.process_type == "batch" and not self._workspace.is_kind(source, job.kind):
            return self._skip(source, f"not a {job.kind} file")

        destination = job.destination if job.process_type == "single" else job.destination / source.name

        try:
            if job.mode == "sequential":
                written = self._apply_separately(codec, source, destination, pool)
            else:
                written = [self._apply_together(codec, job.kind, source, destination)]
        except AugmentationException as error:
            # One unreadable medium in a directory is data about that medium, not a reason to
            # abandon the rest of the batch; a single-file job has no rest to protect.
            if job.process_type == "single" or self._config.halt_on_error:
                raise
            return self._skip(source, str(error))

        return ItemOutcome(source=source, written=written)


    def _skip(self, source: Path, reason: str) -> ItemOutcome:

        """

        Records a medium the runner passed over, reporting it where asked to.

        """

        if self._config.warn_verbose:
            logger.warning(f"Skipping {source}: {reason}")

        return ItemOutcome(source=source, skipped_reason=reason)


    def _apply_together(self, codec: IMediaCodec, kind: MediaKind, source: Path, destination: Path) -> Path:

        """

        Chains every augmentation onto the medium and writes one output.

        """

        stream = codec.read(source)

        frames = self._walk(stream.frames,
                            "Processing video",
                            "frame",
                            stream.properties.frame_count,
                            self._config.augmentation_verbose and kind == "video")
        tracked_steps = self._config.augmentation_verbose and kind == "image"
        augmented = (self._apply_all(frame, tracked_steps) for frame in frames)

        codec.write(destination, MediaStream(properties=stream.properties, frames=augmented))

        return destination


    def _apply_separately(self, codec: IMediaCodec, source: Path, destination: Path, pool: ThreadPoolExecutor | None) -> list[Path]:

        """

        Applies each augmentation to the untouched medium and writes one output apiece.

        Each task owns one augmentation instance and one output path, so no two threads
        reach the same augmentation and none of them shares a decoded frame. The pool
        preserves submission order, which keeps the written list in the order registered.

        """

        # A still is decoded once and the frame is shared, because thirteen of fourteen
        # decodes are otherwise pure waste and the augmentations are all read-only, which
        # the catalog suite asserts. A moving medium hands out a one-shot iterator that no
        # amount of sharing survives, so each of its outputs reads the file again.
        probe = codec.read(source)
        single = probe.properties.frame_count == 1
        shared = next(probe.frames, None) if single else None
        # A moving medium's probe left its iterator untouched, so the first output consumes
        # that stream instead of opening the file a second time.
        spare: MediaStream | None = None if single else probe

        tasks: list[Callable[[], Path]] = []
        for label, augmentation in self._augmentations.items():
            tasks.append(self._one_output(codec, source, destination, label, augmentation,
                                          probe.properties, shared, spare))
            spare = None

        finished = (task() for task in tasks) if pool is None else pool.map(lambda task: task(), tasks)

        return list(self._walk(finished,
                               "Applying augmentations",
                               "augmentation",
                               len(tasks),
                               self._config.augmentation_verbose))


    def _one_output(self,
                    codec: IMediaCodec,
                    source: Path,
                    destination: Path,
                    label: str,
                    augmentation: IAugmentation,
                    properties: MediaProperties,
                    shared: Frame | None,
                    spare: MediaStream | None) -> Callable[[], Path]:

        """

        A thunk applying one augmentation to the medium and writing its output.

        """

        target = destination.with_name(f"{destination.stem}_{label}{destination.suffix}")

        def write_one() -> Path:
            if shared is not None:
                frames: Iterator[Frame] = iter([shared])
                measurements = properties
            elif spare is not None:
                frames = spare.frames
                measurements = spare.properties
            else:
                stream = codec.read(source)
                frames = stream.frames
                measurements = stream.properties
            augmented = (augmentation.apply(frame) for frame in frames)
            codec.write(target, MediaStream(properties=measurements, frames=augmented))
            return target

        return write_one


    def _apply_all(self, frame: Frame, tracked: bool) -> Frame:

        """

        Passes one frame through every augmentation in order.

        """

        steps = self._walk(list(self._augmentations.values()),
                           "Applying augmentations",
                           "augmentation",
                           len(self._augmentations),
                           tracked)

        for augmentation in steps:
            frame = augmentation.apply(frame)

        return frame


    def _walk[T](self, items: Iterable[T], description: str, unit: str, total: int | None, enabled: bool) -> Iterator[T]:

        """

        Routes an iteration through the progress port, or plainly past it.

        """

        if not enabled:
            return iter(items)

        return self._progress.track(items, description, unit, total)
