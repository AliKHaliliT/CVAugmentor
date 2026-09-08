# 0042. Give the upstream report a place and a defect class

Status: Superseded by 0047
Date: 2026-09-07

## Context

Four upstream reports reached the family in ten days from three projects,
and no two had the same container. The guide fixed the content of an entry
and the order of the work, and never named a path, a filename, whether a
report is one file or one per entry, or a date, so each agent invented the
rest: six files with one entry each, one file for one finding, one dated
file with numbered entries. Separately, an adopting agent found a defect in
a template, worked around it, and sent nothing. The section's trigger word
was improvement, and its qualifying step told the agent to be sure a
candidate was genuinely better before writing it down. A small local patch
did not read as an improvement to propose, and the adoption gate's "nothing
qualified" deferred to the same judgment.

## Decision

The report is a record of the child at
`docs/upstream/YYYY-MM-DD-short-kebab-title.md`, one file per report, dated
by the day it is sent and never edited afterwards, registered by one index
row, and held by the rulebook's existing rules for dated records. Its shape
is fixed. An opening paragraph names the project, the template commit it is
aligned to, and the styles it uses; numbered entries follow with four
labeled parts each; a closing line asks the receiver to verify before
adopting, and a last line lists what the project holds locally until the
reply arrives. The reply is filed beside the report as a dated record of the
child's own.

A report carries two kinds of entry. Improvements are judged as before. A
defect is never judged. Anything worked around, patched, suppressed, or left
unmade in template-owned bytes or template-prescribed behavior is an entry,
whether or not the child is sure it is a defect and however small the fix,
and an entry may say plainly that the child could not tell a defect from its
own misunderstanding. The delivery gate gains an item, upstream honesty,
requiring every such workaround to be written down before delivery, in
STATE.md until the report is sent and as a defect entry in the report
itself. The adoption gate's report item now asserts both halves, that no
improvement qualified and that nothing was worked around.

## Options considered

- A mechanical detector for the marks a workaround leaves, a suppression
  comment, a type ignore, a warnings filter, a disabled lint, in carried
  files was deferred. A child carries no tracking of which files came from
  the template, so the check would be heuristic, and the prose rule with the
  gate item is the right size until the detector has data.
- One report per entry was refused, because the reply is a re-alignment
  order for the whole report and a child re-aligns once.
- Keeping the report outside the tree, as an issue alone, was refused,
  because the child's history would then show neither what it sent nor what
  it was told.

## Consequences

The maintainer receives one shape. A child's history carries every report it
sent and every reply it followed. A workaround can no longer be kept in
silence by an agent's judgment of its size. The template itself carries no
`docs/upstream/` folder, having no upstream, and the audit needs no new
check because the folder rule already holds dated records.
