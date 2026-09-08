from collections.abc import Iterable, Iterator
from pathlib import Path

import pytest

from cvaugmentor.core.config import PipelineConfig
from cvaugmentor.domain.exceptions import MediaReadError, UnsupportedMediaError
from cvaugmentor.domain.schemas.jobs import ApplyMode, AugmentationJob, ProcessType
from cvaugmentor.domain.schemas.media import Frame, MediaKind, MediaProperties, MediaStream
from cvaugmentor.services.execution import AugmentationRunner

# The runner never inspects a frame, so these fakes carry plain strings where production
# carries pixels. Only the four outward ports are stood in for, each hand-written against
# its interface rather than patched into place.


class FakeCodec:

    def __init__(self, kind: MediaKind = "image", frames: tuple[str, ...] = ("frame",), fails: Exception | None = None) -> None:
        self.kind = kind
        self._frames = frames
        self._fails = fails
        self.reads: list[Path] = []
        self.writes: list[tuple[Path, list[Frame]]] = []

    def read(self, source: Path) -> MediaStream:
        self.reads.append(source)
        if self._fails is not None:
            raise self._fails
        properties = MediaProperties(frame_count=len(self._frames), width=4, height=4, frames_per_second=1.0)
        return MediaStream(properties=properties, frames=iter(self._frames))

    def write(self, destination: Path, stream: MediaStream) -> None:
        self.writes.append((destination, list(stream.frames)))


class FakeWorkspace:

    def __init__(self, entries: list[Path] | None = None, kinds: dict[str, bool] | None = None) -> None:
        self._entries = entries if entries is not None else []
        self._kinds = kinds if kinds is not None else {}

    def list_entries(self, directory: Path) -> list[Path]:
        return list(self._entries)

    def is_kind(self, path: Path, kind: MediaKind) -> bool:
        return self._kinds.get(path.name, True)


class CountingProgressSink:

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, int | None]] = []

    def track[T](self, items: Iterable[T], description: str, unit: str, total: int | None = None) -> Iterator[T]:
        self.calls.append((description, unit, total))
        return iter(items)


class ScriptedAugmentation:

    def __init__(self, name: str = "echo", raises: Exception | None = None) -> None:
        self.name = name
        self.raises = raises
        self.applied: list[Frame] = []
        self.reseeds = 0

    def apply(self, frame: Frame) -> Frame:
        self.applied.append(frame)
        if self.raises is not None:
            raise self.raises
        return f"{frame}+{self.name}"

    def reseed(self) -> None:
        self.reseeds += 1


def build_runner(*augmentations: ScriptedAugmentation,
                 codec: FakeCodec | None = None,
                 workspace: FakeWorkspace | None = None,
                 **config: bool) -> tuple[AugmentationRunner, FakeCodec, CountingProgressSink]:
    resolved_codec = codec if codec is not None else FakeCodec()
    progress = CountingProgressSink()
    runner = AugmentationRunner(codecs=[resolved_codec],
                                workspace=workspace if workspace is not None else FakeWorkspace(),
                                progress=progress,
                                augmentations={a.name: a for a in augmentations},
                                config=PipelineConfig(**config))
    return runner, resolved_codec, progress


def job(source: str = "in.png",
        destination: str = "out.png",
        process_type: ProcessType = "single",
        mode: ApplyMode = "singular",
        kind: MediaKind = "image") -> AugmentationJob:
    return AugmentationJob(source=Path(source),
                           destination=Path(destination),
                           kind=kind,
                           process_type=process_type,
                           mode=mode)


def test_singular_mode_chains_every_augmentation_into_one_output() -> None:
    first, second = ScriptedAugmentation("first"), ScriptedAugmentation("second")
    runner, codec, _ = build_runner(first, second)

    result = runner.run(job())

    assert len(codec.writes) == 1
    destination, frames = codec.writes[0]
    assert destination == Path("out.png")
    assert frames == ["frame+first+second"]
    assert result.written == [Path("out.png")]


def test_sequential_mode_writes_one_output_per_augmentation_named_by_its_label() -> None:
    runner, codec, _ = build_runner(ScriptedAugmentation("flip"), ScriptedAugmentation("blur"))

    result = runner.run(job(mode="sequential"))

    assert [path for path, _ in codec.writes] == [Path("out_flip.png"), Path("out_blur.png")]
    assert [frames for _, frames in codec.writes] == [["frame+flip"], ["frame+blur"]]
    assert result.written == [Path("out_flip.png"), Path("out_blur.png")]


def test_sequential_mode_reads_a_still_once_and_hands_every_augmentation_the_same_frame() -> None:
    # Thirteen of fourteen decodes are waste on a still, and every augmentation is
    # read-only, which the catalog suite asserts separately (see decision 0052).
    first, second = ScriptedAugmentation("one"), ScriptedAugmentation("two")
    runner, codec, _ = build_runner(first, second)

    runner.run(job(mode="sequential"))

    assert codec.reads == [Path("in.png")]
    assert first.applied == ["frame"]
    assert second.applied == ["frame"]


def test_sequential_mode_reads_a_moving_medium_again_for_every_augmentation() -> None:
    # A stream of frames is a one-shot iterator, so sharing it would starve every
    # augmentation after the first.
    codec = FakeCodec(kind="video", frames=("one", "two", "three"))
    runner, _, _ = build_runner(ScriptedAugmentation("a"), ScriptedAugmentation("b"), codec=codec)

    runner.run(job(kind="video", source="in.mp4", destination="out.mp4", mode="sequential"))

    assert codec.reads == [Path("in.mp4"), Path("in.mp4")]
    assert [frames for _, frames in codec.writes] == [
        ["one+a", "two+a", "three+a"],
        ["one+b", "two+b", "three+b"],
    ]


def test_a_batch_walks_every_entry_the_workspace_lists() -> None:
    workspace = FakeWorkspace(entries=[Path("dir/a.png"), Path("dir/b.png")])
    runner, codec, _ = build_runner(ScriptedAugmentation(), workspace=workspace)

    result = runner.run(job(source="dir", destination="out", process_type="batch"))

    assert [path for path, _ in codec.writes] == [Path("out/a.png"), Path("out/b.png")]
    assert result.written == [Path("out/a.png"), Path("out/b.png")]


def test_a_batch_entry_of_the_wrong_kind_is_recorded_as_skipped_rather_than_read() -> None:
    workspace = FakeWorkspace(entries=[Path("dir/a.png"), Path("dir/notes.txt")],
                              kinds={"a.png": True, "notes.txt": False})
    runner, codec, _ = build_runner(ScriptedAugmentation(), workspace=workspace)

    result = runner.run(job(source="dir", destination="out", process_type="batch"))

    assert codec.reads == [Path("dir/a.png")]
    assert [outcome.source for outcome in result.skipped] == [Path("dir/notes.txt")]
    assert result.skipped[0].skipped_reason == "not a image file"


def test_an_unreadable_medium_in_a_batch_becomes_data_the_rest_of_the_run_survives() -> None:
    workspace = FakeWorkspace(entries=[Path("dir/broken.png")])
    codec = FakeCodec(fails=MediaReadError("the file is corrupt"))
    runner, _, _ = build_runner(ScriptedAugmentation(), codec=codec, workspace=workspace)

    result = runner.run(job(source="dir", destination="out", process_type="batch"))

    assert result.written == []
    assert result.skipped[0].skipped_reason == "the file is corrupt"


def test_an_unreadable_medium_in_a_batch_stops_the_run_when_halting_is_enforced() -> None:
    workspace = FakeWorkspace(entries=[Path("dir/broken.png")])
    codec = FakeCodec(fails=MediaReadError("the file is corrupt"))
    runner, _, _ = build_runner(ScriptedAugmentation(), codec=codec, workspace=workspace, halt_on_error=True)

    with pytest.raises(MediaReadError):
        runner.run(job(source="dir", destination="out", process_type="batch"))


def test_an_unreadable_medium_in_a_single_run_always_raises() -> None:
    codec = FakeCodec(fails=MediaReadError("the file is corrupt"))
    runner, _, _ = build_runner(ScriptedAugmentation(), codec=codec)

    with pytest.raises(MediaReadError):
        runner.run(job())


def test_a_kind_no_codec_carries_is_refused_before_anything_is_read() -> None:
    runner, codec, _ = build_runner(ScriptedAugmentation())

    with pytest.raises(UnsupportedMediaError):
        runner.run(job(kind="video"))

    assert codec.reads == []


def test_every_augmentation_redraws_between_batch_items_when_asked_to() -> None:
    augmentation = ScriptedAugmentation()
    workspace = FakeWorkspace(entries=[Path("dir/a.png"), Path("dir/b.png")])
    runner, _, _ = build_runner(augmentation, workspace=workspace, random_state=True)

    runner.run(job(source="dir", destination="out", process_type="batch"))

    assert augmentation.reseeds == 2


def test_no_augmentation_redraws_when_the_random_state_is_left_off() -> None:
    augmentation = ScriptedAugmentation()
    workspace = FakeWorkspace(entries=[Path("dir/a.png"), Path("dir/b.png")])
    runner, _, _ = build_runner(augmentation, workspace=workspace)

    runner.run(job(source="dir", destination="out", process_type="batch"))

    assert augmentation.reseeds == 0


def test_the_progress_unit_names_one_item_so_a_sink_renders_its_rate_correctly() -> None:
    workspace = FakeWorkspace(entries=[Path("dir/a.mp4")])
    codec = FakeCodec(kind="video", frames=("one", "two"))
    runner, _, progress = build_runner(ScriptedAugmentation(),
                                       codec=codec,
                                       workspace=workspace,
                                       verbose=True,
                                       augmentation_verbose=True)

    runner.run(job(source="dir", destination="out", process_type="batch", kind="video"))

    units = [unit for _, unit, _ in progress.calls]
    assert units == ["video", "frame"]
    assert all(not unit.endswith("s") for unit in units)


def test_a_walk_reports_nothing_through_the_port_while_its_verbosity_is_off() -> None:
    workspace = FakeWorkspace(entries=[Path("dir/a.png")])
    runner, _, progress = build_runner(ScriptedAugmentation(), workspace=workspace)

    runner.run(job(source="dir", destination="out", process_type="batch"))

    assert progress.calls == []


def test_the_overall_walk_is_reported_with_the_count_it_is_about_to_cross() -> None:
    workspace = FakeWorkspace(entries=[Path("dir/a.png"), Path("dir/b.png")])
    runner, _, progress = build_runner(ScriptedAugmentation(), workspace=workspace, verbose=True)

    runner.run(job(source="dir", destination="out", process_type="batch"))

    assert progress.calls == [("Overall progress", "image", 2)]


def test_a_single_run_reports_no_overall_walk_because_it_crosses_one_item() -> None:
    runner, _, progress = build_runner(ScriptedAugmentation(), verbose=True)

    runner.run(job())

    assert progress.calls == []


def test_two_codecs_for_one_kind_are_refused_at_construction() -> None:
    with pytest.raises(ValueError, match="one codec per kind"):
        AugmentationRunner(codecs=[FakeCodec(), FakeCodec()],
                           workspace=FakeWorkspace(),
                           progress=CountingProgressSink(),
                           augmentations={},
                           config=PipelineConfig())


def test_a_runner_with_no_codec_is_refused_at_construction() -> None:
    with pytest.raises(ValueError, match="at least one codec"):
        AugmentationRunner(codecs=[],
                           workspace=FakeWorkspace(),
                           progress=CountingProgressSink(),
                           augmentations={},
                           config=PipelineConfig())
