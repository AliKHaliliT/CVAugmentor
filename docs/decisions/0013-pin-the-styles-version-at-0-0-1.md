# 0013. Pin the style's version at 0.0.1

Status: Accepted
Date: 2026-08-10

## Context

A style is not a product. Nobody upgrades through releases of a template; a derived project copies the shape once and versions itself. Yet the family's version fields told product stories. This package declared 1.0.0 with a Production/Stable classifier, and its changelog had accumulated an Unreleased section containing a removed public export, which forced a semver question, 2.0.0 or not, that had no meaningful answer for a template.

The owner ruled that everything in the family that never releases reads 0.0.1, one rule with no exceptions, so a version field can never again imply a release process that does not exist.

## Options considered

- **Cut releases properly.** Rejected: it would manufacture a release process purely to justify a number, and the changelog work that follows would document upgrades nobody performs.
- **Leave the numbers as decoration.** Rejected: a decoration that looks exactly like a promise is how this was found, since the pending question "what version comes next" only existed because 1.0.0 claimed there would be a next.
- **Pin 0.0.1 everywhere and delete what the pin obsoletes.** Accepted.

## Decision

The package version becomes 0.0.1 and stays there. The Development Status classifier goes, since maturity classifiers describe products. And `CHANGELOG.md` is deleted, because the baseline's trigger, a versioned package that consumers upgrade through, is now permanently unmet, and the baseline's own rule is that a conditional file whose trigger is gone is clutter. Its pending Unreleased entries dissolve into the commit history that already carries them.

## Consequences

The style never cuts a release, so upgrade-facing summaries have no home and impact lives in commit subjects, which the rulebook already provides for. A derived project starts its own versioning from whatever number it likes, and the attribution line in its README carries the provenance. The number 0.0.1 now means "this is a style" everywhere in the family.
