# 0057. Seed an instance, and draw a frame-dependent effect from a drawn seed

Status: Accepted
Date: 2026-09-08

## Context

An augmentation left without a setting draws one, so a dataset built from
unspecified settings could not be built again. Ten of the fifteen draw
something. The remaining five, the flips, the grayscale, the negative, the
no-op, and the rotation, take every setting they use from the caller.

Reproducibility was the last lever missing after the rewrite. Shear became
bit-exact with the previous major version, hue round-trips at zero error, and
cutout became deterministic, so the draws were the only thing standing between
a caller and rebuilding a dataset exactly.

## Evidence

A suite case comparing two instances built with the same seed, applied, then
redrawn as the batch runner redraws between items, failed on one of the ten:

```
Noise:  agree on the first frame        yes
        agree after reseed on both      NO
```

The cause is that the speckle was drawn from the instance's own generator
inside `apply`, so the generator's position depended on how many frames that
instance had already speckled. Two instances holding the same seed stayed in
step only while both had been applied the same number of times. The case that
caught it applied one of the pair before redrawing, which a batch pass does on
every item after the first.

Zoom already avoided this by drawing a value once and building a per-frame
generator from it, so the pattern was in the tree and only one augmentation
was outside it.

## Options considered

- **Give every augmentation a seed, for a uniform signature.** Rejected. Five
  of the fifteen draw nothing, and a parameter that cannot affect an output is
  a lie the reader has to test to disbelieve.
- **Seed the pipeline rather than each augmentation.** Rejected for now. It
  reads well and it hides which augmentation consumed which draw, so two
  pipelines differing by one augmentation would produce unrelated settings for
  all the others.
- **Leave the speckle drawn from the instance's generator and document the
  ordering.** Rejected. A seed whose meaning depends on the call count is a
  seed that works in a suite and fails in a pass.
- **Draw the effect's own seed once and build a generator from it per frame.**
  Chosen, following what zoom already did.

## Decision

An augmentation that draws a setting takes `seed` as its last constructor
parameter, and an augmentation that draws nothing does not take one. The seed
fixes the instance's generator, so every draw it ever makes follows from it,
including the ones a later `reseed` asks for. A whole pass therefore replays,
not merely its first item.

Where an effect depends on a frame size the instance cannot know until a frame
arrives, the instance draws a seed for that effect once, at reseed time, and
builds a generator from it per frame. Nothing is drawn from the instance's own
generator inside `apply`. `SEED_LIMIT` lives once in the shared frame helpers,
since two augmentations now derive a generator this way.

The suites read the seeded set off the constructor signatures and compare it
against the set of modules that build a generator, so an augmentation that
gains a draw and forgets its seed fails rather than passing quietly.

## Consequences

A dataset built from unspecified settings is reproducible by recording the
seeds, which is the last of the reproducibility levers this rewrite left open.

`seed=True` is accepted as seed 1, because `bool` is an `int` in Python and the
guard follows the shape every other guard in the catalog uses. Tightening only
this one would be an inconsistency worth more than the mistake it prevents.

Noise draws one more value per reseed than before, so a given seed produces
different settings than it would have under the previous ordering. Nothing
depends on that, seeds being new in this change.

Seeding the pipeline rather than the augmentation stays available and is not
foreclosed. It would sit above this, handing each registered augmentation a
seed derived from one, and this decision is what makes that possible later.
