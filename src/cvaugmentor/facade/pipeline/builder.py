from cvaugmentor.adapters.media import OpenCvVideoCodec, PillowImageCodec
from cvaugmentor.adapters.progress import TqdmProgressSink
from cvaugmentor.adapters.workspace import LocalWorkspace
from cvaugmentor.core.config import PipelineConfig
from cvaugmentor.core.plugins import load_entry_point_augmentations
from cvaugmentor.domain.exceptions import DuplicateAugmentationError, PipelineConfigurationError
from cvaugmentor.domain.interfaces import (IAugmentation, IMediaCodec, IProgressSink,
                                           IWorkspace)
from cvaugmentor.domain.schemas.media import MediaKind
from cvaugmentor.facade.pipeline.pipeline import Pipeline
from cvaugmentor.services.execution import AugmentationRunner


class PipelineBuilder:

    """

    A guarded fluent builder assembling a Pipeline from its ports.


    Usage
    -----
    Every injected implementation is validated against its Protocol at wiring
    time, so a misconfigured pipeline fails at build rather than midway through
    a directory. Each augmentation is registered under a label, which names the
    file it writes in sequential mode; pass one explicitly to run the same
    augmentation twice with different settings. Anything not provided falls
    back to the defaults, which are the Pillow and OpenCV codecs, the local
    filesystem, a tqdm progress sink, and a default PipelineConfig.
    ```python
    from cvaugmentor import PipelineBuilder, PipelineConfig
    from cvaugmentor import augmentations as aug

    pipeline = (
        PipelineBuilder()
        .with_augmentation(aug.Blur(1.0), label="blur_soft")
        .with_augmentation(aug.Blur(5.0), label="blur_hard")
        .with_config(PipelineConfig(verbose=True))
        .build()
    )
    ```

    """

    def __init__(self) -> None:

        """

        Constructor for the PipelineBuilder class.


        Parameters
        ----------
        None.


        Returns
        -------
        None.


        Raises
        ------
        None.

        """

        self._augmentations: dict[str, IAugmentation] = {}
        self._codecs: dict[MediaKind, IMediaCodec] = {}
        self._workspace: IWorkspace | None = None
        self._progress: IProgressSink | None = None
        self._config: PipelineConfig | None = None


    def with_augmentation(self, augmentation: IAugmentation, label: str | None = None) -> PipelineBuilder:

        """

        Registers one augmentation under the label naming its output.


        Parameters
        ----------
        augmentation : IAugmentation
            The augmentation to apply.

        label : str | None, optional
            The name its sequential-mode output carries. Defaults to the
            augmentation's own name.


        Returns
        -------
        PipelineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `augmentation` does not satisfy IAugmentation, or `label` is not
            a string.

        DuplicateAugmentationError
            If the label is already registered.

        """

        if not isinstance(augmentation, IAugmentation):
            raise TypeError(f"augmentation must satisfy IAugmentation. Received: {augmentation} with type {type(augmentation)}")
        if label is not None and not isinstance(label, str):
            raise TypeError(f"label must be a string. Received: {label} with type {type(label)}")

        resolved = label if label is not None else augmentation.name
        if resolved in self._augmentations:
            raise DuplicateAugmentationError(f"The label '{resolved}' is already registered. Pass an explicit label to register it twice")


        self._augmentations[resolved] = augmentation

        return self


    def with_augmentations(self, *augmentations: IAugmentation) -> PipelineBuilder:

        """

        Registers several augmentations, each under its own name.


        Parameters
        ----------
        *augmentations : IAugmentation
            The augmentations to apply, in the order given.


        Returns
        -------
        PipelineBuilder
            The builder, for chaining.


        Raises
        ------
        None.

        """

        for augmentation in augmentations:
            self.with_augmentation(augmentation)

        return self


    def with_discovered_augmentations(self) -> PipelineBuilder:

        """

        Registers every augmentation third parties publish to the entry-point group.


        Parameters
        ----------
        None.


        Returns
        -------
        PipelineBuilder
            The builder, for chaining.


        Raises
        ------
        None.

        """

        for augmentation in load_entry_point_augmentations():
            self.with_augmentation(augmentation)

        return self


    def with_codec(self, codec: IMediaCodec) -> PipelineBuilder:

        """

        Replaces the default codec for the medium kind this one carries.


        Parameters
        ----------
        codec : IMediaCodec
            The codec to use for its own kind.


        Returns
        -------
        PipelineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `codec` does not satisfy IMediaCodec.

        """

        if not isinstance(codec, IMediaCodec):
            raise TypeError(f"codec must satisfy IMediaCodec. Received: {codec} with type {type(codec)}")


        self._codecs[codec.kind] = codec

        return self


    def with_workspace(self, workspace: IWorkspace) -> PipelineBuilder:

        """

        Injects the location reader that lists directories.


        Parameters
        ----------
        workspace : IWorkspace
            The workspace implementation to use.


        Returns
        -------
        PipelineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `workspace` does not satisfy IWorkspace.

        """

        if not isinstance(workspace, IWorkspace):
            raise TypeError(f"workspace must satisfy IWorkspace. Received: {workspace} with type {type(workspace)}")


        self._workspace = workspace

        return self


    def with_progress_sink(self, progress: IProgressSink) -> PipelineBuilder:

        """

        Injects where the runner reports the work it walks through.


        Parameters
        ----------
        progress : IProgressSink
            The progress sink implementation to use.


        Returns
        -------
        PipelineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `progress` does not satisfy IProgressSink.

        """

        if not isinstance(progress, IProgressSink):
            raise TypeError(f"progress must satisfy IProgressSink. Received: {progress} with type {type(progress)}")


        self._progress = progress

        return self


    def with_config(self, config: PipelineConfig) -> PipelineBuilder:

        """

        Injects the immutable settings governing reporting and reseeding.


        Parameters
        ----------
        config : PipelineConfig
            The configuration to run under.


        Returns
        -------
        PipelineBuilder
            The builder, for chaining.


        Raises
        ------
        TypeError
            If `config` is not a PipelineConfig.

        """

        if not isinstance(config, PipelineConfig):
            raise TypeError(f"config must be a PipelineConfig. Received: {config} with type {type(config)}")


        self._config = config

        return self


    def build(self) -> Pipeline:

        """

        Assembles the pipeline from everything registered so far.


        Parameters
        ----------
        None.


        Returns
        -------
        Pipeline
            The assembled public facade.


        Raises
        ------
        PipelineConfigurationError
            If no augmentation was registered.

        """

        if not self._augmentations:
            raise PipelineConfigurationError("A pipeline needs at least one augmentation. Register one before building")


        defaults: dict[MediaKind, IMediaCodec] = {"image": PillowImageCodec(), "video": OpenCvVideoCodec()}
        runner = AugmentationRunner(codecs=list((defaults | self._codecs).values()),
                                    workspace=self._workspace if self._workspace is not None else LocalWorkspace(),
                                    progress=self._progress if self._progress is not None else TqdmProgressSink(),
                                    augmentations=self._augmentations,
                                    config=self._config if self._config is not None else PipelineConfig())

        return Pipeline(runner)
