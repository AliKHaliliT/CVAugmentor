# 0016. Budget the bounded documents and check the census's findings

Status: Accepted
Date: 2026-08-10

## Context

The size budget kept losing. Projects built on this family drifted long, one architecture map reached twice the budget, and the agent guides in derived projects sat at three times the styles' size, all while the rulebook said roughly 150 lines for every living document. The budget was the last size rule held by review, and review is where it rotted.

The owner also asked for the general version of the question: a census of every rule the family states, sorted by whether a machine holds it, a machine could hold it, or only a reader ever can. One boundary was set for the third group, and it matters: review-only rules do not get emphatic prose bolted on, because agents read the guides literally, and urgency reads as noise that degrades the calm instructions around it.

## Options considered

- **One universal hard budget.** Rejected by the owner: a manual and a map must cover whatever exists, so gating them forces either dishonest brevity or ritual fission of documents whose job is completeness.
- **Warnings instead of failures.** Rejected: a warning is a failure someone has decided to ignore in advance.
- **Two classes, one bound, and the census's checkable findings implemented.** Accepted.

## Decision

`AGENTS.md` and `docs/ARCHITECTURE.md` grow with the system rather than against a number. The freedom is not license. They say everything as briefly as it can be said, and an agent guide that keeps growing usually means the project's boundary was drawn too wide, which is a scoping problem no budget fixes. Every other living document is bounded at 150 lines, the audit fails one that exceeds its bound, and fission stays the remedy. `README.md` stands outside both classes, governed by its schema.

The audit also gains the census's checkable findings: every document under `docs/` must be registered in the index, organic names stay UPPERCASE and records keep their `NNNN-kebab` shape, and `STATE.md` must hold exactly its four sections. For this template the audit further holds the Python layout conventions, a directory holds either subpackages or modules and an `__init__.py` is a door that only re-exports, ruff's PGH rules ban blanket suppressions, and a citizenship suite now pins what the library-citizenship rule claims: the NullHandler is present, importing the package reads no environment, and the version stays pinned.

The census's remainder stays with review on purpose, worded exactly as calmly as before: the translators clause, the prose tells, server-cache versus client-state placement, and the public-audience rule, each already labeled as carried by agent and human alike.

## Consequences

The bounded documents can now be at most one commit over budget before a build goes red, and the accretion habit meets a gate instead of a reviewer's patience. The free-growing pair is watched by judgment rather than a number, which is the honest shape of their job. The costs are a budget number that is now law rather than a suggestion, and an audit whose checks must be kept calibrated as the conventions they enforce evolve.
