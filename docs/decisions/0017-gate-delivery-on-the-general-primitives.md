# 0017. Gate delivery on the general primitives

Status: Accepted
Date: 2026-08-13

## Context

Treasury study 0001 in the My-Styles repository reduced 14,765 named software
engineering concepts to 125 primitive operations, each carrying a price. A
subset of them is general: applicable to any project this family builds, in
any language, without opposing one another, because the family's earlier
rulings already settled their internal conflicts. The checkable members of
that subset were law here before the study named them, carried by the
toolchain: import contracts, the layout and documentation audits, the type
checker, the linters, the prose grep, and the pinned rulebook. The members
that need judgment were scattered: some lived as hard rules, others only as
habits of review. Nothing defined when a task counts as delivered, so closing
quality depended on whoever was closing, and fixes arrived as expensive
after-the-fact repairs rather than as properties carried while writing.

## Options considered

- Machine checks for everything. The judgment items are not expressible as
  tree or text invariants, and pretending otherwise produces checks that
  measure proxies, which the family's coverage-threshold ruling already
  rejects.
- The gate inside docs/CONVENTIONS.md. That rulebook is scoped to
  documentation and budget-bound at 150 lines; delivery discipline is
  operating-manual law, and AGENTS.md is the operating manual.
- Free review with no fixed list. Unbounded scrutiny drifts into taste,
  invites endless polishing loops, and cannot be handed to an agent calmly.
- A gate of rules without primitive names. Considered seriously, since a name
  invites a reader to substitute their prior for the stated rule. Rejected
  because the names index a shared literature that helps when a rule meets an
  unforeseen case, and the bias risk is closed by making the rule normative:
  the gate states that where a name's common usage and the rule differ, the
  rule governs.

## Decision

AGENTS.md gains a delivery gate: sixteen named items, each a one-line rule,
weighed against every change before it may be called delivered. Fifteen carry
the general primitives. The sixteenth points rather than copies. It sweeps
the review-held clauses of the guide's own Hard rules at every close, so
style law receives the same end-of-change reflection without a second copy
that could drift. The items are carried from the first line written rather
than retrofitted at the end. The
closing loop is bounded: findings must trace to a listed item, the list is
closed, one clean pass ends it, and a finding that survives three honest fix
attempts is recorded in STATE.md and surfaced at delivery instead of looped
on further.

## Consequences

"Delivered" now has a definition that travels with the repository and binds
agents and humans alike. Writing with the gate in mind front-loads quality,
which costs less than repair passes. The bounded loop prevents both
under-checking and endless polishing. Derived projects adopt the gate through
the normal alignment wave. The primitives outside the general subset remain
project options in the treasury, weighed at design time, never at the gate.
