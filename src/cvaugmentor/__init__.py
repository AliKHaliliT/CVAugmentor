from importlib.metadata import PackageNotFoundError, version
from logging import NullHandler, getLogger

from cvaugmentor.adapters import augmentations
from cvaugmentor.core.config import PipelineConfig
from cvaugmentor.core.logging import PACKAGE_LOGGER_NAME
from cvaugmentor.domain.exceptions import AugmentationException
from cvaugmentor.facade.pipeline import Pipeline, PipelineBuilder
from cvaugmentor.facade.schemas import AugmentationReport, ItemReport

try:
    __version__ = version("cvaugmentor")
except PackageNotFoundError:
    __version__ = "0.0.0"

getLogger(PACKAGE_LOGGER_NAME).addHandler(NullHandler())

__all__ = [
    "AugmentationException",
    "AugmentationReport",
    "ItemReport",
    "Pipeline",
    "PipelineBuilder",
    "PipelineConfig",
    "__version__",
    "augmentations",
]
