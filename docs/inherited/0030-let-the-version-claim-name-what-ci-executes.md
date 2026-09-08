# 0030. Let the version claim name what CI executes

Status: Accepted
Date: 2026-08-27

## Context

A note about future-proofing prompted a survey of where this package states
which Python it supports, and the answer was five places. The floor in
`pyproject.toml` said `>=3.13`, the trove classifier said 3.13, ruff's
`target-version` and mypy's `python_version` checked the 3.13 dialect, and CI
executed 3.14. The ends of that story disagree. The floor was declared and
dialect-checked but never executed, and the interpreter that actually ran was
claimed nowhere. In the family's own language, a range claim whose floor no
check runs is a completeness claim without a boundary.

The wider question the note asked is how code stays workable on interpreters
that do not exist yet. Python answers that itself. The backwards-compatibility
policy deprecates loudly for at least two releases before removing anything,
so every future removal announces itself as a `DeprecationWarning` years
early. This suite ran with those warnings scrolling past unread.

## Decision

The version story is one number, and the number is the one CI executes. The
floor, the classifier, the linter target, the type-checker target, and the CI
pin all say 3.14 now, and whoever bumps one bumps them all. A real package
built from this template widens the floor for its users by adding that floor
to the CI matrix, so the declared range never outgrows the proven one.

The test suite treats every warning as an error through
`filterwarnings = ["error"]`. Gating on the warning converts a breakage on a
future interpreter into a red test today, while the fix is cheap and
unhurried. An exception must be a named ignore for one specific message with a
reason beside it, never a blanket, the same honesty PGH already demands of
lint suppressions.

The ruling is family-wide. ArchtypeCore and Helm carry the same rule in their
own records, shaped to their genres, since an application claims one runtime
and a client claims an engine range.

## Options considered

- `from __future__ import annotations`, the era's famous future-proofing
  import, is refused. Python 3.14 evaluates annotations lazily by default, so
  the import now selects the superseded dialect, the one that broke runtime
  introspection in libraries like pydantic. On this floor every annotation
  form the house writes is already native, so the import buys nothing and
  points backward.
- An advisory CI job on the next interpreter's release candidate is refused
  for the template. It is recurring maintenance for a showcase, and the
  warnings gate gives earlier notice anyway, because a warning on 3.14 names a
  removal roughly two releases out while an rc job only reports a breakage
  once it exists.
- An upper bound on `requires-python` is refused permanently. A ceiling makes
  the resolver refuse interpreters that would have worked, which is the one
  genuinely anti-future move available in packaging metadata.
- Running both ends of a declared range in CI is the right shape for a shipped
  package and is not taken here, because the template claims a single version
  and doubling the jobs would prove a range the showcase does not promise.

## Consequences

The five version fields agree. When 3.15 releases, the bump is one sweep of
the same five fields, and any deprecation the suite started failing on has
been fixed long since. The README's Conventions section states the rule in one
paragraph so an instantiating project inherits it.

The warnings gate makes the suite stricter than the code it tests, which is
the point. The first dependency that starts warning turns the suite red
without any change to this repository, and that is the gate working, since the
alternative was learning the same fact from a broken upgrade two releases
later.
