# 0049. Carry a frame as an RGB array

Status: Accepted
Date: 2026-09-08

## Context

[Decision 0042](0042-carry-a-frame-as-an-opaque-handle.md) settled that the
domain moves frames it cannot read, so `Frame` is `Any` and nothing in `domain`
or `services` inspects a pixel. It deliberately left open what the adapters
agree the carrier actually is. Until now that carrier was a Pillow image,
because Pillow was the image codec and every augmentation was written against
its API.

Moving the operations onto NumPy forces the question. An augmentation that
computes with arrays cannot accept a Pillow image without converting on entry
and on exit, and a conversion in every one of fifteen augmentations is fifteen
copies of the same buffer per frame.

## Evidence

Measured on one 1920x1080 RGB frame, comparing a specialised NumPy or OpenCV
implementation against the Pillow call it replaces:

```
brightness   23.5x    exposure   12.9x    noise        12.3x
saturation   11.9x    flip       10.5x    grayscale    10.3x
zoom         10.2x    shear       8.5x    negative      7.7x
translation   6.3x    rotate      5.1x    blur          4.6x
hue           0.9x
```

Fourteen of the fifteen are faster once the frame is already an array, and the
sole exception is hue, which pays for a colour-space round trip either way.

## Options considered

- **Keep Pillow images and convert inside each augmentation.** Rejected. The
  conversion is a full buffer copy in and another out, paid per augmentation
  per frame, which is most of the win handed back.
- **Make the carrier a union and let each adapter accept either.** Rejected.
  Every augmentation would carry a two-branch entry guard forever, and the
  union is a contract nobody can check because the annotation is `Any`.
- **State the carrier in the domain as an ndarray.** Rejected. That is the
  Dependency Rule violation 0042 exists to prevent, and the import contract
  forbids `numpy` in `domain` by name.
- **Agree the carrier among the adapters, leaving the domain annotation
  untouched.** Chosen.

## Decision

Every adapter this package ships agrees that a frame is a C-contiguous HxWx3
`uint8` NumPy array in RGB order. The agreement lives among the adapters and
in the comment beside `Frame`, never in the annotation, so 0042 holds exactly
as written.

One shared guard, `adapters/augmentations/frames.as_pixels`, validates the
contract at the entry of every augmentation and raises `TypeError` naming what
arrived. The codecs guarantee the shape on the way out and check it on the way
in.

## Consequences

Alpha channels and palettes are still flattened at the codec, which
[decision 0048](0048-convert-every-image-to-rgb-at-the-codec.md) already
settled, and the reason is now stronger because the array shape encodes it.

A third-party augmentation published to the entry-point group and written
against Pillow images breaks at the guard rather than silently producing
nothing. The guard's message names the expected shape so the failure explains
itself, and the major version carries the break.

RGB rather than OpenCV's native BGR is the order, so the video codec converts
in both directions. That cost is one pass per frame and it buys an order that
matches how everyone outside OpenCV describes colour.
