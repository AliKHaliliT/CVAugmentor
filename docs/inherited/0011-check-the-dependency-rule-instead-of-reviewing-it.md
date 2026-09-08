# 0011. Check the Dependency Rule instead of reviewing it

Status: Accepted
Date: 2026-08-08

## Context

The first hard rule of this template says the Dependency Rule is absolute, with `domain` and `services` never importing from `facade`, `adapters`, or any SDK. Nothing enforced it. The runner importing a concrete adapter instead of receiving it through its port, or a schema reaching for the Anthropic SDK, passes ruff, passes strict mypy, passes the suite, and goes green in CI, because none of those tools is asking who may import whom. For this package the stakes are the architecture itself, since the ports are the design, and a core that imports its adapters is a different design wearing the same folder names.

The client style closed the same class of gap in its [decision 0008](https://github.com/AliKHaliliT/My-Styles/blob/main/Helm/docs/decisions/0008-check-the-layer-rule-instead-of-reviewing-it.md), moving the layer rule from review into ESLint, and the server template has now done the same for its Dependency Rule. This template was the last of the three holding its central rule by memory.

## Options considered

- **Leave it to review.** Rejected: the discipline is only as strong as the reviewer's attention, and importing the concrete adapter is precisely the shortcut that looks harmless in a diff.
- **Express the boundaries in ruff.** Rejected: ruff's banned-import rules apply to the whole project at once and cannot say that `services` may not import `adapters` while `facade` may, so the shape this rule needs is the one ruff cannot express.
- **Write a custom checker.** Rejected: a hand-rolled AST walker is a second implementation of a solved problem, and it would itself be the least-reviewed code in the repository.
- **Adopt import-linter.** Accepted. It is purpose-built for exactly this, it reads its contracts from the `pyproject.toml` a package already owns, and it joins the existing dev dependency group.

## Decision

Two contracts in `pyproject.toml` state the rule the agent guide has always claimed. "The core stays inside the ports" forbids `keel.domain` and `keel.services` from importing `keel.facade`, `keel.adapters`, and `anthropic`. "The Dependency Rule points one way" is a layers contract over `keel.facade`, `keel.services`, and `keel.domain`.

The layer directories are bare namespace packages by the folder-purity convention, so they are listed as root portions rather than through a single `keel` root, which the tool would scan past because they carry no `__init__.py`. Locating those portions imports the package root once, and the library-citizenship rule is what makes that safe, since this package promises no import-time side effects; everything past that point is parsed rather than executed.

The Lint verb becomes `ruff check . && lint-imports`, keeping the five commands at five, and CI runs the documented command.

The forbidden contract was proven live before this record was written. A planted import of the tool registry adapter inside the runner broke it, with the chain named, and reverting the plant took the run green again. The upward direction announces itself differently here, and the difference is worth naming. Because the facade already imports the services and the services already import the domain, an upward import completes a real cycle, so the command fails with Python's own circular-import error naming the modules rather than with a contract report. Either way the Lint verb goes red, and the contract report covers the violations that do not cycle, which are exactly the quiet ones.

## Consequences

The rule that defines this package's architecture is now checked on every push, and the family no longer has a style whose central absolute is held by memory alone.

The costs are one development dependency and a Lint verb that runs two tools. The check is also only as complete as its forbidden list, so a new SDK adopted by an adapter belongs in the contract in the same change that adds it to the extras. The portion list in the linter's configuration mirrors the layer directories, so a new top-level layer joins that list when it joins the tree.
