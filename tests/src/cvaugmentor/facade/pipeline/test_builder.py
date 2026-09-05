from collections.abc import Iterable, Iterator
from pathlib import Path

import pytest

from cvaugmentor.core.config import PipelineConfig
from cvaugmentor.domain.exceptions import DuplicateAugmentationError, PipelineConfigurationError
from cvaugmentor.domain.schemas.media import Frame, MediaKind, MediaProperties, MediaStream
from cvaugmentor.facade.pipeline import Pipeline, PipelineBuilder

# The builder's job is to refuse a bad wiring at build time, so these fakes are the smallest
# things that do and do not satisfy each port.


class ScriptedAugmentation:

    def __init__(self, name: str = "echo") -> None:
        self.name = name

    def apply(self, frame: Frame) -> Frame:
        return frame

    def reseed(self) -> None:
        return None


class FakeCodec:

    def __init__(self, kind: MediaKind = "image") -> None:
        self.kind = kind
        self.reads: list[Path] = []

    def read(self, source: Path) -> MediaStream:
        self.reads.append(source)
        properties = MediaProperties(frame_count=1, width=4, height=4)
        return MediaStream(properties=properties, frames=iter(["frame"]))

    def write(self, destination: Path, stream: MediaStream) -> None:
        list(stream.frames)


class CountingProgressSink:

    def track[T](self, items: Iterable[T], description: str, unit: str, total: int | None = None) -> Iterator[T]:
        return iter(items)


class NotAnAugmentation:

    pass


def test_a_builder_carrying_no_augmentation_refuses_to_build() -> None:
    with pytest.raises(PipelineConfigurationError):
        PipelineBuilder().build()


def test_a_built_pipeline_is_the_facade_and_nothing_deeper() -> None:
    pipeline = PipelineBuilder().with_augmentations(ScriptedAugmentation()).build()

    assert isinstance(pipeline, Pipeline)


def test_an_object_that_does_not_satisfy_the_port_is_refused_at_wiring_time() -> None:
    with pytest.raises(TypeError, match="IAugmentation"):
        PipelineBuilder().with_augmentation(NotAnAugmentation())  # type: ignore[arg-type]


def test_a_label_registered_twice_is_refused_rather_than_silently_overwritten() -> None:
    builder = PipelineBuilder().with_augmentation(ScriptedAugmentation("blur"))

    with pytest.raises(DuplicateAugmentationError, match="blur"):
        builder.with_augmentation(ScriptedAugmentation("blur"))


def test_an_explicit_label_lets_the_same_augmentation_be_registered_twice() -> None:
    pipeline = (PipelineBuilder()
                .with_augmentation(ScriptedAugmentation("blur"), label="blur_soft")
                .with_augmentation(ScriptedAugmentation("blur"), label="blur_hard")
                .build())

    assert isinstance(pipeline, Pipeline)


def test_a_non_string_label_is_refused() -> None:
    with pytest.raises(TypeError, match="label"):
        PipelineBuilder().with_augmentation(ScriptedAugmentation(), label=7)  # type: ignore[arg-type]


def test_a_config_that_is_not_one_is_refused() -> None:
    with pytest.raises(TypeError, match="PipelineConfig"):
        PipelineBuilder().with_config({"verbose": True})  # type: ignore[arg-type]


def test_an_injected_codec_replaces_the_default_for_its_own_kind(tmp_path: Path) -> None:
    codec = FakeCodec("image")
    source, destination = tmp_path / "in.png", tmp_path / "out.png"
    source.write_bytes(b"not really a png")

    pipeline = (PipelineBuilder()
                .with_augmentations(ScriptedAugmentation())
                .with_codec(codec)
                .with_progress_sink(CountingProgressSink())
                .with_config(PipelineConfig())
                .build())
    pipeline.augment(source, destination, "image", "single", "singular")

    assert codec.reads == [source]


def test_every_fluent_method_hands_the_builder_back_for_chaining() -> None:
    builder = PipelineBuilder()

    assert builder.with_augmentation(ScriptedAugmentation()) is builder
    assert builder.with_codec(FakeCodec()) is builder
    assert builder.with_progress_sink(CountingProgressSink()) is builder
    assert builder.with_config(PipelineConfig()) is builder
