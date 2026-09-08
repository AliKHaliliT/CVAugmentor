# 0047. Keep upstream entries in one living document until they resolve

Status: Accepted
Date: 2026-09-08

## Context

In three days the upstream report grew from a section of prose into a folder
of immutable letters, replies, and resolution records, with a gate item for
each and a name for each, and the owner of the family could no longer tell
from a project's tree whether anything had gone upstream, what had become of
it, or which of three file kinds to read. The design had treated in-flight
work as history. An open entry is pending between a project and its style,
resolved and then gone, which is what `STATE.md` already models, and
anything worth remembering about it belongs in a decision record.

## Decision

A project built from this template carries one living document,
`UPSTREAM.md` at the top of `docs/`, present from adoption on and registered
by one row; the template has none. Its schema is fixed and the audits hold
it: a title, one sentence that every entry is a lead and not a verdict, and
one section, Open, holding the words Nothing open or entries, each a dated
heading with a kind line, a pin line, and four labeled parts. An entry is
written in the change that closes the work which produced it, and the
closing note names it. It is resolved at re-alignment against the new pin,
the records the template gained, and the treasury's dispositions: deleted
where the template took it, deleted or turned into the project's own
decision record where a record refused it, left in place where the template
is silent, and re-verified and re-dated or made the project's own decision
once it is ninety days old. No reply is owed and none is filed. The file is
free-growing, the horizon bounding it; it is dated, the second exception to
the living-document rule beside STATE. The delivery gate holds one sentence
about it and the adoption gate two. The folder of letters, the reply files,
the resolution records, and the bundle rule are gone, and the demo arrow
carries the exemplar file.

## Options considered

- Keeping the folder and adding a marker per file kind was refused, because
  the confusion was not the names but the species; three kinds of immutable
  letter for one pending item is the wrong shape however they are named.
- One file per entry, living, was refused, because the family already has a
  document of this exact kind and a second one with sections is what a
  reader expects to find beside it.
- A line budget instead of a horizon was refused, because a project mid
  refactor may legitimately hold five long entries, while an entry nobody
  has resolved in a season is the thing the rule exists to surface.

## Consequences

The owner opens one file per project and reads it the way STATE is read.
Nothing about the upstream lives in the record folders, and nothing waits
for a reply. Every record the family wrote on the folder design is
superseded by this one, which is the honest cost of having built it wrong.
