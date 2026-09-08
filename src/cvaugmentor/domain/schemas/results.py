from dataclasses import dataclass, field
from pathlib import Path

from cvaugmentor.domain.schemas.jobs import ApplyMode
from cvaugmentor.domain.schemas.media import MediaKind


@dataclass(frozen=True, slots=True)
class ItemOutcome:

    """

    What one input medium produced, or why it produced nothing.


    Attributes
    ----------
    source : Path
        The medium the runner read.

    written : list[Path]
        Every path written from it, empty when the medium was skipped.

    skipped_reason : str | None
        Why the medium was passed over, or None when it was augmented.

    """

    source: Path
    written: list[Path] = field(default_factory=list)
    skipped_reason: str | None = None

    @property
    def was_skipped(self) -> bool:

        """

        Whether the runner passed this medium over instead of augmenting it.

        """

        return self.skipped_reason is not None


@dataclass(frozen=True, slots=True)
class JobResult:

    """

    The concluded outcome of an augmentation job.


    Attributes
    ----------
    kind : MediaKind
        The medium kind the job carried.

    mode : ApplyMode
        The application mode the job ran under.

    outcomes : list[ItemOutcome]
        One entry per input medium, in the order the runner read them.

    """

    kind: MediaKind
    mode: ApplyMode
    outcomes: list[ItemOutcome] = field(default_factory=list)

    @property
    def written(self) -> list[Path]:

        """

        Every path the job wrote, across all of its input media.

        """

        return [path for outcome in self.outcomes for path in outcome.written]

    @property
    def skipped(self) -> list[ItemOutcome]:

        """

        Every input medium the job passed over.

        """

        return [outcome for outcome in self.outcomes if outcome.was_skipped]
