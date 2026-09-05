# 0001. Adopt the documentation system

Status: Accepted
Date: 2026-07-16

## Context

Technical documentation in earlier projects accumulated ad hoc and degraded in two recurring ways. Append-only files (most notably a history file recording every change together with its reason) grew without bound until they were closer to log files than documents: too large for a human to skim and too large for an AI agent to load usefully. Documents that should have stayed current, such as architecture overviews, were instead amended incrementally and accumulated stale narration beside fresh fact. On top of that, agent instructions lived in a vendor-specific file (`CLAUDE.md`), tying the project to one assistant, and there was no contract making documents discoverable: a document a reader did not already know about might as well not have existed.

## Options considered

- **A single chronological history file.** Rejected: it duplicates what git already records, and re-narrating chronology at file scale always degenerates into a worse git log; its growth is unbounded by construction.
- **A fully fixed documentation set** (every project has exactly these files and no others). Rejected: a CLI tool, a server, and a library do not need identical documents, so a fixed set is always either bloated or insufficient.
- **Fully organic documentation** (each project grows whatever documents it wants, however it wants). Rejected: without a fixed entry point and a mandatory index, documents are undiscoverable to agents and future readers.
- **A hybrid: a small fixed spine plus an indexed organic zone, with every document split into one of two species (living documents and records).** Accepted.

## Decision

Adopt the documentation system specified in [CONVENTIONS.md](../CONVENTIONS.md): a vendor-neutral `AGENTS.md` as the agent entry point and the single documentation index, `STATE.md` for the living project state, `docs/ARCHITECTURE.md` as the living map of the system, immutable decision records under `docs/decisions/` as the durable home of rationale, and `CHANGELOG.md` as the curated per-release summary for consumers of the package, with per-species writing rules (living documents are rewritten in place and size-budgeted; records are dated and never edited). The history file is retired: a small "why" goes into the commit message body, a decision-shaping "why" becomes a decision record, and an upgrade-facing "what changed" goes into the changelog.

## Consequences

No document has a reason to grow without bound. Living documents are size-budgeted and split when they outgrow the budget, and the record set grows by adding small files rather than by growing one. Rationale survives in a form both humans and agents can load selectively, and the entry point works across assistants instead of being tied to one vendor. The cost is discipline: the index must be maintained with every documentation change, the species rules must be respected, and superseding a decision means writing a new record rather than editing the old one.
