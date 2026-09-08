# Changelog

This file summarises what each release changes for the people who install it. The reasoning behind a change lives in [docs/decisions/](docs/decisions/), not here.

## 2.0.0

A full rewrite onto a Hexagonal Architecture. Every entry under Removed or Changed breaks a 1.x program, so read this section before upgrading.

### Removed

- The import name `CVAugmentor` is gone. The package is now imported as `cvaugmentor`, all lowercase, which is what PEP 8 asks of a module name. The name on PyPI is unchanged, so `pip install CVAugmentor` still works.
- The `Augmentations` namespace is now `augmentations`, reached as `from cvaugmentor import augmentations as aug`.
- `Pipeline()` no longer takes its augmentations per call. They are registered on a `PipelineBuilder`, which returns the `Pipeline`.
- Calling an augmentation instance directly no longer works. Each one now answers `apply(frame)`, which is the method its port declares.
- The exact version pins on NumPy, OpenCV, and Pillow are replaced by lower bounds, so CVAugmentor no longer forces a downgrade on the projects that install it. `colorama` is gone, having never been imported.
- `pydantic` and `tqdm` are no longer dependencies. The schemas are frozen dataclasses and progress is one rewritten terminal line.
- OpenCV is no longer a hard requirement. It moves to the `fast` and `video` extras, so `pip install CVAugmentor` now succeeds on Alpine and on Windows for ARM, where OpenCV publishes no wheel. Video needs `pip install "CVAugmentor[video]"`, and an attempt without it raises `UnsupportedMediaError` naming the command.
- A frame is no longer a Pillow image. Augmentations receive and return a contiguous HxWx3 `uint8` NumPy array in RGB order, so a third-party augmentation written against Pillow for 1.x must be updated.
- The generated Sphinx site and the `gh-pages` branch it lived on are gone. The docstrings are the API reference, and the written documentation is in the repository under `docs/`.

### Added

- `Translation`, an augmentation that slides a frame across its own canvas. Positive values move it right and down.
- The `fast` extra, carrying OpenCV and Intel ISA-L. With it a pass runs about ten times faster than 1.x; without it, about four, on the same lossless output.
- An optional `seed` on every augmentation that draws a setting, ten of the fifteen. It fixes every draw the instance makes, including the ones a redraw between batch items asks for, so a dataset built from unspecified settings can be built again. The five that draw nothing do not take one.
- `PipelineConfig.workers`, which sizes the pool that encodes outputs. `None` sizes it from the machine, and `1` keeps every write on the calling thread.
- This package's own PNG codec, used for reading the PNGs it wrote and for writing every PNG. It encodes a 1920x1080 frame in roughly 43 ms against Pillow's 300 ms at the same setting, and its files read back through Pillow and OpenCV unchanged.
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

- A pass is roughly ten times faster at 1920x1080 and five times faster at 256x256, measured over fifteen augmentations. Compression, not the augmentations, was the bottleneck, and the writes now run on a thread pool.
- Augmented output is 1.02x to 1.14x larger than 1.x wrote, because the PNG encoder applies one row filter rather than choosing per row. It remains lossless.
- `Hue` now shifts by the degrees it documents. In 1.x the shift was added straight to an eight-bit hue channel, so its unit was really 256ths of a turn and `Hue(40)` rotated 56.25 degrees. Divide a 1.x value by 256 and multiply by 360 to reproduce an old result.
- Hue is computed in float32 rather than on an eight-bit colour wheel, so a shift of zero or a full turn now returns the frame unchanged. Measured across the whole 8-bit colour cube, OpenCV's eight-bit hue round trip moves pixels by up to five levels while doing nothing at all.
- `Noise` redraws its speckle when an instance meets a frame of a different size, and does not restore an earlier size's pattern if it meets that size again. Within one video, or any batch of uniform size, the behaviour is unchanged.
- `Shear` reproduces 1.x pixel for pixel, and so does `Rotate` at any multiple of 90 degrees, which is where its default sits. `Rotate` at an arbitrary angle differs on at most 0.19 percent of pixels, each of which takes a neighbouring source pixel rather than an invented one. Axis flips are unchanged.
- `Cutout` now places each patch independently. In 1.x every patch of one frame landed at the same coordinates, because the placement was redrawn from a single stored seed inside the loop.

- Python 3.14 or newer is required.
- Images are converted to RGB when read. A palette or alpha channel no longer reaches an augmentation that cannot read it, at the cost of dropping transparency.
- `aug_verbose` is now `augmentation_verbose`, and the verbosity flags live on `PipelineConfig` rather than in the `augment` call.
- Progress bars name their unit in the singular, so tqdm renders `3.00image/s` rather than `3.00images/s`.
- Out-of-range settings that were previously accepted in silence are now refused: a negative blur radius, a negative exposure factor, and a non-positive cutout size or count.

## 1.1.2 and earlier

Released before this file existed. See the repository history.
