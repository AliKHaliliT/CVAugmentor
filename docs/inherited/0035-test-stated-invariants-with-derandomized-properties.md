# 0035. Test stated invariants with derandomized properties

Status: Accepted
Date: 2026-09-01

## Context

The suites assert on hand-picked examples, which document intent but state
an invariant only as far as the examples reach. Parts of this style's
surface carry invariants stronger than any example list, above all the
translators, whose whole contract is that nothing is lost or invented
crossing the boundary. Property-based testing states such an invariant
over generated inputs and shrinks any counterexample to its smallest
form. The owner weighed adoption and ruled for it, narrowly.

## Decision

Property tests are a demonstrated test shape, not a mandate. They join
the ordinary suites at the mirrored paths, under the same Test verb, with
no gate item, no new command, and no change to the placement and
substitution rules, because breadth was already a judgment call and this
is breadth. The worked examples are the outbound facade translators here
and the rounding strategies in the demo arrow cut from this style.

Every property in the gate runs derandomized with no example database, so
a pinned tree reproduces the same result on every run; free-roaming
randomness stays a local exploration tool and never enters CI or
evidence. Hypothesis carries the dev dependency, and its cache directory
joins the ignore file.

A green property test claims that no counterexample exists in the cases
its settings generate, never that the property is proved. That boundary
is stated where the suites declare their settings, per the family's rule
that a check may never imply more than it decides.

## Options considered

- Blanket adoption across every suite was refused. Most of the surface
  has no articulable property, and a property test restating its own
  implementation is a slower example test.
- Unpinned randomness in CI was refused, because a gate that can fail on
  a seed nobody chose reports weather, not regressions, and a claim
  pinned to a tree must reproduce from that tree alone.

## Consequences

The translator and strategy invariants are now defended over generated
input rather than spot-checked. Example suites stay, since they document
intent the properties do not. An instance whose domain carries a real
invariant has exemplar bytes to cut from; one whose domain does not
carries no obligation.
