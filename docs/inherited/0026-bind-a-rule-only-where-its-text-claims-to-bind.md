# 0026. Bind a rule only where its text claims to bind

Status: Accepted
Date: 2026-08-24

## Context

During the third treasury study, effort was spent applying house conventions
to material those conventions never named. Untracked working files that would
be discarded at the study's end were restyled for prose, and their line counts
were read as defects to trim, though no reader would ever open them and no
rule's text reached them. The same reflex appears outside a study whenever a
file's length alone is offered as a reason to shorten it, which treats the
length budget for living documents as though it governed every file.

Each rule in the family already names its own ground when read closely. The
length budget speaks of living documents, and records are exempt from it. The
prose law speaks of tracked bytes written for a public audience. A study
stage's cap is declared for that stage, and the method had already learned
that a rule written for one stage can be wrong at the next. What was missing
was the general statement, so the reach of a rule was being decided by
instinct instead of by its text, and instinct reached too far.

## Decision

A rule binds only where its own text claims to bind. A length budget governs
the document whose budget it is, the prose law governs a tracked byte, and a
stage's cap governs that stage; outside that reach a rule does not apply at
all.

Two things follow. Nothing is spent applying a convention to material it never
named, so an untracked working file that will never ship is not trimmed,
restyled, or corrected into compliance with any house rule. And a count taken
of such material stays legal everywhere, because counting is measurement; what
changes is that the count is never a finding to fix.

## Consequences

The agent guide carries the rule in one line, identical across the family. The
treasury's study method states the same split in its own terms, since a study
is where the most scaffolding gets written. The working files there answer
only to the machine-readable contract that keeps them checkable, and the
deliverable answers to everything from the fold onward.

No existing check changes, because no check was enforcing a rule outside its
ground; the overreach lived in passes and review rather than in tools. What
changes is where effort is allowed to go, since work spent restyling what no
rule names and no reader opens is now recognized as spent outside every rule's
reach.
