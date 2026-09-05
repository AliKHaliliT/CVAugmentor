# 0014. Prefer double quotes where the choice is free

Status: Accepted
Date: 2026-08-10

## Context

The owner carries a habit from C, single quotes for single characters, and asked whether it should become a family rule. The deliberation that followed produced a test the family now applies to every candidate general rule: a rule that claims to be language-independent must hold in any current or future style without ever breaking a syntax or changing a meaning.

The C habit fails that test twice over, since C itself forces the distinction while Python and TypeScript erase it. But so does the naive replacement. "Always double quotes" breaks standard SQL, where double quotes turn a string literal into an identifier, and rewrites shell behavior, where the delimiter decides whether a variable expands. Meanwhile the family's trees were already uniformly double-quoted in practice, with the drift that had crept in fixed by hand days earlier, so the rule existed as habit with nothing holding it.

## Options considered

- **No rule, quotes stay taste.** Rejected by the owner after seeing the drift: an unlegislated uniform style decays one commit at a time, and every decayed site teaches the next reader the wrong convention.
- **The unconditional rule.** Rejected: it fails the family's own generality test at SQL and the shell.
- **The conditional rule.** Accepted, because a rule that binds only where the choice is free is true everywhere by construction, the same move that made the frozen rulebook copyable.

## Decision

Where a language offers a free choice of string delimiter with identical semantics, use double quotes, switching only where it avoids escapes. Where the delimiters differ in meaning, the meaning decides. The sentence joins the canonical Conventions paragraphs that derived projects inherit verbatim.

Enforcement rides the Lint verb where a checker exists. Here ruff's Q rules carry it, selected beside the docstring-presence codes; the checker's first run caught one escape-avoidance site in the CLI, fixed by flipping the outer quotes exactly as the rule prescribes.

## Consequences

Quote choice stops being a per-commit decision, and the uniform tree teaches itself. The rule costs nothing where it does not bind, so SQL inside a Python string keeps its single quotes and a shell script keeps choosing by expansion. Turning the checker on immediately caught one real site, a help string escaping its inner quotes where flipping the outer ones was the rule's own answer, which is the kind of finding that says the checker earns its place.
