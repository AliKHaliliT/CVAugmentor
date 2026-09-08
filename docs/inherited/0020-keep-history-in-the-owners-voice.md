# 0020. Keep history in the owner's voice

Status: Accepted
Date: 2026-08-14

## Context

The owner has twice ruled that git history carries no AI attribution: once in
June 2026 in another repository, and again in August when a default
Co-Authored-By trailer reached a commit here and was amended out before push.
The rule lived only in one assistant's private memory, so any other agent, or
the same assistant on another machine, would re-offend with the tooling's
default behavior. A cross-project sweep surfaced the gap.

## Options considered

- Leave it in assistant memory. Memory is per-assistant and per-machine; the
  rule failed exactly this way once already.
- Check it in continuous integration by grepping pushed commit messages.
  History is immutable once pushed, so a single violation would fail forever
  or demand rewriting public history, and the existing law already keeps
  commit-message rules with review for the same reason.

## Decision

A hard rule in AGENTS.md: commit history speaks in the owner's voice alone,
no attribution trailers, no Co-Authored-By lines, nothing naming a tool or an
assistant in a commit message. Held in review, where the delivery gate's
hard-rules sweep reads it at every close.

## Consequences

The rule now travels with the repository and binds every agent and human who
reads the guide, not just the one who was corrected. Derived projects adopt
it through the normal alignment wave. History in this family stays authored
by its owner.
