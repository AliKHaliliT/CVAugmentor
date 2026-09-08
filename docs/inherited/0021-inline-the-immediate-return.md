# 0021. Inline the immediate return

Status: Accepted
Date: 2026-08-14

## Context

The owner's old hand-coding rule inlined any value used only once, including
the temporary that is assigned and immediately returned, on a performance
intuition. Measured honestly, the performance case is empty in every
optimized runtime. Ahead-of-time compilers and warm just-in-time compilers
rewrite both forms into static single assignment, where every intermediate
value is an anonymous register whether the source named it or not, so the
machine code is identical. Only a pure interpreter such as CPython keeps the
extra store and load, worth nanoseconds per call. What survives review is
half of the readability claim: the assign-then-return temporary carries a
name that says nothing the function's own name did not, while a name that
explains a complex expression is documentation with one use. Use-count is
therefore the wrong criterion; information is.

## Options considered

- The full old rule, no names for single-use values. It deletes explaining
  variables, one-use names doing real documentation work, which is why the
  refactoring literature keeps Inline Variable and Extract Variable side by
  side; both directions are correct in their scope.
- A prose rule held in review. The narrow case is machine-expressible, and
  the judgment half is already covered twice, by the delivery gate's
  cognitive-load and ubiquitous-language items, so a prose rule would restate
  existing coverage.
- Performance as the stated rationale. It is false in optimized runtimes, and
  a rule justified by a wrong reason invites wrong extensions.

## Decision

The linter forbids assigning a value and immediately returning it. The Python
styles select RET504 in ruff, costing no new dependency; the client style
adopts prefer-immediate-return from Sonar's maintained ESLint plugin. The
governing line for every case the machine cannot see: a name earns its line
by saying something the expression does not, so vapid temporaries die and
explaining names live, and a computation collapses into its return only where
the expression is the meaning, as with a published formula, never where the
stage names carry the explanation.

## Consequences

The mechanical case is law with no new judgment load, and its first run on
this repository found and removed one real instance. Extract Variable stays
legal and welcome where a name is documentation. Derived projects adopt the
rule through the normal alignment wave.
