# Upstream report, 2026-09-08

You are reading this because a project built from the Keel template finished a
change that moved its compute layer onto an optional accelerator, and that work
surfaced one improvement the template should have and one place where the
template's own bytes had to be departed from. The project is aligned to template
commit `ba37107a9b373936f58e971aaa293d8111e82c63` and uses Keel alone. Every
entry below is a lead rather than a verdict.

## 1. Hold both paths of an optional backend to a stated tolerance

**What it is.** Where a project puts an optional dependency behind a port and
ships a fallback implementation for the case where it is absent, the law should
require that the suite execute both paths rather than one, and should hold the
two to a stated tolerance rather than to equality wherever a vendor's arithmetic
differs from its own documented formula. The tolerance belongs in a record with
the measurement that set it, so a later widening is a visible change rather than
a quiet one.

**How the work surfaced it.** The project moved fifteen pixel operations onto an
accelerator that publishes no wheel for two of its eight target platforms, so
every operation grew a second implementation. Three of those fallbacks diverged
from their accelerated counterpart by 22, 55 and 253 levels out of 255. All
three passed every other case in the suite, because nothing executed them: the
development machine had the accelerator installed, so the fallback branch was
dead code that type-checked, linted, and looked reviewed. Two of the three were
found only when a case was added that resolved the backend to absent and
compared the results. The third was found only when that case was also run over
a noise frame, because on a smooth gradient a wrong interpolation kernel lands
on nearly the same pixel and the case reads as decorative while proving nothing.

**Why it is believed better.** The template already achieves the spirit of this
in its own demo, where the provider adapter's translator suites run with the SDK
uninstalled, but it states the practice nowhere as a rule and its demo cannot
exercise the failure this finds. That adapter has no second implementation, so
absence there means the adapter is simply unavailable. The case this rule
governs is different and more dangerous, because absence means a different
implementation runs and produces subtly different output, and the project that
shipped it would never see that on its own machine. A second clause earns its
place beside the tolerance: a fixture must be chosen so the two paths can
actually disagree, since a smooth one hides exactly the class of defect the case
exists to catch.

**Records checked.** 0009 leaves test breadth free, and that is the nearest
prior ruling, but it governs which collaborators are substituted at a seam
rather than a code path that exists only on some installs, so it does not
decide this. 0015 shows the practice applied to the demo's provider adapter
without stating it as law. 0025 requires that a check imply no more than it
decides, which this strengthens rather than contradicts, since a green suite
over an unexecuted branch is the exact failure 0025 names. No record refuses it.

## 2. The tool configuration carries the demo's own stack

**What was worked around.** The adoption section makes the tool configuration
style-owned law and says a child copies it and changes only the names that must
be its own. Three settings in that block name the demo's dependencies rather
than a name the child can re-adapt. The type checker loads a plugin for the
demo's validation library, the test runner sets an async mode the demo needs,
and the import contract forbids the demo's one vendor SDK by name. This project
uses none of the three, so all three lines were deleted rather than re-adapted,
which is a departure from the instruction as written. The import contract's
forbidden list was additionally extended with the SDKs this project must keep
out of its core, which the instruction does cover, so only the deletions are
reported here.

The report cannot tell whether this is a defect or the instruction working as
intended with deletion implied. The maintainer decides. What is certain is that
a child following the instruction literally cannot, because two of the three
settings make the checks fail outright when their library is absent.

**Records checked.** 0040 makes the tool configuration law and gives the reason,
which is that a selection the style refused would forbid the house docstring
rhythm. It reasons entirely about the linter's rule selection and does not
consider settings that name a dependency. No record addresses the case.

## 3. The rulebook's one-line summary reads as licensing a one-line docstring

**What it is.** The rulebook's code-level section says that purely internal
helpers and thin mappers keep a one-line summary. Read plainly that licenses
`"""One line."""`, which the docs audit rejects, because the audit holds the
house rhythm of a blank line, a lone triple quote, a blank line, the summary,
a blank line, and a lone triple quote. Naming the rhythm in that sentence, or
saying that the summary is one line of content rather than one line of file,
would remove the ambiguity.

**How the work surfaced it.** Eight helpers were written with the compact form
across four files. The audit caught all eight in one run and the fix was
mechanical, so the cost was one cycle rather than a defect, which is why this
sits below the other two.

**Records checked.** 0040 introduced the mechanical rhythm check and explains
why the rhythm is held where a rule can see it. It does not discuss the
rulebook's wording. No record addresses the case.

## Closing

Verify every claim above with proper research-backed grounding before adopting
it, because this report is a lead and not a verdict.

Pending a reply, the project holds locally: a section in its agent guide
requiring both paths of an optional backend to be executed and held to one
level per channel, a decision record carrying that tolerance with the
measurements that set it, a suite case that resolves the backend to absent over
both a gradient and a noise fixture, and a tool configuration with the three
demo-stack settings removed.
