# Upstream

Aligned to Keel at e069bab89f8155dc8998427b2535959c74598d76.

Every entry below is a lead, not a verdict; verify it against the template's own tree before adopting it.

## Open

### 2026-09-09 The baseline names only a checks workflow

Kind: defect
Pin: e069bab89f8155dc8998427b2535959c74598d76

**What it is.** The baseline's row for `.github/workflows/` is triggered by the
project running its checks on a hosted runner, and it names `ci.yml` as the file
that runs the commands the guide documents. It describes no other workflow, so a
project that also publishes something from a runner has no row to sit under.

**How the work surfaced it.** This project publishes its API reference from the
default branch into an upload artifact, which is a deployment rather than a
check and therefore deliberately not part of `ci.yml`, since its failure must
not block a merge. That put a second workflow file in the directory. Nothing in
the tree objected, the audits pass, and the file is outside what the baseline
describes rather than against it, which is the kind of silence worth reporting
before every child resolves it differently.

**What was worked around.** Nothing was patched or suppressed. The second file
was added and the baseline was left as the style owns it, so this is a report
rather than a local divergence. A sentence in that row naming a publishing
workflow, or saying the directory holds the checks workflow and whatever else
the project publishes with, would settle it.

**Records checked.** The inherited records were read for a prior ruling. 0003
adopts the baseline and reasons about always-present and trigger-conditional
files without distinguishing a check from a deployment. 0010 fixes the five
commands and requires them to run on push and on pull request, which is about
`ci.yml`'s contents rather than about what else may sit beside it. 0045 and 0058
concern this project's own publishing rather than the style's law. No record
addresses the case.

### 2026-09-09 The ignore rules miss the import contract's second cache

Kind: defect
Pin: e069bab89f8155dc8998427b2535959c74598d76

**What it is.** The Lint command's import-contract step leaves two cache
directories behind, not one. The template's `.gitignore` ignores
`.import_linter_cache/` and nothing ignores `.grimp_cache/`, so every child
that runs that command accumulates an unignored directory in its working tree.

**How the work surfaced it.** Building a source distribution before a first
release listed `.grimp_cache/bc6e9915910c9939a794955295f16cbc5eb7e699.data.json`
among its files. A regenerable cache had been swept into an artifact about to be
published, which sent the search back to the ignore rules. Both names are
confirmed from the tools' own sources rather than inferred, on import-linter
2.15: `importlinter/cli.py` and `importlinter/configuration.py` carry the
literal `.import_linter_cache`, and `grimp/caching.py` carries `.grimp_cache`.
Both directories exist in this working tree.

**What was worked around.** `.grimp_cache/` was added beside the existing rule.
The baseline requires every ignore rule to correspond to the actual stack, so
this is compliance rather than divergence, and the template needs the same line
because the same command leaves the same directory in every child.

Worth stating for the reader of this entry: the first draft of it claimed the
template's existing rule named a directory nothing creates and should be
replaced. That was wrong. Rebuilding the distribution after the change put
`.import_linter_cache/` into it instead, which is how the mistake was caught
before it was sent.

**Records checked.** 0003 adopts the baseline and gives the curation rule this
correction follows. No inherited record addresses any particular tool's cache
directory. No record refuses it.