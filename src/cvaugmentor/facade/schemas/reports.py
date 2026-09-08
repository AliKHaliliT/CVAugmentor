from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass(frozen=True, slots=True)
class ItemReport:

    """

    Facade schema for what one input medium produced.


    Attributes
    ----------
    source : Path
        The medium that was read.

    written : list[Path]
        Every path written from it.

    skipped_reason : str | None
        Why the medium was passed over, or None when it was augmented.

    """

    source: Path
    written: list[Path] = field(default_factory=list)
    skipped_reason: str | None = None


@dataclass(frozen=True, slots=True)
class AugmentationReport:

    """

    Facade schema for the concluded outcome of an augmentation pass.


    Attributes
    ----------
    kind : Literal["image", "video"]
        The medium kind the pass carried.

    mode : Literal["sequential", "singular"]
        The application mode the pass ran under.

    total_inputs : int
        How many input media the pass considered.

    total_written : int
        How many files it wrote.

    total_skipped : int
        How many input media it passed over.

    items : list[ItemReport]
        One entry per input medium, in the order they were read.

    """

    kind: Literal["image", "video"]
    mode: Literal["sequential", "singular"]
    total_inputs: int
    total_written: int
    total_skipped: int
    items: list[ItemReport] = field(default_factory=list)
