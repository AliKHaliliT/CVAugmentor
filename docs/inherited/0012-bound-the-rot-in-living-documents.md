# 0012. Bound the rot in living documents

Status: Accepted
Date: 2026-08-10

## Context

Two entries in this family's living documents were found asserting things that had stopped being true: a deferral claiming an app lacked an icon it had carried for weeks, and an instruction to enable a deployment that had been live for days. Both were written correctly and rotted silently, because reality moved through paths that never touched the files.

The owner has watched this failure survive every documentation architecture they have tried, and named the mechanism precisely. Documents rot when the writer's context is gone, whether the session ended, the context window overflowed, or the task moved on. A rule that says "update the document when things change" binds the writer at write time, and it fails exactly when memory fails. The species split already protected the records, which are immutable and cannot rot; every observed failure sat in a living document, and every one was the same sentence type, a claim whose truth lives in the tree or the world rather than in the document.

## Options considered

- **More discipline.** Rejected: it is the thing that already failed, here and in every earlier system the owner built, because it depends on remembering.
- **A full freshness apparatus**, front-matter metadata, per-document owners, review scoring, as some documentation platforms run. Rejected: heavier than a template family needs, and most of its weight serves organizational routing this family does not have.
- **Three bounded rules plus a mechanical audit.** Accepted, because the family already dates every STATE entry, so the expiry mechanism was one meaning-change away.

## Decision

Three rules join the living-documents section of the rulebook. A STATE entry's date becomes its last-verified stamp rather than its birthday, an entry older than 90 days is expired and may not be relied on until re-verified, and the docs audit fails on expiry so the sweep cannot be forgotten. Living documents record intent and decisions, never inventory the tree can answer, because a premise the tree can contradict rots silently while a wish only rots when it dies. And a sentence in a living document is a claim to verify before relying on it, with every change ending in a sweep of STATE for entries the change completed or invalidated, binding agents and humans alike.

The mechanical half is checked rather than reviewed. `scripts/audit_docs.py` verifies that every repository path a living document names exists, that every relative link resolves, and that no STATE entry has outlived the horizon; CI runs it as the Docs step before anything installs. Decision records are exempt from all of it, since they describe the past.

The audit proved itself during its own calibration by catching a path claim in this family that had already rotted, a testing note referencing a folder that does not exist.

## Consequences

Staleness stops being unbounded. A claim in a living document is now either machine-checked, or expiry-dated with a 90-day ceiling on how long it can be wrong, or written as intent that only rots when the wish dies. The cost is that a push after a quiet quarter can go red purely because time passed, which is the forcing function working as designed, and that the audit's path heuristics may need tuning when documents legitimately name things that look like paths.
