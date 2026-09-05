import argparse
from collections.abc import Sequence

from cvaugmentor.adapters import augmentations as catalog
from cvaugmentor.core.config import PipelineConfig
from cvaugmentor.domain.exceptions import AugmentationException
from cvaugmentor.facade.pipeline.builder import PipelineBuilder

# The door at cvaugmentor/adapters/augmentations is the one list of what ships, so the
# catalog is read back off it rather than retyped here and left to drift.
CATALOG = {
    value.name: value
    for value in vars(catalog).values()
    if isinstance(value, type) and hasattr(value, "name") and hasattr(value, "apply") and hasattr(value, "reseed")
}


def build_parser() -> argparse.ArgumentParser:

    """

    Builds the command-line parser.


    Parameters
    ----------
    None.


    Returns
    -------
    argparse.ArgumentParser
        The parser the console script drives.


    Raises
    ------
    None.

    """

    parser = argparse.ArgumentParser(prog="cvaugmentor",
                                     description="Augment images and videos for computer vision tasks.")
    parser.add_argument("input_path", nargs="?", help="the medium to read, or the directory holding them")
    parser.add_argument("output_path", nargs="?", help="the medium to write, or the directory to write into")
    parser.add_argument("--target", choices=("image", "video"), default="image", help="what the paths carry")
    parser.add_argument("--process", choices=("single", "batch"), default="single", help="whether the paths are files or directories")
    parser.add_argument("--mode", choices=("sequential", "singular"), default="sequential", help="one output per augmentation, or one output in total")
    parser.add_argument("--augmentation", action="append", choices=sorted(CATALOG), metavar="NAME",
                        help="an augmentation to apply at its default settings; repeatable")
    parser.add_argument("--all", action="store_true", help="apply every built-in augmentation")
    parser.add_argument("--quiet", action="store_true", help="draw no progress bars")
    parser.add_argument("--random-state", action="store_true", help="redraw random parameters between batch items")
    parser.add_argument("--list", action="store_true", help="list the built-in augmentations and exit")

    return parser


def main(argv: Sequence[str] | None = None) -> int:

    """

    Runs one augmentation pass from the command line.


    Parameters
    ----------
    argv : Sequence[str] | None, optional
        The arguments to parse, or None to read them from the process.


    Returns
    -------
    exit_status : int
        Zero when the pass finished, non-zero when it did not.


    Raises
    ------
    None.

    """

    parser = build_parser()
    arguments = parser.parse_args(argv)

    if arguments.list:
        for name in sorted(CATALOG):
            print(name)
        return 0

    if arguments.input_path is None or arguments.output_path is None:
        parser.error("input_path and output_path are required unless --list is given")

    chosen = sorted(CATALOG) if arguments.all else (arguments.augmentation or [])
    if not chosen:
        parser.error("choose at least one augmentation with --augmentation, or --all")

    builder = PipelineBuilder().with_config(PipelineConfig(verbose=not arguments.quiet,
                                                           augmentation_verbose=not arguments.quiet,
                                                           random_state=arguments.random_state))
    for name in chosen:
        builder.with_augmentation(CATALOG[name]())

    try:
        report = builder.build().augment(arguments.input_path,
                                         arguments.output_path,
                                         arguments.target,
                                         arguments.process,
                                         arguments.mode)
    except (AugmentationException, ValueError) as error:
        print(f"cvaugmentor: {error}")
        return 1

    print(f"Wrote {report.total_written} file(s) from {report.total_inputs} input(s), skipping {report.total_skipped}.")

    return 0
