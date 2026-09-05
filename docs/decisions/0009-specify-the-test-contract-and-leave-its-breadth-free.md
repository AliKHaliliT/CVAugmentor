# 0009. Specify the test contract and leave its breadth free

Status: Accepted
Date: 2026-08-05

## Context

This template specifies where every production module goes and why. Tests were the one part of it with no rule at all. The frozen rulebook and the repository baseline mentioned tests zero times, AGENTS.md said only that test breadth was an intentional gap, and the architecture map named the mirrored folder without saying what belonged in it.

That is the worst place to leave unspecified, because a test is written under time pressure, reviewed more loosely than the code it covers, and is where an agent improvises most freely. An improvised suite in a ports-and-adapters package reaches for patching, and a patched internal passes green while quietly voiding the substitutability the ports were built to provide. For this package that is not a stylistic loss; the ports are the architecture, so a suite that bypasses them is testing a different design from the one shipped.

The template also asserted a shape it never demonstrated. `tests/src/keel/` held a single `.gitkeep`, so the folder claimed a convention with no example of it, while the sibling client template backed the same claim with real suites. Every other convention here is taught by a worked example in the demo domain, and this was the sole exception.

A wording defect sat on top of that. AGENTS.md called the gap "test breadth", which describes a thin suite, when in fact there was none.

## Options considered

- **Leave tests unspecified and let each project decide.** Rejected: the styles exist so a project never has to invent structure, and tests are structure. Leaving the most improvisation-prone part free contradicts the premise.
- **Specify tests fully, including a coverage threshold and a naming schema.** Rejected: a percentage gate buys assertions that assert nothing, and a naming schema buys review nitpicks.
- **Specify the frame and leave the volume free.** Accepted.

## Decision

Three rules bind. Suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by a hand-written fake satisfying the port in `domain/interfaces` that it stands in for, and never by patching a module's internals. No coverage threshold is imposed.

Test files stand outside the every-export documentation rule, since a suite documents itself through the name of each case and the assertion it makes. That belongs in the frozen rulebook, because it is a code-level documentation question, and it is the only part of this decision recorded there.

The rule ships with a worked example rather than as prose alone, and the example makes a further point the rule does not. `tests/src/keel/services/execution/test_agent_runner.py` composes the shipped registry, transcript, and event-sink adapters, because each is already deterministic and runs in process, and stands in only for the reasoner and a tool, which are what reach a model and the outside world in production. So the honest reading of the substitution rule is not "fake everything", it is "substitute at the seam, and prefer a real adapter when the real adapter is already suitable".

The gap sentence in AGENTS.md now states what is true, which is that the suite demonstrates the shape rather than being a thin version of a real one.

## Consequences

A suite added here has a shape to match and an example to read. The type checker now covers the tests under the same strict settings as the package, and it passes without a single suppression, which is evidence that the ports are narrow enough to satisfy honestly.

The suite also documents the loop's contract in a way prose could not, pinning that a failing tool becomes data unless configured to halt, that the step budget bounds a reasoner that never stops, and that a broken event sink never takes a run down. Those were properties the code had and nothing asserted.

The cost is that a fake is more work than a patch. That is the intended trade, since a fake declared against a port stops compiling when the port changes, where a patch would silently keep passing.
