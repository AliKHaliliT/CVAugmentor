# 0046. Declare dependencies as lower bounds

Status: Accepted
Date: 2026-09-05

## Context

Version 1.x pinned every dependency to an exact version: `numpy==2.2.2`,
`opencv-python==4.11.0.86`, `Pillow==11.1.0`, `tqdm==4.67.1`, and
`colorama==0.4.6`. That is the right shape for an application, which controls
its own environment. CVAugmentor is a library, and a library's pins become
constraints on every project that installs it.

The practical effect is that any project already using a different NumPy could
not install CVAugmentor without downgrading, and two libraries pinned this way
to different versions of the same dependency cannot be installed together at
all.

`colorama` was pinned and never imported anywhere in the package.

## Evidence

Resolving the package's actual imports on Python 3.14 today produces NumPy
2.5.2, Pillow 12.3.0, opencv-python 5.0.0.93, and tqdm 4.70.0. Every one of
those is a major or minor step beyond what 1.x pinned, and the package's full
suite plus an end-to-end pass over sample images and video runs green on them.
So the pins were not describing a tested combination. They were describing the
versions that happened to be installed when the file was written.

## Options considered

- **Keep exact pins.** Reproducible for a maintainer, and an installation
  conflict for a user.
- **Pin an upper bound as well, such as `numpy>=2,<3`.** Defensible for a
  dependency with a history of breaking changes, and it forces a release of this
  package every time a dependency crosses a major, whether or not anything broke.
  The evidence above is that OpenCV crossed from 4 to 5 without breaking a call
  this package makes.
- **Lower bounds at the version whose API the code actually uses.** States a
  fact the maintainer can defend and leaves the resolver free.

## Decision

Dependencies are declared as lower bounds, each set at the version whose API the
package is written against: `numpy>=2`, `opencv-python>=4.11`, `pillow>=11`,
`pydantic>=2`, `tqdm>=4.67`. `colorama` is dropped.

## Consequences

A floor is a claim, so it has to be true. `opencv-python>=4.11` says this
package's `cv2.VideoWriter.fourcc` and capture-property calls work from 4.11
onward, and it was chosen because 1.x already required that version, not because
every release between it and 5.0 was tested here.

Nothing upstream stops this package from breaking when a dependency does. That
risk was always present and was hidden rather than removed by the pins, since a
pinned version is only tested until the day it is written. The gate is what
catches it now, and it runs on the resolver's current answer rather than on a
frozen one.

Dropping `colorama` removes a dependency the package never imported. tqdm still
installs it on Windows for its own colouring, so nothing about the terminal
output changes.
