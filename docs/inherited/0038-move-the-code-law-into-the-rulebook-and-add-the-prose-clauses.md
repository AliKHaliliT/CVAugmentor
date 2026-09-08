# 0038. Move the code law into the rulebook and add the prose clauses

Status: Accepted
Date: 2026-09-03

## Context

The code-level convention lived canonically in the README, a human-facing
document, and the agent guide pointed there for it, so the family's code
law sat in the document an agent is least likely to read as binding. The
adopting agent missed it. Beyond that, the review of the doctoral
repository surfaced rules with no clause for a case they met: prose
inherited on adoption day, dated documents that are neither spine nor
decision, invariants with no observable output, and reports to a person
that an expert outside the work could not follow.

## Decision

The docstring convention moves into the rulebook's code-level section,
verbatim, and the README keeps one paragraph pointing at the rulebook and
one on ownership; the README carries no law of its own, and the README
schema says so. The Prose section gains two paragraphs. Inherited prose
comes under the law at adoption, tracked in STATE as debt until paid, with
a named exclusion for paths another guard hashes. A report to a person
opens with a plain account a reader outside the work can follow and pairs
every abstract finding with one concrete instance. The species section
states that any dated document under docs/ is a record for the purpose of
immutability, whatever it is called. The test rule states that an
invariant with no observable output is observed through a counting fake at
the seam it crosses, and that where no seam exists the invariant is asking
for one.

## Options considered

- Letting inherited prose converge when next edited was refused, because
  it is the lenient path that leaves a half-folded repository half folded.
- An output schema for reports was refused again; the plain-account rule
  is an order of presentation, not a form.

## Consequences

One home for law and one for welcome. An adopting agent finds the
docstring convention where the rulebook is, meets the inherited corpus
with a written rule, and knows what to do with a briefing or a progress
report.
