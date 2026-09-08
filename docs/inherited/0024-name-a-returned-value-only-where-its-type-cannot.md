# 0024. Name a returned value only where its type cannot

Status: Accepted
Date: 2026-08-23

## Context

The NumPy docstring style allows a returned value to be written either as
`name : Type` or as `Type` alone, and the convention in the README chose
neither. It fixed the three-section trio, the empty-section sentinel, and the
scope of `Raises`, and it said nothing about this. A silence in a written
convention is where drift gets in, and it did.

Reading the two Python styles side by side made the drift visible. The server
style names the return in 9 of its 58 typed returns and leaves the other 49
bare. The package style names none of its 24. The obvious reading is that the
package style drifted from the server style, and it is wrong. The package
style matches what the server style does in 84 percent of its own returns.

The nine are the interesting part, because they are not scattered. Eight of
them name the return precisely where the type says nothing, `formatted_log :
str`, `record_logging_switch : bool`, `payload : dict[str, Any]`. A bare `str`
tells a reader nothing about what the string holds, and the name is doing the
work the type failed to do. The ninth was `token : AuthToken`, where the type
already says token, and it was the only one of its kind in the repository.

So the practice was already consistent, on a rule nobody had written down. The
name earns its place when the type cannot carry the meaning.

## Decision

A returned or yielded value is named only where its type cannot carry the
meaning. An opaque `str`, `bool`, `int`, or `dict[str, Any]` gets a name that
says what it holds. A `RunResult`, an `AuthToken`, or any type whose own name
is the answer is left bare, because repeating the type as a name tells the
reader the same thing twice and trains them to skip the line.

The rule reaches `Returns` and `Yields`, which are the sections where NumPy
leaves the choice open. `Parameters` and `Attributes` always carry the name
the code gives them, so no judgment arises. `Raises` and `Warns` have no name
slot at all, so the question cannot arise there, which answers the obvious
worry about this spreading into the exception sections.

The convention now says so in the README, which is where the docstring rules
already live and where the silence was.

## Consequences

Five returns in this repository named an opaque type and now carry a name,
across the three tool results, the expression evaluator, and the command-line
exit code. This repository had no stutter to remove.

The rule is held in review and is not machine-checked, on the principle that a
check may never imply more than it decides. A checker could catch the stutter
case, where a name is a lowercase echo of its own type, but it could never
decide whether a given type carries its meaning, which is the larger half. A
check limited to the stutter would have to be named for the stutter, and a rule
about naming is not worth a tool that examines the smaller half of it.
