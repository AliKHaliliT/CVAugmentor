# 0056. Execute the fallback on musl and infer Windows on ARM

Status: Accepted
Date: 2026-09-08

## Context

The accelerators are optional, so every operation carries a second
implementation for the platforms where OpenCV and Intel ISA-L publish no
wheel. Those platforms are musl distributions and Windows on ARM. The suites
cover the fallback by resolving the backend to absent, which proves the branch
computes the right answer but says nothing about whether the package installs
and runs where the accelerators are genuinely unavailable.

The style now requires that both paths of an optional backend be executed
rather than one executed and the other asserted about, so the question is what
executing means for a platform no runner here can reach.

## Evidence

The hard dependencies publish wheels for both platforms at this project's
Python floor, verified by filename rather than by a platform summary:

```
numpy  2.5.3    numpy-2.5.3-cp314-cp314-musllinux_1_2_x86_64.whl
                numpy-2.5.3-cp314-cp314-musllinux_1_2_aarch64.whl
                numpy-2.5.3-cp314-cp314-win_arm64.whl
pillow 12.3.0   pillow-12.3.0-cp314-cp314-musllinux_1_2_x86_64.whl
                pillow-12.3.0-cp314-cp314-musllinux_1_2_aarch64.whl
                pillow-12.3.0-cp314-cp314-win_arm64.whl
```

Both platforms also carry free-threaded variants of the same wheels, which is
worth noting only because a filename search that stops at its first match finds
the free-threaded one and reads as though the standard interpreter were
unsupported.

## Options considered

- **Leave both platforms covered by substitution alone.** Rejected. It is the
  state the new rule was written against, and it cannot catch an install that
  fails before any test runs.
- **Withhold the extras on a glibc runner.** This was the first attempt and it
  is weaker than it looks, because the accelerators are absent by choice there
  rather than by necessity, so it proves the branch runs and not that the
  platform works. It is replaced rather than kept, since two jobs asking almost
  the same question is waste.
- **Add a Windows on ARM runner.** Rejected for now. The residue it would close
  is the narrowest of the three below, and the job would exist to re-prove a
  wheel table this record already quotes.
- **Execute on musl and name what stays inferred.** Chosen.

## Decision

A CI job runs the whole suite inside a `python:3.14-alpine` container, where
neither accelerator can be installed at all, and asserts before testing that
the backend resolved to no OpenCV and to the standard library's deflate. That
job replaces the one which withheld the extras on glibc.

It installs only the test tools rather than the whole development group,
because the job's question is whether the fallback works and a linter without a
musl wheel would break it while answering nothing.

What stays inferred is stated rather than implied. The fallback branch is
executed, on musl, in CI. Windows on ARM runs that same branch, so what is
inferred there is not the logic but whether the platform's own toolchain
installs the two wheels quoted above.

## Consequences

The fallback is proven on a platform that cannot have the accelerators, which
is what the rule asks for, and the STATE entry that carried this as deferred
work is closed rather than re-dated.

A Windows on ARM failure would be a first-report-from-a-user failure. That is
accepted because the branch is proven elsewhere, the wheels are published, and
the platform's share of this package's users is small enough that a runner
costs more than the risk it removes. Should a report arrive, the runner is the
fix and this record is the thing to supersede.

The Alpine job is slower than the glibc job it replaces, since it resolves
wheels for a less common platform. That is the price of asking a real question
instead of a convenient one.
