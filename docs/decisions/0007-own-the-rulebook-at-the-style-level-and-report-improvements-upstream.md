# 0007. Own the rulebook at the style level and report improvements upstream

Status: Accepted
Date: 2026-08-04

## Context

The template exists to be applied. Projects are built from it or refactored against it, usually by an agent that is not the style's owner, and the first family of projects refactored against the family's templates exposed two gaps in how the system handles that situation.

First, a refactor can genuinely out-think the template. When it does, nothing said where the improvement belonged, so it stayed in the refactored project and the template silently stopped being the best statement of its own form. Second, the rulebook froze itself with "do not modify this file" and located the authority to change it in "the repository owner", which a derived project holding a copied rulebook can read as its own owner. That ambiguity is enough for copies to drift apart while every copy believes it is following the rule.

## Options considered

- **Rely on discipline and keep the wording.** Rejected: the drift already happened once under this wording, and a rule that failed silently will fail silently again.
- **Let derived projects adapt their rulebooks.** Rejected: the family's premise is that each form has one best current statement, and per-child rulebooks turn every future alignment into a negotiation over whose adaptation wins.
- **Anchor ownership in the style and give improvements a formal path upstream.** Accepted.

## Decision

Two changes, made together because each covers the other's failure mode.

The rulebook's preamble now states that a rule changes only inside the template itself, in the My-Styles repository and by its owner, and that a derived project never edits or diverges from its copy. A child that believes a rule is wrong or missing does not get to be right locally; the case travels upstream. This record is the superseding decision the preamble requires for its own change.

AGENTS.md gains the upstream report, the vehicle for that travel. At the end of a refactor against this template, and only after the template has been properly implemented, improvements the template should have had are qualified against the decision records (an idea already considered and rejected earns no entry, and an empty report is not written at all), written up one self-contained entry at a time, applied to the template first, and followed by a manual alignment check on the refactored project so it ends up carrying the upstream form of each improvement. Each entry records how the improvement was found, why it is believed better, and that the logs hold no prior ruling on it, and each ends by instructing the receiver to verify the claim with research before adopting it. The report opens by explaining its own existence, because its reader may be the owner, who applies it to the style directly, or a stranger to the project, who files it as an issue on the open-source template.

## Consequences

Improvements now have exactly one destination, so the template converges toward the best known statement of its form instead of being overtaken by its own children. The qualification step keeps the mechanism honest, since a report cannot be generated out of obligation when nothing real was found.

The costs are deliberate. The refactoring agent must read the decision log before claiming novelty, the owner must ground every claim in research before adopting it, and the final alignment check adds a second visit to the refactored project.
