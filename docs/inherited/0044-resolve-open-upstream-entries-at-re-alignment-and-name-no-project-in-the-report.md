# 0044. Resolve open upstream entries at re-alignment and name no project in the report

Status: Superseded by 0047
Date: 2026-09-07

## Context

The upstream section described the reply as the re-alignment order and told
the child to list what it held locally until the reply arrived, so a child
whose maintainer said only that the report was reviewed and the latest should
be fetched had held items and no written procedure for them. Its
re-alignment read the records since the pin, recopied the carried files, and
re-adapted the rest, but never walked the entries it had sent, so it could
not tell an entry the template had silently fixed from one the template had
ignored, and a later reader could not tell why the project differed from its
style. The same section asked the report to name the project. The report is
the one artifact that leaves a project, and it leaves for a public repository
where it is quoted verbatim into records, commits, and replies, so a private
project's name and domain traveled with it; the first reports did exactly
that, and the template's own dispositions repeated them.

## Decision

No reply is owed, and re-alignment does not wait for one. Every open entry of
the child's upstream reports is resolved at re-alignment against the new
pin, by the diff of the files the entry touches and the records since the
pin. An entry the template now carries is adopted in the template's form and
the child's draft dropped. An entry a record refuses is dropped, or kept as
the child's own decision record where the matter is the child's to decide.
An entry the template is silent on stays open with the child's version in
place, which is what tells a later reader why the project differs from its
style. The resolution is one dated record beside the report, the adoption
gate holds it, and a reply, when one comes, is filed as well and makes the
resolution short.

The report names nothing that identifies its sender: no project name, no
person, no host, no path or address pointing at the project, and no fact
about its domain beyond what a finding needs, because it is written for the
template's public audience whatever the sending project's visibility. The
delivery gate holds it. The maintainer's dispositions and replies name a
report by its date and alignment pin, never by the project.

## Options considered

- Requiring a reply was refused. A maintainer who says fetch the latest and
  nothing more is common and honest, and a rule the world routinely breaks
  teaches an agent to improvise around it.
- Tracking open entries in STATE.md was refused. An unanswered report is not
  the child's work to do, the report itself is the durable ledger, and the
  state file's horizon would demand re-dating what has not changed.
- A mechanical check for project names was refused, because a checker cannot
  decide what identifies a project; the skeleton and the gate item carry it.

## Consequences

A child can be told nothing and still re-align correctly, and its history
shows for every divergence whether the template took it, refused it, or has
not spoken. A report can be pasted into the template's public records without
redaction. The two dispositions written before this rule keep the words they
carry, because records are immutable and pushed history is not rewritten.
