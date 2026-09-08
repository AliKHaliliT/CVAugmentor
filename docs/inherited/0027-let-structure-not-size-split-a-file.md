# 0027. Let structure, not size, split a file

Status: Accepted
Date: 2026-08-25

## Context

The owner favors small files, and the instinct has two roots worth separating.
One is files that demand scrolling and re-scrolling, which is usually an
ordering problem rather than a size problem, since a file laid out in reading
order stays navigable far past the length where a shuffled one is lost. The
other is that a several-thousand-line file reads as a god file even when it
breaks no rule, because a file that size is carrying a module's weight in a
file's clothes.

The question was whether to answer the instinct with law. A line limit for
code files was considered, and so was an atomization convention, one function
or one class per file, with wrapper classes giving large classes a smaller
face. Both were rejected by rules the family already holds. A line cap is a
check that implies more than it decides, since it decides a count while its
green light would be read as cohesion, which it never examined. A cap also
manufactures the wrapper pathology on schedule, the same disease the family
banned at small scale in the immediate-return rule and the return-naming
rule, a name that adds nothing and is paid for by every reader. And a fold
budget from the treasury's studies does not transfer, because a budget forces
genuine merging in a redundant catalog while code split by size is not folded
but scattered, growing the distance between related lines.

What survived is the part of the instinct that is structural rather than
numeric. A file that big almost always has internal sections its author could
already name, the comment banners and the clumps of functions that travel
together. Nameable sections are modules asking to exist.

## Decision

A file holds one idea, and the rule is judgment rather than a gate.

A file grown past easy reading is a prompt to ask whether it still holds one
idea. When its sections have earned names, it is a folder wearing a file's
name, and the split follows those names rather than any count, with the
style's re-export convention keeping the import surface unchanged so no
caller pays for the move. A file with no nameable sections, a generated table
or one long linear procedure, is one idea at its honest size and stays whole.

Size is the symptom and never the verdict. No line limit exists for code and
none may be added, because a cap would decide by count what only structure
can decide.

## Consequences

The README's conventions carry the rule, and no check changes, since the rule
is review's to apply. Size remains legal to measure anywhere, under the rule
that a count of material no rule names is a measurement rather than a finding.

Three shapes are refused by name. A line limit of any value. Atomization
conventions such as one function or one class per file, which optimize the
file listing at the cost of every actual reading. And wrapper classes or
forwarding files created to make something look smaller, which add a seam and
no meaning. Folder depth is also earned one level at a time, as sections
themselves grow sections; nesting built ahead of need is speculative
structure.

Size and importance stay independent on purpose. The rule says nothing about
how load-bearing a file is, because a generated fixture can be enormous and
trivial while the most load-bearing file in a project can be its smallest.
