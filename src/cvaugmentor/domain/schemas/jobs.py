from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from cvaugmentor.domain.schemas.media import MediaKind

ApplyMode = Literal["sequential", "singular"]
ProcessType = Literal["single", "batch"]


@dataclass(frozen=True, slots=True)
class AugmentationJob:

    """

    Domain schema describing one requested pass over the filesystem.


    Attributes
    ----------
    source : Path
        The medium to read, or the directory holding the media to read.

    destination : Path
        The medium to write, or the directory to write the media into.

    kind : MediaKind
        Whether the job carries images or moving pictures.

    process_type : ProcessType
        Whether the paths name one medium or two directories.

    mode : ApplyMode
        Whether each augmentation is saved on its own or all are chained into
        one output.

    """

    source: Path
    destination: Path
    kind: MediaKind
    process_type: ProcessType
    mode: ApplyMode
