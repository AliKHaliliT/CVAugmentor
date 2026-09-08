# Project State

## Now

- Nothing in flight.

## Next

- Give every augmentation an optional seed, so a dataset built from a random draw can be rebuilt from the same one (2026-09-05).

## Deferred

- The fallback CI job runs the NumPy paths with no extras installed, but only on glibc x86-64, so musl and Windows-on-ARM are still covered by inference from the wheel table rather than by a run (2026-09-08).

## Blocked

- GitHub Pages still names the deleted gh-pages branch as its source and must be turned off in the repository settings, which no command in this tree can reach (2026-09-05).
