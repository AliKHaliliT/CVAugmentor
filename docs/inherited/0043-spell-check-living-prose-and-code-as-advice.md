# 0043. Spell-check living prose and code as advice

Status: Accepted
Date: 2026-09-07

## Context

A project's spell check found a misspelling in a carried error message of
the server template, in the text a developer reads at the moment something
is already failing, and reported it. The family had no spell check, only the
vocabulary grep. A sweep of the whole family with codespell found that one
misspelling in living prose and code, two false positives, a real word in
the four audit scripts and a test framework's API name, and dozens of flags
in the treasury's vocabulary records, nearly all acronyms and domain terms,
with a handful of genuine typos that stay where they are because numbered
study files are immutable records.

## Decision

CI runs codespell over living prose and code as an advisory step beside the
vocabulary grep, in the family workflow and in every template's own
workflow, with records, claims, reviews, upstream reports, the treasury,
generated files, and dependencies excluded as quoting ground. A flagged word
is corrected, or, when it is a real term of the domain, named in the step's
ignore list, so the decision is written where the check runs. The rulebook's
prose section states the check and its standing, and the tool is pinned by
version.

## Options considered

- Gating on spelling was refused, because the checker cannot tell a
  misspelling from a domain term, and a check may never imply more than it
  decides.
- A dictionary file for the family was refused for now. The ignore list
  holds two words, and a file earns itself when the list grows.
- Checking the records was refused, because they are immutable and a typo
  in a record is part of what happened.

## Consequences

On today's tree the step prints nothing once the reported typo is fixed,
which is the right silence for an advisory. A child inherits the check from
its inert workflow, and its own ignore list grows in its own workflow.
