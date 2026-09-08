# 0045. Carry the template's records in an inherited folder and start a project's own at one

Status: Accepted
Date: 2026-09-08

## Context

A project built from the templates re-aligned and met the template's newest
records under numbers its own records already held. A child's `docs/decisions/`
mixed two sequences with two writers: the template's records, carried
byte-identical and recopied at every re-alignment, and the child's own,
continuing the count from wherever the template stood at adoption. Collision
was a matter of time once the template grew weekly, and the duplicate-number
check answered it with "renumber the newer record", the wrong advice under a
mirror. The adopting agent offered three ways out, an offset for the child's
numbers, renumbering at every re-alignment, or a separate folder for the
child's records, and paused for the style to rule.

## Decision

In a project built from this template, the template's own decision records
are carried whole in an `inherited/` folder under `docs/`, byte-identical to
the template's at the alignment pin, recopied as one folder at every
re-alignment, registered by one index row, and never edited or added to.
`docs/decisions/` holds the project's own decisions and nothing else,
numbered from 0001 in every project alike, the adoption itself being the
first of them, and a record cites an inherited one across the folder as
`../inherited/NNNN-short-kebab-title.md`. A number is unique within its
folder and the two sequences never meet, so the template grows without
colliding with any child, and a reader knows whose record they hold from
where it sits.

The audits treat both folders as numbered record folders, holding the name
shape and unique numbers within each, and the docs-zone rule stops asking
the inherited folder for dated names. The family audit holds the demo
arrow's inherited folder as its style's decision folder whole, nothing
missing and nothing extra, and the carried guide tail now stops before the
documentation index, since the index lists a project's own documents. The
adoption gate's pin item requires the inherited folder to hold the pin's
records whole. A project that mixed the two sequences fixes itself by moving
the inherited records into their folder, pure renames the immutability check
passes, and keeps its own numbers as they are.

## Options considered

- Offsetting the child's numbers to 1001 and above was refused. It is the
  cheapest change and works for a child born under it, but every existing
  child would renumber its own records, and honest renumbering edits record
  bodies, since records cite each other by number, which the immutability
  check rightly flags; a number range that carries jurisdiction is also a
  convention a reader must know rather than something the tree shows.
- Renumbering the child's records at every re-alignment was refused, because
  records are immutable and cited by number, and a rule that renames them is
  a rule against records.
- Moving the child's own records to a separate folder was refused, because
  `docs/decisions/` would then mean the template's records in a child and the
  project's own in a template, and the carried folder would still be a merge.

## Consequences

The carried folder is a pure mirror, decidable by byte identity, and
jurisdiction is visible in the tree rather than in a number range. The
template can grow for as long as it lives. A project born before this rule
moves its inherited records once, with no content edits, and its own records
keep the numbers they have.
