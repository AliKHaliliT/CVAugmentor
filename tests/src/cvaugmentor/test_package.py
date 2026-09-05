import logging
import os
import subprocess
import sys

# Library citizenship, pinned: the package logger stays silent by default, importing the
# package reads no environment, and the version is the one pyproject declares.


def test_the_package_logger_carries_a_null_handler() -> None:
    import cvaugmentor  # noqa: F401

    handlers = logging.getLogger("cvaugmentor").handlers
    assert any(isinstance(handler, logging.NullHandler) for handler in handlers)


def test_importing_the_package_needs_no_environment() -> None:
    # A clean interpreter with an emptied environment imports the package or it does not;
    # an import-time environment read would crash right here.
    result = subprocess.run(
        [sys.executable, "-c", "import cvaugmentor"],
        env={"PATH": os.environ.get("PATH", ""), "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")},
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr


def test_the_package_version_is_the_one_the_project_declares() -> None:
    import tomllib

    import cvaugmentor

    with open("pyproject.toml", "rb") as manifest:
        declared = tomllib.load(manifest)["project"]["version"]

    assert cvaugmentor.__version__ == declared


def test_the_public_surface_is_curated_rather_than_whatever_leaked() -> None:
    import cvaugmentor

    assert set(cvaugmentor.__all__) == {
        "AugmentationException",
        "AugmentationReport",
        "ItemReport",
        "Pipeline",
        "PipelineBuilder",
        "PipelineConfig",
        "__version__",
        "augmentations",
    }
