from typing import Any

import pytest
from PIL import Image

from cvaugmentor.adapters import augmentations as catalog
from cvaugmentor.domain.interfaces import IAugmentation

# Every augmentation is built with explicit settings here, because a case asserting that a
# frame changed must not depend on which value a draw happened to land on. The catalog is
# read off the package door, so a new augmentation that is exported is covered the moment it
# lands and one that is not exported fails the door case below.
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
    (catalog.Saturation, {"saturation_factor": -1}, True),
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


def frame() -> Image.Image:

    """A colourful gradient, so an augmentation that changes colour visibly does."""

    canvas = Image.new("RGB", (64, 48))
    canvas.putdata([(x * 4 % 256, y * 5 % 256, (x + y) * 3 % 256) for y in range(48) for x in range(64)])
    return canvas


def pixels(image: Image.Image) -> bytes:
    return image.tobytes()


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_every_augmentation_satisfies_the_port_it_is_registered_under(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    assert isinstance(augmentation(**arguments), IAugmentation)


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_every_augmentation_returns_a_frame_of_the_size_it_was_given(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    original = frame()

    augmented = augmentation(**arguments).apply(original)

    assert isinstance(augmented, Image.Image)
    assert augmented.size == original.size


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_every_augmentation_changes_the_frame_unless_it_promises_not_to(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    original = frame()

    augmented = augmentation(**arguments).apply(original)

    assert (pixels(augmented) != pixels(original)) is changes


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_one_instance_treats_every_frame_the_same_way(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    # This is what keeps a video coherent: the same instance crosses every frame of it, so a
    # parameter drawn once must not be redrawn per call.
    instance = augmentation(**arguments)

    assert pixels(instance.apply(frame())) == pixels(instance.apply(frame()))


@pytest.mark.parametrize(("augmentation", "arguments", "changes"), CASES, ids=IDS)
def test_a_frame_that_is_not_an_image_is_refused(augmentation: type[Any], arguments: dict[str, Any], changes: bool) -> None:
    with pytest.raises(TypeError, match="PIL Image"):
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
