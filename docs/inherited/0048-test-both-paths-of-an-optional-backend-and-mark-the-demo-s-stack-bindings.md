# 0048. Test both paths of an optional backend and mark the demo's stack bindings

Status: Accepted
Date: 2026-09-08

## Context

A project built from Keel moved its compute onto an optional accelerator
that ships no wheel for two of its target platforms, so every operation grew
a fallback implementation. Three fallbacks diverged from their accelerated
counterparts by up to 253 levels out of 255 and passed every case in the
suite, because the development machine had the accelerator and nothing ever
executed the fallback; one of the three was found only when the case ran
over a noise frame, since on a smooth gradient a wrong kernel lands on nearly
the same pixel. The same project had to delete three lines of the tool
configuration the adoption section calls law, the type checker's plugin for
the demo's validation library, the test runner's async mode, and the import
contract's ban on the demo's vendor SDK, because a child that uses none of
them cannot run the checks with them present, and reported the deletions as
a departure it could not classify. It also wrote eight helper docstrings as
one line of file, because the rulebook says a thin mapper keeps a one-line
summary while the audit holds the house rhythm.

## Decision

Where an optional dependency sits behind a port with a fallback
implementation, the suite executes both paths and holds them to a tolerance
a decision record states with the measurement that set it, over a fixture on
which the two can disagree. The test-honesty gate item and the map's testing
rules carry it as the fourth rule, because a fallback that only the machines
without the dependency ever run is dead code that reviews well.

Inside the tool configuration a line that binds the demo's own stack rather
than the style's rule is marked with a comment beginning Stack binding, and a
child re-adapts or removes such a line freely; everything unmarked is law.
Keel marks its validation plugin, its async mode, and its vendor SDK's two
lines; ArchetypeCore and Helm mark nothing, because their stacks are the
style's own.

The rulebook says a thin mapper keeps a summary of one sentence, in the house
rhythm, since one line of content was always what was meant and one line of
file is what the audit rejects.

## Options considered

- Requiring equality between the two paths was refused, because a vendor's
  arithmetic legitimately differs from its documented formula by a level or
  two, and a tolerance nobody recorded would widen quietly.
- Letting a child delete configuration lines by judgment was refused, since
  the adoption text said only names may change; marking the lines makes the
  permission decidable.

## Consequences

A fallback path is proven or absent. A child knows which configuration lines
it may touch by reading them. Eight docstrings a project wrote against the
rulebook's wording will not be written again.
