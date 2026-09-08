# Project State

## Now

- Nothing in flight.

## Next

- Give every augmentation an optional seed, so a dataset built from a random draw can be rebuilt from the same one (2026-09-05).

## Deferred

- The fallback CI job runs the NumPy paths with no extras installed, but only on glibc x86-64, so musl and Windows-on-ARM are still covered by inference from the wheel table rather than by a run (2026-09-08).

## Blocked

- Re-alignment to Keel commit 8367603 is analysed and waiting on the owner's ruling on record numbering, because the template's new records claim 0042 to 0044 and this project's own records already hold 0042 to 0055 (2026-09-08).
