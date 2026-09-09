# 0045. Retire the generated documentation site

Status: Superseded by [0058](0058-publish-the-api-reference-from-main-with-pdoc.md)
Date: 2026-09-05

## Context

Version 1.x published a Sphinx site to GitHub Pages. The arrangement had three
moving parts: a `gh-pages` branch holding both a copy of the source and the
generated HTML, a workflow that on every push to `main` checked out that branch,
merged `main` into it with `-X theirs`, rebuilt the site, and committed the
result, and a `conf.py` plus a generator script that existed only on that branch
and nowhere a reader of `main` would find them.

The branch held 213 files, of which the ones not also on `main` were entirely
build output: `.doctree` pickles, `_sources` copies, and rendered HTML. Its
history shows the failure mode the design invites, five commits in a row named
for debugging the workflow itself.

The content of that site was the docstrings, which live in the source and are
read there by anyone with an editor.

## Options considered

- **Keep the arrangement.** A second branch that has to be kept merged with the
  first, whose build breaks on a schedule set by other people's tooling, in
  exchange for rendering text that is already readable at its source.
- **Move the site build to `main` and publish from an artifact.** Removes the
  branch merge, keeps Sphinx, its configuration, its theme, and a build step in
  the gate that fails for reasons unrelated to the package.
- **Keep the site and stop generating it from `main`.** A site that goes stale
  the first time a docstring changes, which is worse than not having one.
- **Retire it, and keep written documentation in the repository.** The style
  already prescribes what technical documentation exists and where, so the
  package gains `docs/` and loses the site.

## Decision

The Sphinx site and the `gh-pages` branch are retired. Documentation is the
docstrings, read at their source, plus the documents the rulebook prescribes,
which live under `docs/` on `main`. The repository is a single branch.

## Consequences

The auto-doc workflow is gone, and with it the two TODO entries that asked for
it to run on pull requests and for its quoting to be cleaned up. Both were
requests to improve a thing that no longer exists, which is the cheapest way to
satisfy them.

The published site at the old address stops resolving. GitHub Pages keeps its
own setting naming the deleted branch as a source, and that setting has to be
turned off in the repository's settings by hand, which no command in this tree
can reach; STATE.md carries it as blocked until it is done.

Anyone who wants rendered API documentation can still run Sphinx over the
package, since NumPy-style docstrings are what its autodoc reads. What the
project no longer does is maintain that build as part of its own gate.
