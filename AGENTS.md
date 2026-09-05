# CVAugmentor Agent Guide

CVAugmentor is an installable Python package that augments images and videos for computer vision work. It is built to [Keel](https://github.com/AliKHaliliT/My-Styles/tree/main/Keel), the style's template for Python packages, so the layer boundaries here are law rather than preference and the documentation system below is the same one every project in the family carries. Unlike that template, this is a shipped library rather than a blueprint, so nothing in it is deliberately incomplete and no gap is intentional; anything temporary appears in STATE.md.

## Commands

- Install (editable): `pip install -e .` (Python 3.14+; add the tooling with `pip install --group dev`; if an import fails after the tree moves, check where the editable install points with `pip list` before debugging code)
- Run the CLI: `cvaugmentor input.png output.png --all` lists what it wrote, and `python -m cvaugmentor --list` names every built-in augmentation
- Test: `pytest`
- Lint: `ruff check . && lint-imports` (ruff checks style and docstring presence; import-linter checks the Dependency Rule)
- Type-check: `mypy src tests` (strict mode is configured in `pyproject.toml`)
- Docs: `python scripts/audit_docs.py` (the living documents against the tree and the calendar)

The checks report at two levels. A failure is a verdict, it stops the
command, and it means a rule the tool fully decides has been broken. A warning is
advice, it leaves the exit status clean, and it comes from a check that cannot
decide its own question and so is not allowed to gate. Advice is not noise and
not optional reading. Every warning is looked at and then either fixed or
dismissed in writing, in the change that produced it, and a warning is never
silenced with a suppression comment to make a run look clean. The advisory checks here are the credential heuristics, run as `ruff check --select S105,S106 .`, which read any suggestive string as a possible secret and are wrong often enough that they cannot be a gate, and the prose-vocabulary grep in CI, which reads an honest domain term the same as a tell and so advises for review.

## Hard rules

- The Dependency Rule is absolute. `domain` and `services` never import from `facade`, `adapters`, or any SDK; layer-owned objects cross a layer boundary only through translators, a clause no import graph can see, so it is carried in review by the agent writing a change and the human reading it alike.
- Library citizenship: no global mutable state, no environment reads at import time, and a `NullHandler` on the package logger.
- Every directory holds either subpackages or modules, never a mix (the package root is the sole exception); an `__init__.py` exists only where it re-exports.
- Test suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by a hand-written fake satisfying the port in `domain/interfaces` that it stands in for; never patch or monkey-patch a module's internals, because a test bound to an implementation voids the substitutability the ports exist to provide. No coverage threshold is imposed, so breadth stays a judgment call while the placement and substitution rules do not. The shape is mapped in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#testing). An invariant with no observable output, such as work done once rather than twice, is observed through a counting fake at the seam it crosses, and where no seam exists the invariant is asking for one.
- Follow the docstring convention in the rulebook's code-level section and the documentation rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); the latter is frozen and must not be edited.
- The documentation rulebook is owned by the style. [docs/CONVENTIONS.md](docs/CONVENTIONS.md) changes only inside the template itself, in the My-Styles repository and by its owner; a project derived from this template never edits its copy and never diverges from it. A derived project that believes a rule is wrong or missing sends the case upstream instead (see [The upstream report](#the-upstream-report)).
- An em dash is legal where it clearly beats the comma, the parenthesis, or the period it replaces, and it counts as its paragraph's one flourish. A tracked file carries at most two; CI counts that boundary, while the judgment of fit and commit messages stay with review.
- Commit history speaks in the owner's voice alone: no attribution trailers, no Co-Authored-By lines, nothing naming a tool or an assistant in a commit message. Held in review, like every commit-message rule.
- A check may never imply more than it decides. A green run is a claim, so a check is named for the question it actually settles, and a check that cannot settle its question advises rather than gates. Whatever it leaves undecided is stated beside the rule as review's work, never left to look automated, because the half no tool reaches is the half that rots and it rots faster behind a passing signal. This is why the family carries no coverage threshold, no maturity score, and no metric standing in for a rule it cannot decide. A check that reads history binds from the arrival of its own scope, found in the tree's own history and dated by the sentence that states the scope, never by a name or a date a child's past could already carry, because a commit cannot be unmade and a rule that reaches behind its arrival can never go green; when the scope changes, the sentence changes with it.
- A check that makes a worker damage the work is worse than no check. When a rule fights something real, neither bend the work to earn a green run nor rewrite the rule. Pause the work in a state it can resume from, report the conflict, propose the change, and wait for the owner's explicit approval, because a rule change slipped into a busy diff is a decision nobody made. A length rule cuts filler and never information, a repair is verified for its side effects rather than for its intent, and a warning is answered rather than avoided, since an advisory a worker silences has become a gate.
- A completeness claim names its boundary. Saying that every caller was updated or every usage fixed is a fact only when it names the enumerable list it exhausted, a grep, a file list, a suite run, that a reader can re-derive. A claim over a region the claimant drew itself, such as every edge case considered, is offered as judgment rather than fact, because no boundary exists for it to have reached and the claim reports only that the claimant stopped finding things. Review probes the second kind, and trusts the first only as far as its boundary reaches.
- A rule binds only where its own text claims to bind. A length budget governs the document whose budget it is, the prose law governs a tracked byte, and a stage's cap governs that stage; outside that reach a rule does not apply at all. So nothing is spent applying a convention to material it never named, such as trimming or restyling an untracked working file that will never ship, and a count taken of such material is a measurement rather than a finding to fix.
- All prose must read as if a person wrote it. Never write the clause-colon splice, a sentence shaped as claim, colon, elaboration; in prose a colon may only introduce a list, a quote, or a label. The softer language-model tells (balanced semicolon antitheses, triadic lists, not-X-but-Y reversals) are fine one at a time and forbidden stacked, so allow at most one flourish per paragraph and keep the rest plain declarative sentences. No tool can judge these, so they are held in review, agent and human alike. The full catalog of tells, the vocabulary, and the portability test live in the rulebook's Prose section ([docs/CONVENTIONS.md](docs/CONVENTIONS.md#prose)).
- Every tracked byte is public prose. Confidential facts, private repository names, deployment details, and the description of what was withheld and why never enter a tracked file or a commit message, even in a private repository, because visibility can flip and history is permanent. Such context goes to the untracked `LOCAL.md` at the root (see [docs/BASELINE.md](docs/BASELINE.md)); read it when it exists, create it when first needed, and when unsure whether a fact is sensitive, ask the owner instead of recording it.
- Read [STATE.md](STATE.md) before starting work, and sweep it before starting anything new, deleting every entry that describes finished work and re-verifying or deleting any entry the tree no longer confirms. Its entries are claims to verify, not facts. Completing work deletes its entry in the same change, never adds a narration of the landing, and every change ends with a sweep for entries it completed or invalidated.

## The delivery gate

A task is not delivered while the gate below has findings. Carry these items from the first line written, because they are cheapest to satisfy while the code is still forming and most expensive as after-the-fact repairs; the closing pass exists to confirm, not to redo.

Closing a task follows one loop: run the checking commands above, weigh the change against every item below, fix what an item names, and repeat. One pass with no findings ends the loop. A finding is a concrete disagreement with a listed item, never general unease; the list is closed, and nothing outside it may generate rework. If the same finding survives three honest fix attempts, stop looping, record the finding and the attempts in STATE.md, and say so plainly when delivering. The names below index a wider literature; where a name's common usage and the rule beside it differ, the rule governs.

- **Cognitive load**: nothing in the change is harder to hold in mind than the task requires.
- **Granularity**: the size of every new unit (function, file, document, the change itself) is a choice, not an accident.
- **Growth honesty**: what each loop's or query's cost grows with is a choice, not an accident, and no change buys a worse growth rate where a construction of equal effort exists.
- **Ubiquitous language**: new names use the vocabulary the tree already speaks.
- **Single source of truth**: the change introduces no second copy of any fact, and anything derived points at its source.
- **Least privilege and surface**: nothing gains more access, exports, or dependencies than the task needs.
- **Adversary honesty**: every change that creates or moves a trust boundary names who it is meant to withstand, and deciding that nobody is attacking it is a decision to write down rather than an assumption to leave implicit.
- **Boundary honesty**: no data crosses a boundary unchecked, and checking happens at the door, once.
- **Loud failure**: every new failure path raises a typed error; nothing is swallowed or silently defaulted.
- **Two hats**: shape changes and behavior changes are separate steps, and no incidental reformatting rides along.
- **Waste**: nothing speculative and nothing the change orphaned is left behind.
- **The measured line**: nothing is made faster without a measurement that demanded it, and every optimization that lands records its measurement and its price.
- **Test honesty**: substitutes stand in only at the declared seams, and time, randomness, and order are controlled.
- **Point-of-use truth**: the doc comment or docstring each export carries is true, not merely present.
- **Intent-split placement**: every documentation change lands in the document whose reader it serves, per the rulebook's species.
- **Decision records**: any choice made here that would be re-litigated without a record gets one now.
- **Debt**: every shortcut taken is written in STATE.md before delivery, never carried in memory.
- **The commands**: every checking command above has passed against the final state of the tree, and every advisory finding printed along the way has been read and then fixed or dismissed in writing.
- **The hard rules**: the change disagrees with no review-held clause of this guide's Hard rules, re-read now, not recalled.

## The upstream report

This template is the style's single statement of its form, and it only stays that way if improvements flow back to it. When a refactor against this template surfaces something the template itself should have had, the improvement belongs in the template first and in the refactored project second; an improvement kept privately by one child is a quiet fork of the style.

The order is strict:

1. **Finish the refactor as specified.** The report comes after the template has been properly implemented, never instead of finishing.
2. **Qualify every candidate.** An improvement earns an entry only if it is genuinely better rather than differently shaped, the template does not already have it, and [docs/decisions/](docs/decisions/) shows no record of it being considered and rejected. Read the decision records before writing anything; a rejected idea returning without new evidence is noise, and a report invented to satisfy this section when nothing real was found is worse than no report.
3. **Write each entry as a hand-off.** One entry per improvement, self-contained enough to be pasted verbatim to an agent or handed to the template's maintainer and acted on with no other context. Each entry states what the improvement is, how the refactor surfaced it, why it is believed better than what the template does today, and that the decision records were checked and hold no prior ruling. Each entry ends by telling the receiver to verify the claim with proper research-backed grounding before adopting it, because the report is a lead, not a verdict.
4. **Apply upstream first, then align.** The improvement lands in the template before the child keeps it. Integrating it there often refines it further, so afterwards run a manual final alignment check on the refactored project, confirming it carries the upstream form of each improvement rather than the draft it started from.

Every report opens by saying why the reader is seeing it. The style's owner uses the report to point an agent at the template and improve it directly. Anyone else is holding it because this template is open source, and the right move is to file the report as an issue on the template's repository so the improvement reaches everyone who builds on the style.

The reply travels the same road down. The template's maintainer answers a report with one file that names, per entry, whether it was kept, adapted, or refused and why, what the reporting project now reverts in favor of the template's version, and the template commit the project aligns to next, so the reply is a re-alignment order rather than a verdict to interpret.

## Adopting this style

An existing repository adopts this style through one refactor, and the refactor is done when the gate below holds, not when the tree looks similar. Three rules govern the work.

The adopting agent folds, moves, rewrites, and deletes on its own authority. Ten documents that say one thing become one document that says it; a folder with no room in the map is given one, folded into a room that exists, or removed; code is rewritten into the convention rather than left beside it. Git is the archive, so none of this needs asking. What the owner reviews is content that leaves the repository, and it is reviewed once, at the end, from the inventory the agent keeps: every tracked path classified as kept in its room, folded into a named document, moved to a named room, or deleted with its reason. The pause-and-propose rule stays reserved for a conflict with a rule; a routine refactor decision never pauses.

The demo is the authority on dialect and never on scope. Every artifact the refactor produces is cut from the exemplar the map's Exemplars section names for its kind, a docstring from the exemplar docstring, a translator from the exemplar translator, a suite from the exemplar suite, because a rule names what must exist and only the style's own bytes carry how it reads. What the demo leaves out is its named incompleteness, not a ceiling. The tool configuration is dialect too. The lint, type-check, and import-contract settings the style ships, with the comments that give their reasons, are style-owned law like the rulebook; a child copies them and changes only the names that must be its own, such as the packages a contract lists, because a selection the style refused, docstring-format codes among them, forbids the very rhythm the exemplars carry.

The adoption is done when every item below holds, and the agent says so by naming the boundary it exhausted rather than by feeling finished. The gate decides what a check can decide; what it cannot, it names as review's, so a passing gate is never read as the whole.

- **Inventory exhausted**: every tracked path is classified, and no path is left undecided.
- **Audits green**: the docs audit, the lint, the type-check, and the tests pass on the final tree, which holds that every directory has a room, every document under `docs/` a species and a row, every record its immutability, and every documented parameter its name.
- **Debt paid**: the STATE debt list the adoption opened, inherited prose or inherited structure that could not be brought under the law in one change, is empty.
- **Leftovers swept**: every rule the adoption or re-alignment retired has had what it required removed from the tree, and the inventory names the sweep.
- **Pin recorded**: the README attribution names the template commit the project was aligned to.
- **Report written**: the upstream report exists, or the closing note states that nothing qualified.
- **Residue named**: whether folding preserved meaning, whether docstrings say true things, and whether prose is good are review's questions against the exemplars, and the closing note says so instead of implying the gate covered them.

Re-alignment is the same refactor in miniature. The child reads the decision records the template gained since its pin, because every rule change carries one; recopies the files the style carries verbatim, the rulebook, the baseline, the docs audit, the inherited records, the editor and attribute files, the tool-configuration blocks with their project names re-adapted, and this guide from its shared tail; re-adapts from a diff whatever it adapted at adoption; for every rule its own configuration had and the style's does not, sweeps out what that rule required, because the rule's absence in the template is a refusal rather than an oversight; runs the gate above; and moves the pin. A history-reading check binds the child from the commit its scope sentence arrived in, the re-alignment commit itself, so a red gate over older commits is a defect in the check to send upstream, never a reason to rewrite history. No changelog is kept, because the records are the changelog and a summary would be a lossy copy of them.

## Documentation index

This is the single index of the project's technical documentation. A document that is not listed here does not exist as far as this project is concerned: when you create a document, register it here in the same change; when you remove one, delist it here.

| Document | What it is and when to read it |
| --- | --- |
| [README.md](README.md) | Human-facing overview: philosophy, structure, and setup. |
| [STATE.md](STATE.md) | Living project state (Now / Next / Deferred / Blocked). Read first, always. |
| [CHANGELOG.md](CHANGELOG.md) | Curated per-release summary for consumers upgrading the package. Records; never rewritten. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The annotated map of the whole package. Read before any structural change. |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | The documentation rulebook: document species, schemas, naming. Frozen; do not edit. Read before writing or changing any documentation. |
| [docs/BASELINE.md](docs/BASELINE.md) | The repository baseline: always-present files, never-tracked files, and their modification rules. Read before adding, removing, or reshaping root-level or dot files. |
| [docs/decisions/](docs/decisions/) | Immutable decision records holding the project's "why". Read the relevant record before revisiting a settled topic; never edit an accepted record. |

There are no assistant-specific instruction files. Every assistant reads this file directly. If a tool genuinely cannot read AGENTS.md, give it a one-line shim that imports or points to this file and nothing more.
