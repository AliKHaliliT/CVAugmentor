# 0006. Write tracked content for a public audience

Status: Accepted
Date: 2026-08-01

## Context

The documentation system works by compelling faithful recording. STATE.md must say what is deferred and why, decision records carry the real rationale, and commit bodies carry the why. Applied to a real deployment of the style, that discipline turned into a leak vector, because a faithful agent recording what was withheld and why writes the sensitive fact into a tracked file in the same stroke. Two properties of git make such a leak unfixable after the fact. Repository visibility is not stable, since a private repository is public after one settings change, and history is permanent, since content removed from tracking still lives in every clone of the history. The style had no rule saying where faithfulness must stop.

## Options considered

- **A writing rule alone.** Rejected: when an agent hits sensitive context it still needs somewhere to put it, and a rule with no outlet bends under the system's own pressure to record everything.
- **A session-local scratch file, deleted when the session ends.** Rejected: the context dies with the session, so a later session either re-asks the owner or re-derives the sensitive fact and leaks it fresh.
- **A persistent untracked companion file plus the writing rule.** Accepted: the rule stops the leak and the file preserves the context on the machine, outside the repository and its history.

## Decision

Every tracked byte and every commit message is written for a public audience, regardless of the repository's current visibility. Confidential facts, private repository names, deployment details, and the description of withheld content never enter tracked files. Their home is `LOCAL.md` at the repository root, never tracked, created the first time something sensitive needs recording. A tracked entry carries the public-safe version and may reference the local ledger with a neutral pointer. A record whose true rationale is confidential gets a public-safe Context, with the full context kept locally. Images are reviewed like prose before being embedded, since a tracked screenshot is as permanent as tracked text. An agent unsure whether a fact is sensitive surfaces the question instead of recording it.

## Consequences

Sensitive context survives on the owner's machine but does not travel with the repository, so a contributor cloning elsewhere will not see `LOCAL.md`, which is both the point and the price. The living documents stay truthful but lose specificity wherever the specifics are sensitive, carrying the public-safe version of an entry while the local ledger carries the real one. Derived projects inherit the rule through AGENTS.md, BASELINE.md, and the ignore file like the rest of the baseline.
