# 0008. Word the rulebook so copies stay true

Status: Accepted
Date: 2026-08-04

## Context

Decision [0007](0007-own-the-rulebook-at-the-style-level-and-report-improvements-upstream.md) fixed the rulebook's ownership: a derived project carries a copy and never diverges from it. Preparing the first such copies surfaced a defect in the rulebook's own wording. It stated instance facts about this repository, such as the sentence presenting the changelog as unconditionally present because this package versions releases. In a derived project where the fact differs, a verbatim copy of that sentence is false, which forces exactly the divergence the ownership rule forbids. A frozen file that cannot be copied truthfully makes its own freeze unworkable.

## Options considered

- **Let derived projects patch instance sentences in their copies.** Rejected: it reopens the door 0009 closed, and "truth-preserving edit" becomes a judgment call made downstream, which is where drift starts.
- **Keep the rulebook as is and accept false sentences in some copies.** Rejected: a rulebook that is knowingly false somewhere teaches readers to discount it everywhere.
- **Reword the rulebook to state rules conditionally and leave instance facts to the living baseline.** Accepted.

## Decision

The rulebook states rules in instance-neutral form. The changelog row of the spine table and the changelog clause under "Where a why belongs" now express the condition (present only where consumers upgrade through releases) and point at BASELINE.md, whose trigger table is a living document and already carries the per-project fact. Whether any given project meets the condition is readable from that project's baseline and its file tree, never from the frozen rulebook.

The same change was made in the sibling templates' rulebooks, which carried the same defect in their own wording, so every rulebook in the family is now copyable verbatim.

## Consequences

A derived project's rulebook can be byte-identical to the template's and true at the same time, which is what makes the never-diverge rule enforceable rather than aspirational. The division of labor is now strict, since the frozen rulebook holds only rules and the living baseline holds the facts that vary per project. The cost is one indirection: a reader asking "does this project keep a changelog" consults the baseline trigger instead of finding the answer asserted in the rulebook.
