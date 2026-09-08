# 0053. Declare the accelerators optional and fall back in code

Status: Accepted
Date: 2026-09-08

## Context

The fast paths need OpenCV for the operations and Intel ISA-L for deflate.
Declaring both as ordinary dependencies is what a package normally does, and
here it would break `pip install` outright on platforms where the two publish
no wheel, because pip then falls back to a source build that needs CMake and a
C toolchain and will not succeed on a user's machine.

## Evidence

Wheels published for the current release of each distribution:

```
platform            numpy   pillow   opencv-headless   isal
Windows x64          yes     yes           yes          yes
Windows ARM64        yes     yes           NO           NO
macOS Intel          yes     yes           yes          yes
macOS Apple Si       yes     yes           yes          yes
Linux x64 glibc      yes     yes           yes          yes
Linux ARM glibc      yes     yes           yes          yes
Linux x64 musl       yes     yes           NO           yes
Linux ARM musl       yes     yes           NO           yes
```

NumPy and Pillow cover all eight. OpenCV misses three.

What the fallback costs, over one 1920x1080 image and fifteen augmentations:

```
1.x, Pillow throughout, serial                    4762 ms
fallback, NumPy and stdlib zlib, threaded         1157 ms    4.1x
full stack, OpenCV and ISA-L, threaded             449 ms   10.6x
```

The fallback is four times faster than the version it replaces, so no platform
regresses.

## Options considered

- **Require both.** Rejected. `pip install cvaugmentor` fails on three of
  eight platforms, which is not a supported package.
- **Require them behind a `platform_machine` marker.** Rejected. It excludes
  Windows on ARM correctly and cannot express musl at all, since PEP 508 has
  no libc marker. Half a fix reads as a whole one.
- **Vendor a compiled extension for the sequential kernels.** Rejected here.
  It would need wheels for the same eight platforms, which is the problem
  restated with a build matrix attached.
- **Require NumPy and Pillow, offer the accelerators as extras, and fall back
  at runtime.** Chosen.

## Decision

`numpy` and `pillow` are the only hard dependencies. The `fast` extra carries
`opencv-python-headless` and `isal`, and the `video` extra carries OpenCV
alone.

`core/acceleration` resolves both at import through a guarded import and
exposes `opencv()`, which returns the module or `None`, plus `deflate` and
`inflate`, which route to whichever backend answered. Every operation with a
NumPy fallback asks and takes it. Video has no fallback, so `OpenCvVideoCodec`
raises `UnsupportedMediaError` naming the install command, and it raises when
video work arrives rather than when it is constructed. Construction has to stay
safe because the builder registers a default codec for every medium kind, so a
constructor that demanded OpenCV would make an image-only pipeline unbuildable
on exactly the platforms this decision exists to serve.

The headless OpenCV build is the one named, because this package never opens a
window and the plain build additionally needs `libGL`, which is the most common
way an OpenCV dependency fails inside a container.

## Consequences

A plain `pip install cvaugmentor` works on every platform NumPy and Pillow
reach and runs about four times faster than 1.x. Reaching the full speed, and
reaching video at all, means installing an extra, which the README states as
the recommended install rather than as a footnote.

Two code paths per accelerated operation now exist, and only one of them runs
on any given machine. The suite exercises both by resolving the accelerator to
`None`, because a fallback that is never executed is a fallback that does not
work.

A `platform_machine` marker is deliberately absent. Alpine users get a clear
resolution failure from pip on the extra, which is a better signal than a
partial marker that silently drops the accelerators on a platform that could
have used them.
