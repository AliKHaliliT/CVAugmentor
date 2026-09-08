# 0003. Adopt the repository baseline

Status: Accepted
Date: 2026-07-16

## Context

The always-present files had accumulated by inheritance rather than by decision. The stock Python `.gitignore` deliberately un-ignored `.vscode/settings.json`, so personal, machine-specific editor settings (a conda environment-manager preference) were tracked and shipped to everyone cloning the template. No `.gitattributes` existed, so line endings depended on each contributor's local `core.autocrlf`, leaving repository bytes at the mercy of per-machine settings. There was no `.editorconfig`, and no rule stating which of these files must exist or how they may change.

## Options considered

- **Track curated editor configuration** (a team-convention `settings.json` and `extensions.json`). Rejected: the template is editor-neutral by philosophy, the settings actually tracked were personal rather than universal, and everything worth enforcing already lives vendor-neutrally in tool configuration; this is the assistant-shim decision applied to editors.
- **Leave line endings to each contributor's git configuration.** Rejected: repository bytes must not depend on per-machine settings, and the failure class (a CRLF shebang inside a Linux container) is silent until deployment.
- **A committed baseline: `.gitattributes` and `.editorconfig` as repository policy, editor directories untracked, the whole set specified in a living `docs/BASELINE.md`.** Accepted.

## Decision

Adopt the repository baseline specified in [BASELINE.md](../BASELINE.md): an always-present set (`README.md`, `LICENCE`, `.gitignore`, `.gitattributes`, `.editorconfig`, plus the documentation spine), a conditional set with explicit triggers (`.env.example`, `.dockerignore`, `CHANGELOG.md`, dependency manifests), a never-tracked set (editor directories, secrets, regenerable artifacts, OS junk), and a per-file modification rule for each. `.vscode/` is untracked and ignored. The inherited stock ignore file is replaced by a curated set of labeled sections matching the template's actual stack, so every rule present is a decision rather than an inheritance.

## Consequences

Clones behave identically regardless of the contributor's editor, operating system, or git configuration, and no personal settings ship with the template. The cost is that shared editor behavior can no longer ride along in `.vscode/`, so anything worth standardizing must be expressed through `.editorconfig` or tool configuration, a stricter but more honest channel.
