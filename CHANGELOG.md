# Changelog

This file summarises what each release changes for the people who install it. The reasoning behind a change lives in [docs/decisions/](docs/decisions/), not here.

## 2.0.0

A full rewrite onto a Hexagonal Architecture. Every entry under Removed or Changed breaks a 1.x program, so read this section before upgrading.

### Removed

- The import name `CVAugmentor` is gone. The package is now imported as `cvaugmentor`, all lowercase, which is what PEP 8 asks of a module name. The name on PyPI is unchanged, so `pip install CVAugmentor` still works.
- The `Augmentations` namespace is now `augmentations`, reached as `from cvaugmentor import augmentations as aug`.
- `Pipeline()` no longer takes its augmentations per call. They are registered on a `PipelineBuilder`, which returns the `Pipeline`.
- Calling an augmentation instance directly no longer works. Each one now answers `apply(frame)`, which is the method its port declares.
- The exact version pins on NumPy, OpenCV, Pillow, and tqdm are replaced by lower bounds, so CVAugmentor no longer forces a downgrade on the projects that install it. `colorama` is gone, having never been imported.
- The generated Sphinx site and the `gh-pages` branch it lived on are gone. The docstrings are the API reference, and the written documentation is in the repository under `docs/`.

### Added

- `Translation`, an augmentation that slides a frame across its own canvas. Positive values move it right and down.
- A command-line interface. `cvaugmentor input.png output.png --all` augments from a shell, and `--list` names every built-in augmentation.
- `Pipeline.augment` now returns an `AugmentationReport` saying what was written and what was skipped, instead of returning nothing.
- A batch run no longer dies on one unreadable file. The failure is recorded against that item and the rest of the directory continues, unless `PipelineConfig(halt_on_error=True)` says otherwise.
- The same augmentation can be registered twice under different labels, so `Blur(1.0)` and `Blur(5.0)` can run in one sequential pass.
- Third-party augmentations can be published to the `cvaugmentor.augmentations` entry-point group and picked up with `PipelineBuilder().with_discovered_augmentations()`.
- The package ships as typed, carrying a PEP 561 `py.typed` marker.

### Fixed

- Video frames were passed to Pillow in OpenCV's channel order, so every colour-dependent augmentation read blue as red. `Hue`, `Saturation`, `Grayscale`, and `Negative` now act on the colours a video actually has.
- `Cutout` punched every square in the same place, because it rebuilt its generator from one seed inside its own loop. A count above one now places that many squares.
- `Zoom` raised a `ValueError` when the requested window matched the frame's width or height. A window at least that large is now clamped to the frame.
- Importing the package no longer calls `logging.basicConfig`, which had been reconfiguring the root logger of whatever program imported it. Warnings now go to the `cvaugmentor` logger, which carries a `NullHandler` and stays silent until an application configures logging.
- Augmentations no longer draw from NumPy's global random state, so importing and using CVAugmentor cannot perturb another library's reproducible sequence.

### Changed

- Python 3.14 or newer is required.
- Images are converted to RGB when read. A palette or alpha channel no longer reaches an augmentation that cannot read it, at the cost of dropping transparency.
- `aug_verbose` is now `augmentation_verbose`, and the verbosity flags live on `PipelineConfig` rather than in the `augment` call.
- Progress bars name their unit in the singular, so tqdm renders `3.00image/s` rather than `3.00images/s`.
- Out-of-range settings that were previously accepted in silence are now refused: a negative blur radius, a negative exposure factor, and a non-positive cutout size or count.

## 1.1.2 and earlier

Released before this file existed. See the repository history.
