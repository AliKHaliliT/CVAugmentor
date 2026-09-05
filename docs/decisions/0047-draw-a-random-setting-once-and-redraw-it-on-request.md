# 0047. Draw a random setting once and redraw it on request

Status: Accepted
Date: 2026-09-05

## Context

An augmentation left without a setting draws one. Two requirements pull that
draw in opposite directions. Within one video every frame must be treated
identically, or the result crawls and flickers. Across a dataset each file
should differ, or the augmentation has added no variety.

Version 1.x met both, and the mechanism is worth recording because it was
invisible. A parameter was drawn in `__init__`, and the batch loop re-ran
variety by calling the constructor again on a live instance:

```python
if random_state:
    for instance in augmentations.values():
        instance.__init__()
```

Calling a dunder by hand on an existing object is not something a reader expects,
it cannot be typed, and it silently requires that every augmentation's
constructor stay safe to run twice on the same object forever.

Two augmentations needed more than a value, because where an effect lands
depends on a frame size not known until the frame arrives. Version 1.x handled
that by storing a seed and rebuilding a generator from it. `Cutout` rebuilt the
generator inside its placement loop, so every square in one frame was drawn from
the same seeded sequence and landed in the same place, which made `max_count`
above one do nothing.

## Options considered

- **Keep the constructor call.** Free, and it leaves the package's variety
  mechanism expressed as a trick no interface declares.
- **Draw per frame.** Removes the need for a redraw and destroys video
  coherence, which is the requirement the whole design exists for.
- **Make randomness a port and inject a source.** The most testable shape, and
  it does not by itself answer when a value is redrawn, which is the actual
  question. It also puts a seam in front of fifteen small classes that each use
  it once.
- **Declare a `reseed()` method on the port.** Names the operation the batch
  loop was already performing and lets each augmentation say what a redraw means
  for it.

## Decision

`IAugmentation` declares `reseed()`. A setting the caller gave is held; a
setting the caller left out is drawn from the instance's own generator, at
construction and again on every `reseed()`. Where placement depends on frame
size, the instance holds a seed rather than a position, redraws that seed on
`reseed()`, and builds one generator per frame from it so that a frame of a
given size is always placed identically while the squares within it are not.

Each augmentation owns a `numpy.random.default_rng()` of its own rather than
calling into NumPy's global functions, so importing and using this package
cannot disturb a sequence another library is relying on.

## Consequences

`Cutout` with a count above one now places that many squares, because the
per-frame generator is built once and drawn from repeatedly rather than rebuilt
per square. The README figure shows it.

A redraw moves placement even when the size was given explicitly, since where an
effect lands was never a setting the caller supplied. The catalog suite states
that as two separate cases, one holding that an explicitly settled augmentation
renders identically after a redraw, and one holding that the three placing
augmentations keep their setting while their placement is free to move.

Reproducibility is still missing. Nothing here lets a caller fix a seed and
rebuild a dataset exactly, because the generators seed themselves from the
operating system. Adding an optional seed to every constructor is the obvious
next step and is queued in STATE.md rather than done here.
