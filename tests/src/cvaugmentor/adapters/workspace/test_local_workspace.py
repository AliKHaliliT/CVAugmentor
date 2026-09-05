from pathlib import Path

import pytest

from cvaugmentor.adapters.workspace import LocalWorkspace
from cvaugmentor.domain.interfaces import IWorkspace


def test_the_local_workspace_satisfies_the_port() -> None:
    assert isinstance(LocalWorkspace(), IWorkspace)


def test_entries_come_back_in_the_order_a_person_counting_them_expects(tmp_path: Path) -> None:
    for name in ("10.png", "2.png", "1.png", "20.png"):
        (tmp_path / name).write_bytes(b"")

    entries = LocalWorkspace().list_entries(tmp_path)

    assert [entry.name for entry in entries] == ["1.png", "2.png", "10.png", "20.png"]


def test_a_directory_inside_the_listing_is_not_an_entry(tmp_path: Path) -> None:
    (tmp_path / "frame.png").write_bytes(b"")
    (tmp_path / "nested").mkdir()

    entries = LocalWorkspace().list_entries(tmp_path)

    assert [entry.name for entry in entries] == ["frame.png"]


def test_listing_something_that_is_not_a_directory_is_refused(tmp_path: Path) -> None:
    lone = tmp_path / "frame.png"
    lone.write_bytes(b"")

    with pytest.raises(NotADirectoryError):
        LocalWorkspace().list_entries(lone)


@pytest.mark.parametrize(("name", "kind", "expected"), [
    ("frame.png", "image", True),
    ("frame.jpg", "image", True),
    ("frame.mp4", "image", False),
    ("clip.mp4", "video", True),
    ("clip.png", "video", False),
    ("notes.txt", "image", False),
    ("no_suffix", "image", False),
])
def test_a_name_is_read_for_the_kind_of_medium_it_claims(name: str, kind: str, expected: bool) -> None:
    assert LocalWorkspace().is_kind(Path(name), kind) is expected  # type: ignore[arg-type]
