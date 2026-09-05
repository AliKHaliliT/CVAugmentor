from pathlib import Path

from cvaugmentor.domain.schemas.jobs import ApplyMode, AugmentationJob, ProcessType
from cvaugmentor.domain.schemas.media import MediaKind
from cvaugmentor.facade.schemas import AugmentationReport
from cvaugmentor.facade.translators import domain_to_facade_augmentation_report
from cvaugmentor.services.execution import AugmentationRunner


class Pipeline:

    """

    The public facade wrapping an assembled augmentation runner.


    Usage
    -----
    Consumers obtain a Pipeline from the PipelineBuilder and interact with the
    facade's schemas only. The facade checks the paths at the door, builds the
    domain job from the caller's arguments, and translates the outcome into a
    report on the way out, so no domain object reaches a caller.
    ```python
    from cvaugmentor import PipelineBuilder
    from cvaugmentor import augmentations as aug

    pipeline = PipelineBuilder().with_augmentations(aug.Flip(), aug.Blur(2.5)).build()
    report = pipeline.augment("in.png", "out.png", "image", "single", "sequential")
    ```

    """

    def __init__(self, runner: AugmentationRunner) -> None:

        """

        Constructor for the Pipeline class.


        Parameters
        ----------
        runner : AugmentationRunner
            The assembled orchestration service.


        Returns
        -------
        None.


        Raises
        ------
        TypeError
            If `runner` is not an AugmentationRunner.

        """

        if not isinstance(runner, AugmentationRunner):
            raise TypeError(f"runner must be an AugmentationRunner. Received: {runner} with type {type(runner)}")


        self._runner = runner


    def augment(self,
                input_path: str | Path,
                output_path: str | Path,
                target: MediaKind,
                process_type: ProcessType,
                mode: ApplyMode) -> AugmentationReport:

        """

        Augments the media the paths name.


        Parameters
        ----------
        input_path : str | Path
            The medium to read, or the directory holding the media to read.

        output_path : str | Path
            The medium to write, or the directory to write the media into.

        target : MediaKind
            Whether the paths carry images or moving pictures.

        process_type : ProcessType
            Whether the paths name one medium ("single") or two directories
            ("batch").

        mode : ApplyMode
            Whether each augmentation is written on its own ("sequential") or
            all of them are chained into one output ("singular").


        Returns
        -------
        AugmentationReport
            One entry per input medium, written or skipped.


        Raises
        ------
        ValueError
            If a path does not exist, does not have the shape the process type
            requires, or names a different format in than out.


        Notes
        -----
        A medium that cannot be decoded or encoded raises an
        AugmentationException subclass, unless a batch run is left to record it
        as a skipped item, which is the default.

        """

        source = Path(input_path)
        destination = Path(output_path)

        if not source.exists():
            raise ValueError(f"input_path must exist. Received: {source}")

        if process_type == "single":
            if not source.is_file():
                raise ValueError(f"input_path must name a file when process_type is 'single'. Received: {source}")
            if not destination.parent.is_dir():
                raise ValueError(f"output_path must sit in an existing directory. Received: {destination}")
            if source.suffix.lower() != destination.suffix.lower():
                raise ValueError(f"input_path and output_path must share a format. Received: {source.suffix} in and {destination.suffix} out")
        else:
            if not source.is_dir():
                raise ValueError(f"input_path must name a directory when process_type is 'batch'. Received: {source}")
            if not destination.is_dir():
                raise ValueError(f"output_path must name an existing directory when process_type is 'batch'. Received: {destination}")


        job = AugmentationJob(source=source,
                              destination=destination,
                              kind=target,
                              process_type=process_type,
                              mode=mode)

        return domain_to_facade_augmentation_report(self._runner.run(job))
