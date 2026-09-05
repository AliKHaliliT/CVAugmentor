from collections.abc import Iterable, Iterator
from pathlib import Path

import pytest
from PIL import Image

from cvaugmentor.core.config import PipelineConfig
from cvaugmentor.domain.schemas.media import Frame, MediaKind, MediaProperties, MediaStream
from cvaugmentor.facade.pipeline import Pipeline, PipelineBuilder

# The facade's own job is the door check, so these cases drive a real pipeline over real
# paths and assert on what it refuses before any codec is asked to read.


class PassThrough:

    name: str = "passthrough"

    def apply(self, frame: Frame) -> Frame:
        return frame

    def reseed(self) -> None:
        return None


class RecordingCodec:

    def __init__(self, kind: MediaKind = "image") -> None:
        self.kind = kind
        self.reads: list[Path] = []

    def read(self, source: Path) -> MediaStream:
        self.reads.append(source)
        return MediaStream(properties=MediaProperties(frame_count=1, width=4, height=4),
                           frames=iter(["frame"]))

    def write(self, destination: Path, stream: MediaStream) -> None:
        list(stream.frames)
        destination.write_bytes(b"written")


class SilentSink:

    def track[T](self, items: Iterable[T], description: str, unit: str, total: int | None = None) -> Iterator[T]:
        return iter(items)


def build(codec: RecordingCodec) -> tuple[Pipeline, RecordingCodec]:
    pipeline = (PipelineBuilder()
                .with_augmentations(PassThrough())
                .with_codec(codec)
                .with_progress_sink(SilentSink())
                .with_config(PipelineConfig(warn_verbose=False))
                .build())
    return pipeline, codec


def test_an_input_path_that_does_not_exist_is_refused_before_anything_is_read(tmp_path: Path) -> None:
    codec = RecordingCodec()
    pipeline, _ = build(codec)

    with pytest.raises(ValueError, match="must exist"):
        pipeline.augment(tmp_path / "missing.png", tmp_path / "out.png", "image", "single", "singular")

    assert codec.reads == []


def test_a_single_run_pointed_at_a_directory_is_refused(tmp_path: Path) -> None:
    pipeline, _ = build(RecordingCodec())

    with pytest.raises(ValueError, match="must name a file"):
        pipeline.augment(tmp_path, tmp_path / "out.png", "image", "single", "singular")


def test_a_batch_run_pointed_at_a_file_is_refused(tmp_path: Path) -> None:
    source = tmp_path / "in.png"
    source.write_bytes(b"")
    pipeline, _ = build(RecordingCodec())

    with pytest.raises(ValueError, match="must name a directory"):
        pipeline.augment(source, tmp_path, "image", "batch", "singular")


def test_an_output_format_that_differs_from_the_input_is_refused(tmp_path: Path) -> None:
    source = tmp_path / "in.png"
    source.write_bytes(b"")
    pipeline, _ = build(RecordingCodec())

    with pytest.raises(ValueError, match="share a format"):
        pipeline.augment(source, tmp_path / "out.jpg", "image", "single", "singular")


def test_an_output_directory_that_does_not_exist_is_refused(tmp_path: Path) -> None:
    source = tmp_path / "in.png"
    source.write_bytes(b"")
    pipeline, _ = build(RecordingCodec())

    with pytest.raises(ValueError, match="existing directory"):
        pipeline.augment(source, tmp_path / "nowhere" / "out.png", "image", "single", "singular")


def test_a_clean_run_reports_what_it_wrote_without_leaking_a_domain_object(tmp_path: Path) -> None:
    source = tmp_path / "in.png"
    source.write_bytes(b"")
    pipeline, _ = build(RecordingCodec())

    report = pipeline.augment(source, tmp_path / "out.png", "image", "single", "sequential")

    assert report.total_inputs == 1
    assert report.total_written == 1
    assert report.total_skipped == 0
    assert report.items[0].written == [tmp_path / "out_passthrough.png"]
    assert type(report).__module__.startswith("cvaugmentor.facade")


def test_the_report_names_the_kind_and_mode_the_caller_asked_for(tmp_path: Path) -> None:
    source = tmp_path / "in.png"
    source.write_bytes(b"")
    pipeline, _ = build(RecordingCodec())

    report = pipeline.augment(source, tmp_path / "out.png", "image", "single", "singular")

    assert (report.kind, report.mode) == ("image", "singular")


def test_a_pipeline_wrapping_something_other_than_a_runner_is_refused() -> None:

    with pytest.raises(TypeError, match="AugmentationRunner"):
        Pipeline("not a runner")  # type: ignore[arg-type]


def test_a_real_image_survives_the_default_codecs_end_to_end(tmp_path: Path) -> None:
    source, destination = tmp_path / "in.png", tmp_path / "out.png"
    Image.new("RGB", (16, 12), (10, 20, 30)).save(source)

    pipeline = (PipelineBuilder()
                .with_augmentations(PassThrough())
                .with_progress_sink(SilentSink())
                .with_config(PipelineConfig(warn_verbose=False))
                .build())
    report = pipeline.augment(source, destination, "image", "single", "singular")

    assert report.total_written == 1
    with Image.open(destination) as written:
        assert written.size == (16, 12)
        assert written.convert("RGB").getpixel((0, 0)) == (10, 20, 30)
