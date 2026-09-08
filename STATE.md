# Project State

## Now

- Nothing in flight.

## Next

- Give every augmentation an optional seed, so a dataset built from a random draw can be rebuilt from the same one (2026-09-05).

## Deferred

- The NumPy fallbacks are covered by resolving the accelerator to None rather than by running on a machine that genuinely lacks OpenCV, so the musl and Windows-on-ARM paths are verified by substitution and not in place (2026-09-08).

## Blocked

- GitHub Pages still names the deleted gh-pages branch as its source and must be turned off in the repository settings, which no command in this tree can reach (2026-09-05).
