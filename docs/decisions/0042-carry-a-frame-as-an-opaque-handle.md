# 0042. Carry a frame as an opaque handle

Status: Accepted
Date: 2026-09-05

## Context

The Dependency Rule says the domain and the services import no SDK. This
package's whole subject is pixels, and every pixel it touches arrives from
Pillow or OpenCV, so the rule and the subject meet head on in one place: the
type of the thing the runner passes from a codec to an augmentation and back.

The runner's loop needs to hold that value, hand it around, and collect what
comes back. It never needs to read it. Nothing in `domain` or `services` asks a
frame its size, its mode, or the value of a pixel; those questions belong to the
codecs and the augmentations, which sit on the outside and are allowed their
libraries.

## Options considered

- **Type the ports against `PIL.Image.Image`.** The honest description of what
  actually flows, and an immediate violation. The domain would import Pillow,
  the import contract would fail, and swapping the imaging library would become
  a change to the core rather than to an adapter.
- **Define a neutral domain frame and convert at both boundaries.** Correct on
  paper and expensive in practice. Every frame of every video would be marshalled
  into a NumPy array or a bytes buffer and back for no reader, which is a
  per-frame cost paid to satisfy a type nobody consults. It also puts NumPy in
  the domain, moving the violation rather than removing it.
- **Define a Protocol describing the parts of an image the core uses.** The core
  uses none of them, so the Protocol would be empty, which is a longer way of
  writing the option below.
- **Carry the frame as an opaque handle.** The domain declares `Frame` as an
  alias for `Any` with a comment saying why, and the ports are typed against it.

## Decision

A frame crosses the core as an opaque handle. `cvaugmentor.domain.schemas.media`
declares `Frame`, the codecs and the augmentations agree that the concrete
carrier is a Pillow image, and nothing between them looks.

## Consequences

The import contract passes for a real reason rather than a bookkeeping one, and
`lint-imports` reports the domain and the services free of Pillow, OpenCV,
NumPy, and tqdm over the whole graph.

Type checking stops at the boundary. Inside an adapter, mypy sees a real image
and checks the calls made on it; in the runner it sees `Any` and checks nothing,
which is exactly the trade, since the runner makes no calls on it. A frame of
the wrong kind is caught by the augmentation's own guard rather than by the type
checker, one layer later than a concrete type would catch it.

The suites got the better half of the bargain. Because the runner cannot inspect
a frame, its tests carry plain strings, and a fake codec is a few lines with no
image library involved. That is why the runner's suite runs in milliseconds and
asserts on exact values rather than on pixel tolerances.

The cost lands if a future augmentation ever needs the core to know something
about a frame, a per-frame size check in the runner being the likely case. That
would be the point to revisit this, and the answer then is a small typed
descriptor travelling beside the handle rather than opening the handle itself.
