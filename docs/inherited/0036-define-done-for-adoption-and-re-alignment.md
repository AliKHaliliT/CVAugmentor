# 0036. Define done for adoption and re alignment

Status: Accepted
Date: 2026-09-03

## Context

A repository adopting this style against a large, disordered codebase came
back half folded. Its docs zone held the spine beside foreign folders, its
code kept the docstrings it arrived with, and the agent could not say when
the alignment was complete, because nothing in the style said how an
existing repository gets to the end state or what done means. The same
agent left work untouched rather than decide about it, reading the
baseline's caution about deleting one uncertain file as a reason to ask
before touching anything. The owner asked for a definition of done that a
weaker model cannot slide past and a stronger model does not pay for.

## Decision

The agent guide gains an Adopting section, one text across the family. It
grants the adopting agent authority to fold, move, rewrite, and delete on
its own, because git is the archive, and moves the owner's review of
removals to one reading of an inventory that classifies every tracked path.
It names the demo as the authority on dialect and never on scope, and the
map gains an Exemplars section naming the file an artifact of each kind is
cut from. It states the gate that means done in two parts, a closed list of
conditions a check decides and a named residue that stays review's, so a
passing gate is never read as the whole. It defines re-alignment as the
same refactor in miniature, driven by the decision records the template
gained since the child's pin, which the README attribution now records,
with the files the style carries verbatim recopied and the adapted ones
re-adapted from a diff. No changelog is kept, since the records are the
changelog and a summary would be a lossy copy. The upstream-report section
gains the shape of the maintainer's reply, a re-alignment order rather
than a verdict to interpret.

## Options considered

- A changelog, a version, or a last-edited date for re-alignment were
  refused. A changelog is a summary an agent over-trusts, a date in a
  living document breaks the species rules, and the style's version is
  pinned by an earlier ruling; the records already carry every change.
- Softening the law for weaker models was refused. Every addition here
  adds a check or a stated boundary, which a strong model reads at no
  cost, and none adds exhortation.

## Consequences

An adopting agent knows what it may do without asking, where to cut each
artifact from, and when it is finished. A child re-aligns by reading
records, not by diffing blindly or trusting a summary.
