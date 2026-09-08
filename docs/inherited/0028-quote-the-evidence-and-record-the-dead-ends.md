# 0028. Quote the evidence and record the dead ends

Status: Accepted
Date: 2026-08-25

## Context

Designing a future research-oriented style surfaced two needs, and both
turned out to belong to engineering as much as to research. The first is a
home for measurement. Some decisions rest on something that was run, and the
existing records were folding those results into Context or Consequences as
loose prose, findable only by rereading. The second is the fate of a failed
attempt. An approach that is tried, fails, and is reverted leaves no bytes in
the tree, and the family records a ruling where its bytes land, so the revert
is lawfully silent. Nothing then stops the same approach from being
re-implemented a month later by someone who never learns it already died.

The choice was between keeping the record schema as it stands and letting a
research style carry its own variant, or growing the one schema so every
style shares it. A second schema would split the record species in two and
make every future reader learn which variant they are holding. The docstring
convention already solves the same problem the other way, with one vocabulary
of sections used where they fit and omitted where they are not called for.

## Decision

The record template gains an optional Evidence section between Context and
Options considered. It appears only where the decision rests on something
measured or run, and a record resting on reasoning alone omits it. The
results a decision rested on are quoted in the record in full, never pointed
at, because a record must stay accurate after the tree it measured moves on.

Dead ends become a named trigger for records, and the trigger is evidence
arriving rather than work completing. Where a reverted attempt cost real
effort or could plausibly be retried, its record names the evidence that
killed it, the condition that would reopen it, and the commit that held the
attempt, which after the revert is the only surviving proof the attempt
existed. Ordinary iteration earns no record; the test is whether someone
might plausibly walk back in a month later.

## Consequences

The rulebook's shared core carries both rules, so they hold identically
across the family. No check changes, because both rules are judgment tier;
whether evidence warranted a section and whether an attempt deserved a
tombstone are review's questions.

Records may grow larger where evidence is quoted, and that is legal by
existing law, since records are exempt from the line budget because they
describe a past that does not rot.

A future research-oriented style inherits this schema unchanged and shrinks
accordingly. What remains genuinely its own is pinning claims to artifact
state, references as first-class records, and its own gate, none of which
this ruling creates.
