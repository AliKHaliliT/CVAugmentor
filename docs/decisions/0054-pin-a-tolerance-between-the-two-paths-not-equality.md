# 0054. Pin a tolerance between the two paths, not equality

Status: Accepted
Date: 2026-09-08

## Context

[Decision 0053](0053-declare-the-accelerators-optional-and-fall-back-in-code.md)
gives every accelerated operation a NumPy fallback, so the same augmentation
has two implementations and only one runs on a given machine. The obvious
contract to hold them to is that they produce identical bytes, because
otherwise a dataset depends on which extras a user installed.

Equality turned out to be unreachable for one operation, and the reason is
outside this package.

## Evidence

Grayscale over a random 240x320 frame, after the fallback was rewritten to use
OpenCV's own published fixed-point coefficients (4899, 9617, 1868 over 2^14,
with half a unit added before the shift):

```
accelerated vs fallback   max diff 1, on 633 of 76800 pixels
accelerated vs Pillow     max diff 1
fallback    vs Pillow     max diff 1
```

Saturation blends against that grey, so it inherits the gap multiplied by its
own factor:

```
factor  0.0   max diff 0
factor  0.5   max diff 1
factor  1.0   max diff 1
factor  1.5   max diff 2
factor  2.0   max diff 2
factor  3.0   max diff 3
```

Blur sits at one level for the same kind of reason, OpenCV's box filter
rounding its mean where the fallback's integer division floors it, which three
passes amplify until the half is added explicitly. Every other accelerated
operation matches its fallback exactly.

Two operations reached the tolerance only after being rewritten to meet it,
which is worth recording because both looked acceptable first time. Zoom's
fallback was a bilinear blend against an accelerated cubic and disagreed by 55
levels until the fallback was given OpenCV's own four-tap kernel at its own
coefficient of -0.75, after which the two agree exactly. Blur's fallback
replicated the edge row while OpenCV reflected it, and three passes turned that
into 22 levels along every margin until the border mode was named.

The residue is OpenCV's vectorised colour kernel rounding differently from the
scalar formula OpenCV itself documents. Reproducing that would mean
reimplementing a SIMD rounding schedule that is a build detail rather than a
contract, and which is free to change between OpenCV releases.

## Options considered

- **Compute grayscale in NumPy on both paths, discarding the accelerator.**
  Rejected. It buys exactness for about 23 ms per frame, and grayscale feeds
  saturation as well, so the pass gets roughly ten percent slower to remove a
  one-level difference no model can see.
- **Reverse-engineer OpenCV's vectorised rounding.** Rejected. It pins this
  package to an unpublished build detail, and the next OpenCV release is free
  to break it silently.
- **Assert equality and mark grayscale as a known failure.** Rejected. A
  suppressed assertion is a check that implies more than it decides.
- **State a tolerance, hold both paths to it, and name where it comes from.**
  Chosen.

## Decision

The two paths are held to agreement within one level per channel, not to
equality. Saturation's bound is that gap scaled by its own factor, since the
blend amplifies it arithmetically. The suites assert the tolerance and would
fail on a wider one, so a real divergence is still caught.

The coefficients live once, in `adapters/augmentations/frames.py`, so no
augmentation grows its own grey and the amplification has exactly one source.

## Consequences

A dataset built with the `fast` extra and one built without it are not
byte-identical. They differ by at most one level per channel outside
saturation, and saturation's factor bounds it. That is stated in the README so
nobody discovers it from a checksum.

Reproducing a dataset exactly therefore means recording whether the extra was
installed. Every other reproducibility lever, the draws each augmentation
makes, is already handled by seeding.

Any future accelerated operation is held to the same tolerance, and one that
cannot meet it is a defect rather than a new exception. The two operations that
missed it at first were both fixed by making the fallback compute what the
accelerator computes, rather than something equivalent-looking, which is the
general remedy.
