# 0019. Make the enforcement guard itself

Status: Accepted
Date: 2026-08-13

## Context

A step-back review of the whole family found one pattern behind nearly every
real weakness: the system rigorously checks everything except itself. The
shared law is replicated by hand, the delivery gate and the upstream report
across the agent guides, the rulebook's core across the three styles, the
docs audit across the two Python styles, with no drift detection anywhere,
while derived projects pin the rulebook but not the audit script that
enforces it, and pin actions by mutable tag while pinning law by hash. The
review also proved the risk immediately: the three rulebook cores had
already drifted into three different drafts of the changelog clause, each
from a different amendment day. Two smaller gaps rode along, a
module-mocking ban verified once by hand and never standing in CI, and tree
diagrams in the architecture map that no check could see. And the Deferred
ledger held two entries the tree already answers.

## Options considered

- A cross-repository police workflow that checks the children from here. At
  five repositories the coupling costs more than the drift it prevents, and
  it inverts the ownership the family is built on.
- Leaving the shared blocks to discipline. Discipline already lost once; the
  changelog clause drifted three ways without anyone noticing.
- Leaving the mocking ban and the tree diagrams in review. Both are
  expressible as mechanical checks, and the family's own doctrine forbids
  reviewing what a machine can hold.
- Keeping actions on mutable tags. The rulebook is pinned by hash because a
  name can move; an action tag is a name that moves, and the same primitive
  applies one layer down.

## Decision

A family checker at the repository root, scripts/audit_family.py, holds the
shared blocks byte-identical across the styles: the delivery gate, the
upstream report, the rulebook's shared core, and the docs audit. Its
manifest doubles as the blueprint of what a new style must carry. Its first
run found the drifted changelog clause, which is now aligned on the newest
wording. The workflow pins every action by commit digest, adds secret
scanning over full history, and greps each style's suites for module
mocking. The docs audits gain three checks: duplicate decision-record
numbers, file names drawn in fenced tree diagrams that exist nowhere in the
repository, and dotted module claims in prose that name no real module,
with names declared in pyproject or in code exempt, a boundary the first
false positive taught. The agent guides now name the permanent gaps
themselves instead of pointing at STATE.md. The Deferred ledger is settled:
the routing boundary is stated in the architecture map where it belongs,
and the three type-check pins need no ledger entry because each carries its
reason inline and warn_unused_ignores reports them the day they go stale.
The STATE schema adds the closing clauses: re-verifying means re-deciding,
an entry re-affirmed unchanged across several horizons becomes a decision
record, and after a long absence the first task back is the sweep.

## Consequences

Drift in shared law is now a red build in the style repository, and the
manifest is the seed list for any fourth style. Derived projects receive the
audit-script pin, the seams grep, the pinned actions, and secret scanning
through the normal alignment wave. The enforcement layer still cannot guard
itself perfectly, a workflow cannot pin its own file, and that residual is
accepted and named rather than papered over.
