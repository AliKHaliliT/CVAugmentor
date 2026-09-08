# 0034. Let a directory carry its own README

Status: Accepted
Date: 2026-08-28

## Context

The rulebook's organic zone put every further document under `docs/`, and
the server style had carried a registered document at `engines/README.md`
since the engines directory was created, explaining what an engine is and
the rules for adding one, exactly where a reader deciding those questions
stands. A content review of the family's law read the two against each
other and found the rulebook's letter condemning a document its own index
endorses. Moving the text under `docs/` would satisfy the rule at the
reader's expense, because the person opening the directory is the person
the document exists for.

## Decision

The organic zone gains one exception in location. A directory whose
purpose needs stating where a reader stands may carry its own `README.md`
beside its contents, registered in the index like any other document.
Everything else the organic rule says still binds it, one subject, one
species, present tense, and the index row is what makes it exist.

## Consequences

The server style's `engines/README.md` is legal where it sits. The
exception names placement only, so a document that is not answering what
its directory is for still belongs under `docs/`, and review holds that
line, since no tool can decide what a document is for.
