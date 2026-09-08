# 0055. Reproduce Pillow's fixed-point accumulation for nearest resampling

Status: Accepted
Date: 2026-09-08

## Context

`Shear` and `Rotate` resample with nearest neighbour, so each output pixel
names exactly one source pixel. 1.x named it through Pillow's affine
transform. The rewrite computes the map itself, and the goal was to reproduce
1.x exactly so an existing dataset stays reproducible.

The first attempt implemented the algebra the transform documents, sampling the
centre of each output pixel and flooring. It was close and not exact, and
chasing the gap turned out to be the whole lesson.

## Evidence

Pillow's map was recovered by transforming an image whose pixels encode their
own coordinates, then reading which source pixel each output pixel received.

Fitting the documented algebra against that map, over five shear values and
three frame shapes, and then over ten values:

```
src_x = trunc((x+0.5) + sx*(y+0.5))   src_y = trunc(sy*(x+0.5) + (y+0.5))   2628/2833
src_x = trunc((x+0.5) + sx*(y+0.0))   src_y = trunc(sy*(x+0.5) + (y+0.5))   2509/2833
src_x = trunc((x+0.5) + sx*(y+0.5))   src_y = trunc(sy*(x+0.0) + (y+0.5))   2418/2833

widened to ten shear values: 96.04% of in-bounds pixels
```

Nudging exact boundaries downward, on the theory that Pillow resolves ties one
way, made it worse, which showed the residue was not a tie-breaking rule:

```
no epsilon      1393 disagreements of 35145    96.04% exact
epsilon 1e-12   4502 disagreements of 35145    87.19% exact
```

The cause is that Pillow does not evaluate the algebra at all. It walks each
scanline in 16.16 fixed point, rounding the coefficient into that
representation once and stepping by it, so a coordinate landing on a pixel
boundary falls a hair to one side of it. Fitting the accumulation instead of
the algebra, over twelve coefficients and three variants each of the
coefficient conversion, the half-step, and the added constant:

```
576/576   coefficient=round   half-step=round(a/2)   constant=32768
575/576   coefficient=round   half-step=round(a/2)   constant=32767
566/576   coefficient=trunc   half-step=round(a/2)   constant=32768
```

Held against Pillow over 567 combinations spanning 27 shear values including
negatives, seven frame shapes including a single row and a single column, and
1,274,432 in-bounds pixels:

```
disagreements: 0    100.0000% exact
```

Against real 1.x, over 45 shear cases on five frame shapes, both the
accelerated and the fallback path differ by 0. On the sample photograph, the
shear of 0.2 that previously moved 29.2 percent of pixels now moves none.

Rotate keeps a small residue, measured on the same photograph:

```
0, 90, 180, 270, -90 degrees   0.00% of pixels differ
30 degrees                     0.00%
45 degrees                     0.02%,  max 76
-23 degrees                    0.07%,  max 63
137 degrees                    0.15%,  max 114
33.5 degrees                   0.17%,  max 115
7 degrees                      0.19%,  max 105
```

## Options considered

- **Implement the documented algebra and accept 96 percent.** Rejected once
  the accumulation was understood. A shear of 0.2 puts the sample point on a
  boundary every fifth row, so the 4 percent concentrates into whole rows and
  moved 29 percent of a real frame.
- **Keep Pillow for these two operations.** Rejected. It reinstates the
  dependency for the operations most worth accelerating, and the frame is now
  an array, so the conversion would round anyway.
- **Move to bilinear, which has no tie to break.** Rejected. It changes the
  augmentation both versions documented and softens edges nearest neighbour
  keeps hard.
- **Reproduce the fixed-point accumulation.** Chosen.

## Decision

Shear computes its per-row and per-column offsets in 16.16 fixed point, with
the coefficient rounded into that representation, a half-step of
`round(|a|/2)` carrying the sign, and 32768 added before the shift. That is
Pillow's own accumulation rather than an approximation of it, and it is
bit-exact with 1.x everywhere tested.

Rotate computes a whole-number source map in double precision and gathers
through it. It is exact for every multiple of 90 degrees, which is where its
default sits, and differs on at most 0.19 percent of pixels at an arbitrary
angle. That residue is left rather than chased, because a rotation accumulates
along two axes at once and the same fitting exercise would have to be redone
for a case whose default is already exact.

Both operations compute one integer map and then gather, through `cv2.remap`
on whole-number maps where OpenCV is present and through NumPy indexing
otherwise, so the two paths agree with each other exactly.

## Consequences

A 1.x dataset built with `Shear` is reproducible byte for byte. One built with
`Rotate` at a multiple of 90 degrees is too. One built with `Rotate` at an
arbitrary angle is reproducible except on a fraction of a percent of pixels,
each of which takes a real neighbouring pixel rather than an invented one.

The general lesson is recorded because it will recur. Where a rewrite has to
match a legacy implementation's sampling, the thing to reproduce is the
arithmetic the legacy code performed, not the formula it was approximating. The
fit for the algebra topped out at 96 percent and looked like a floating-point
wall. The fit for the accumulation was exact on the first try.

Emulating a vendor's fixed point is a real coupling, and it is accepted here
because the accumulation is simple, it is pinned by suites over a wide sweep of
values, and Pillow is no longer the implementation, so nothing upstream can
move underneath it.
