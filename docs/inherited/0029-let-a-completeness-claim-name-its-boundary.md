# 0029. Let a completeness claim name its boundary

Status: Accepted
Date: 2026-08-27

## Context

Treasury study 0004 tested sixty-seven claims that a region had been searched
exhaustively, and thirty-four were false. The failures sorted perfectly by one
criterion. A claim to have finished a list someone else published and numbered
verified true again and again, down to obscure tails, because the boundary
exists outside the claimant and anyone can re-derive it. A claim to have
finished a region the claimant delimited itself failed every time it was tested,
sometimes by twenty items, because no external boundary exists that the claimant
could have reached, so the claim reports only that the claimant stopped finding
things. Used prospectively, the rule predicted which claims would hold and which
would not, without an exception.

The engineering version of that claim is made constantly. Every caller was
updated, every usage was fixed, all the edge cases were handled. The first two
can be honest, because a grep, a file list, or a suite run is an enumerable
boundary a reviewer can re-derive. The third is a self-drawn region.

Existing law came close and did not cover it. The checking rule governs what a
CHECK may claim, and the state file's rule says its entries are claims to
verify. Nothing governed what a worker's own completeness claim must carry, so
review had no way to tell a checkable claim from an unfounded one that uses the
same words.

## Decision

A completeness claim names its boundary.

Saying that every caller was updated or every usage fixed is a fact only when
it names the enumerable list it exhausted, a grep, a file list, a suite run,
that a reader can re-derive. A claim over a region the claimant drew itself,
such as every edge case considered, is offered as judgment rather than fact.
Review probes the second kind, and trusts the first only as far as its boundary
reaches.

The rule is judgment tier. No check changes, because no tool can decide whether
a boundary was the right one, only whether one was named, and gating on the
word "all" would breed evasive phrasing rather than named boundaries.

## Consequences

The agent guide carries the rule in one bullet, identical across the family,
beside the checking rule it extends. The two rules together cover both
directions of the same lie: a check may not imply more than it decides, and a
worker may not claim more than a boundary supports.

What changes in practice is small and cheap. A worker writing "updated all
call sites" writes what enumerated them, which usually costs half a line, and a
reviewer reading a completeness claim without a boundary reads it as the
judgment it always was. Nothing changes for claims that never pretended to be
exhaustive.

The rule deliberately does not require a boundary for every claim, only for
claims OF COMPLETENESS. Ordinary statements of what was done are already
governed by review and by the state file's claims-to-verify rule.
