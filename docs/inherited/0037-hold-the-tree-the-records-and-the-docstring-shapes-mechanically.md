# 0037. Hold the tree, the records, and the docstring shapes mechanically

Status: Accepted
Date: 2026-09-03

## Context

The adopting repository's audit passed while its docs zone held foreign
subfolders, because the audit walked only the top level of docs/ and the
records folder. The same class of gap appeared wherever a rule had no
checker behind it. The map was verified in one direction only, every drawn
name existing, never every existing directory drawn, so a stray folder had
no room and nobody noticed. The layout audit could decide nothing over a
tree of loose modules and still print agreement. The rulebook promised
record immutability and no check held it. The docstring convention was
review-held past presence, so an agent satisfied presence and stopped. The
STATE horizon treated an in-flight entry like a deferred one.

## Decision

The docs audit walks the whole docs zone, so a file below a subdirectory is
registered by its path or its folder's row or it fails, and a non-markdown
file there fails outright. It holds the map in the completeness direction:
every tracked directory at the root and one level below the code root, and
every root file, has a room in the map's tree or the baseline's tables. It
reports the roots it held the layout over and fails when the tree's shape
leaves it nothing to hold. It verifies that the import graph the Dependency
Rule contract runs over covers every module on disk, so a contract cannot
report kept over a partial graph. It holds records immutable beyond their
Status line, in the working tree and in every commit since the check
arrived, finding that commit in git's own history so an adopting project
is bound from adoption forward; a shallow clone fails rather than checking
less, and CI fetches full history. It holds the decidable half of the
docstring convention, the trio traveling together and parameter names
matching the signature, and leaves truth and the Usage block to review. An
in-flight STATE entry expires after thirty days rather than ninety.

## Consequences

A foreign folder, an undrawn directory, a rewritten record, or a docstring
naming the wrong parameter fails the gate instead of waiting for a reader.
The audit says what it examined, so a run that decided nothing looks
different from one that found nothing. Installation precedes the docs audit
in CI, since the graph check imports the package.
