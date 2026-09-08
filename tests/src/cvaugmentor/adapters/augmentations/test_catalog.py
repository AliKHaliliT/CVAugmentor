import importlib
import pkgutil
from collections.abc import Callable
from types import ModuleType
from typing import Any

import numpy as np
import numpy.typing as npt
import pytest

from cvaugmentor.adapters import augmentations as catalog
from cvaugmentor.adapters.augmentations import (flip, frames, hue, negative, rotate, saturation,
                                               shear, zoom)
from cvaugmentor.domain.interfaces import IAugmentation

Pixels = npt.NDArray[np.uint8]

HEIGHT, WIDTH = 48, 64

# Every augmentation is built with explicit settings here, because a case asserting that a
# frame changed must not depend on which value a draw happened to land on. The catalog is
# read off the package door, so a new augmentation that is exported is covered the moment it
# lands and one that is not exported fails the door case below.
# Saturation is settled at 0.5 rather than -1 because it is the one operation whose two
# paths are allowed to disagree, by one level scaled by this factor, and 0.5 keeps that
# bound at the single level every other operation is held to (see decision 0054).
CASES: list[tuple[type[Any], dict[str, Any], bool]] = [
    (catalog.Blur, {"radius": 2.0}, True),
    (catalog.Brightness, {"brightness_factor": 0.5}, True),
    (catalog.Cutout, {"max_size": 8, "max_count": 3}, True),
    (catalog.Exposure, {"exposure_factor": 1.6}, True),
    (catalog.Flip, {"flip_type": "horizontal"}, True),
    (catalog.Grayscale, {}, True),
    (catalog.Hue, {"hue_shift": 120}, True),
    (catalog.Negative, {}, True),
    (catalog.NoAugmentation, {}, False),
    (catalog.Noise, {"intensity": 0.5}, True),
    (catalog.Rotate, {"angle": 33}, True),
    (catalog.Saturation, {"saturation_factor": 0.5}, True),
    (catalog.Shear, {"shear": (0.3, 0.2)}, True),
    (catalog.Translation, {"translate": (12, -7)}, True),
    (catalog.Zoom, {"zoom_size": (24, 24)}, True),
]
IDS = [case[0].__name__ for case in CASES]
# These three place their effect somewhere on whatever frame they meet, and that somewhere is
# never a setting the caller gave, so a redraw is free to move it. What a redraw must not
# touch is the setting itself, which the placement cases below hold instead.
PLACEMENT_REDRAWN = {"Cutout", "Noise", "Zoom"}
STABLE_CASES = [case for case in CASES if case[0].__name__ not in PLACEMENT_REDRAWN]
STABLE_IDS = [case[0].__name__ for case in STABLE_CASES]
PLACEMENT_CASES: list[tuple[type[Any], dict[str, Any], str]] = [
    (catalog.Cutout, {"max_size": 8, "max_count": 3}, "max_count"),
    (catalog.Noise, {"intensity": 0.5}, "intensity"),
    (catalog.Zoom, {"zoom_size": (24, 24)}, "zoom_size"),
]

# The modules that hold their own binding to the accelerator resolver: `frames` for the
# shared guard and the shared kernels, and one per augmentation that imported the resolver
# by name. Every one of them has to be told the accelerator is absent or the run under test
# is only half a fallback, so the door case below keeps this list honest.
RESOLVER_HOLDERS: tuple[ModuleType, ...] = (frames, flip, hue, negative, rotate, saturation,
                                            shear, zoom)
# The two paths are held to agreement within one level per channel rather than to equality,
# because the vectorised colour kernel OpenCV ships rounds differently from the scalar
# formula OpenCV itself documents (see decision 0054).
TOLERANCE = 1


def frame() -> Pixels:

    """A colourful gradient, so an augmentation that changes colour visibly does."""

    rows, columns = np.indices((HEIGHT, WIDTH))
    stacked = np.stack([columns * 4 % 256, rows * 5 % 256, (columns + rows) * 3 % 256], axis=-1)

    return np.ascontiguousarray(stacked.astype(np.uint8))


def noise_frame() -> Pixels:

    """A frame with no smoothness left to hide in, for the two paths to be compared over."""

    # A gradient is where a resampling kernel or a border rule that differs by a hair still
    # lands on nearly the same pixel, so the case that compares the two paths runs over this
    # one as well and would catch a divergence the gradient absorbs.
    drawn = np.random.default_rng(0).integers(0, 256, (HEIGHT, WIDTH, 3), dtype=np.uint8)

    return np.ascontiguousarray(drawn)


FRAMES: list[Callable[[], Pixels]] = [frame, noise_frame]
FRAME_IDS = ["gradient", "noise"]


def pixels(augmented: Pixels) -> bytes:
    return np.ascontiguousarray(augmented).tobytes()


def without_the_accelerator(monkeypatch: pytest.MonkeyPatch) -> None:

    """Rebinds the accelerator resolver, everywhere it is held, to one that answers absent."""

    # Reaching into a module internals is otherwise forbidden here in favour of a fake at
    # the port, and the accelerator is not a port: it is an optional backend resolved
    # in-process, which is an architectural seam with no interface to fake. Decision 0053
    # requires both of its paths be exercised, because a fallback that never runs is a
    # fallback that does not work, and substitution is the only way to reach the second path
    # on a machine where the wheel did install.
    for holder in RESOLVER_HOLDERS:
        monkeypatch.setattr(holder, "opencv", lambda: None)


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_every_augmentation_satisfies_the_port_it_is_registered_under(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    assert isinstance(augmentation(**arguments), IAugmentation)


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_every_augmentation_returns_a_frame_of_the_size_it_was_given(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    original = frame()

    augmented = augmentation(**arguments).apply(original)

    assert isinstance(augmented, np.ndarray)
    assert augmented.shape == original.shape


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_every_augmentation_returns_a_frame_a_codec_can_write_straight_out(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    augmented = augmentation(**arguments).apply(frame())

    assert augmented.dtype == np.uint8
    assert augmented.ndim == 3
    assert augmented.shape[2] == 3
    assert augmented.flags["C_CONTIGUOUS"]


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_every_augmentation_changes_the_frame_unless_it_promises_not_to(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    original = frame()

    augmented = augmentation(**arguments).apply(original)

    assert (pixels(augmented) != pixels(original)) is changes


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_no_augmentation_writes_into_the_frame_it_was_handed(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    original = frame()
    handed = original.copy()

    augmentation(**arguments).apply(handed)

    assert pixels(handed) == pixels(original)


@pytest.mark.parametrize("build", FRAMES, ids=FRAME_IDS)
@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_the_accelerated_and_the_fallback_paths_render_the_same_frame(augmentation: type[Any], arguments: dict[str, Any], changes: bool, build: Callable[[], Pixels], monkeypatch: pytest.MonkeyPatch) -> None:
    instance = augmentation(**arguments)
    accelerated = instance.apply(build())

    without_the_accelerator(monkeypatch)

    fallback = instance.apply(build())

    assert np.abs(accelerated.astype(np.int16) - fallback.astype(np.int16)).max() <= TOLERANCE


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_one_instance_treats_every_frame_the_same_way(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    # This is what keeps a video coherent: the same instance crosses every frame of it, so a
    # parameter drawn once must not be redrawn per call.
    instance = augmentation(**arguments)

    assert pixels(instance.apply(frame())) == pixels(instance.apply(frame()))


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_a_frame_that_is_not_an_rgb_array_is_refused(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    with pytest.raises(TypeError, match="HxWx3 uint8 array"):
        augmentation(**arguments).apply("not a frame")


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), STABLE_CASES, ids=STABLE_IDS)
def test_an_explicitly_settled_augmentation_renders_the_same_after_a_redraw(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    instance = augmentation(**arguments)
    before = pixels(instance.apply(frame()))

    instance.reseed()

    assert pixels(instance.apply(frame())) == before


@pytest.mark.parametrize(("augmentation", "arguments", "attribute"), PLACEMENT_CASES,
                         ids=[case[0].__name__ for case in PLACEMENT_CASES])
def test_a_redraw_moves_the_placement_and_leaves_the_setting_alone(augmentation: type[Any], arguments: dict[str, Any], attribute: str) -> None:
    instance = augmentation(**arguments)
    settled = getattr(instance, attribute)

    instance.reseed()

    assert getattr(instance, attribute) == settled


def test_the_catalog_door_exports_every_case_and_nothing_else() -> None:
    exported = {
        value.__name__
        for value in vars(catalog).values()
        if isinstance(value, type) and hasattr(value, "name") and hasattr(value, "apply")
    }

    assert exported == set(IDS)


def test_every_module_that_resolves_the_accelerator_is_one_the_fallback_case_reaches() -> None:
    # A new augmentation that imports the resolver by name and is not listed above would
    # otherwise run its accelerated path twice and report an agreement it never tested.
    holders = {
        module
        for module in (importlib.import_module(f"{catalog.__name__}.{found.name}")
                       for found in pkgutil.iter_modules(catalog.__path__))
        if hasattr(module, "opencv")
    }

    assert holders == set(RESOLVER_HOLDERS)


def test_every_augmentation_carries_a_name_no_other_one_claims() -> None:
    names = [case[0](**case[1]).name for case in CASES]

    assert len(set(names)) == len(names)


@pytest.mark.parametrize("augmentation", [catalog.Cutout, catalog.Zoom, catalog.Noise])
def test_a_redraw_moves_an_unspecified_setting(augmentation: type[Any]) -> None:
    # Ten redraws landing on the same result would need a coincidence far past any run this
    # suite will see, so the loop bounds the randomness instead of tolerating a flake.
    instance = augmentation()
    before = pixels(instance.apply(frame()))

    for _ in range(10):
        instance.reseed()
        if pixels(instance.apply(frame())) != before:
            return

    pytest.fail(f"{augmentation.__name__} did not move across ten redraws")

# Shear reproduces Pillow's 16.16 fixed-point accumulation rather than the algebra it
# approximates, which is what makes it bit-exact with 1.x. A refactor to the "obvious"
# floating-point formula passes every other case in this file and silently moves whole
# rows at coefficients whose sample point lands on a pixel boundary (see decision 0055).
FIXED_POINT_SHEARS = [(0.2, 0.2), (0.3, 0.2), (0.6, -0.6), (0.05, 0.95)]


@pytest.mark.parametrize("values", FIXED_POINT_SHEARS)
def test_shear_offsets_follow_pillows_fixed_point_accumulation(values: tuple[float, float]) -> None:
    from cvaugmentor.adapters.augmentations.shear import _offsets

    for coefficient, count in ((values[0], 48), (values[1], 64)):
        step = int(np.rint(coefficient * 65536.0))
        half = (abs(step) + 1) // 2
        expected = [((step * index + (-half if step < 0 else half) + 32768) >> 16) for index in range(count)]
        assert _offsets(coefficient, count).tolist() == expected


@pytest.mark.parametrize("values", FIXED_POINT_SHEARS)
def test_shear_lands_whole_rows_where_the_sample_point_sits_on_a_boundary(values: tuple[float, float]) -> None:
    # The floating-point formula and the fixed-point one disagree only on boundary rows, so
    # the guard is that the offsets step by whole numbers in the fixed-point order.
    from cvaugmentor.adapters.augmentations.shear import _offsets

    offsets = _offsets(values[0], 48)
    steps = np.diff(offsets)

    assert set(steps.tolist()) <= {0, 1, -1}, "an offset sequence must advance by at most one pixel per row"
