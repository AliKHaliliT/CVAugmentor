from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class ItemReport(BaseModel):

    """

    Facade schema for what one input medium produced.

    """

    source: Path
    written: list[Path] = Field(default_factory=list)
    skipped_reason: str | None = None


class AugmentationReport(BaseModel):

    """

    Facade schema for the concluded outcome of an augmentation pass.

    """

    kind: Literal["image", "video"]
    mode: Literal["sequential", "singular"]
    total_inputs: int
    total_written: int
    total_skipped: int
    items: list[ItemReport] = Field(default_factory=list)
