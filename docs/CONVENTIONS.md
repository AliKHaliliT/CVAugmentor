# Documentation Conventions

This file is the rulebook for this project's technical documentation: which documents exist, what species each one is, how each species is written, and where a "why" belongs. It is normative and frozen; do not modify this file. If a rule ever has to change, the change is made deliberately, by the style's owner, inside the template itself in the My-Styles repository, and recorded as a new decision record superseding the style's record 0001, which is also where the rationale behind this whole system lives. A project derived from this template never edits its copy of this file and never diverges from it, however much better a local rule looks from below; a case for changing a rule travels upstream through the report described in AGENTS.md, and the rule then changes for every project or for none.

## The two species of documents

Every technical document is exactly one of two species, and the species dictates all of its rules.

**Living documents** describe the present. They are edited in place, they are always current, and they are bounded in size. A living document never contains history: no dates, no "previously", no "we changed X to Y" narration. When reality changes, the document is rewritten to match it and the old text disappears; git remembers what it used to say. `AGENTS.md`, `STATE.md`, and `docs/ARCHITECTURE.md` are living documents.

**Records** describe one past event. A record is written once, dated, and never edited again. It is not updated to stay current, because its job is to remain an accurate account of a moment. When reality moves past a record, a new record is written that supersedes the old one. Everything under `docs/decisions/` is a record, and so is any dated document under `docs/` whatever it is called, a briefing or a progress report included, for the purpose of immutability; decisions are the kind this rulebook shapes. A report sent upstream to the style is a record as well, dated by the day it was sent and filed in an `upstream/` folder under `docs/`, with the reply it receives filed beside it; the agent guide gives its shape. In a project built from this template, the template's own decision records are carried whole in an `inherited/` folder under `docs/`, byte-identical to the template's at the alignment pin and recopied as one folder at every re-alignment, so `docs/decisions/` holds the project's own decisions and nothing else, numbered from 0001 in every project alike; a record cites an inherited one by a relative link into the `inherited/` folder.

Nearly every documentation failure is a species violation. A history file that grows until it is unusable is record-species content forced into one ever-growing living file. An architecture document that rots is a living document treated as append-only. Never mix the two species in one file.

## The spine and the organic zone

Every project carries this fixed spine:

| Document | Species | Role |
| --- | --- | --- |
| `AGENTS.md` | Living | Vendor-neutral agent entry point: the operating manual and the single documentation index. |
| `STATE.md` | Living | Current project state: what is in flight, queued, deferred, or blocked. |
| `CHANGELOG.md` | Records | Curated per-release summary for consumers; present only where consumers upgrade through releases (the trigger lives in BASELINE.md). |
| `docs/ARCHITECTURE.md` | Living | The map of the system as it is today. |
| `docs/CONVENTIONS.md` | Living, frozen | This rulebook. |
| `docs/decisions/` | Records | The decision log of this project's own choices; the durable home of rationale. |

Assistant-specific instruction files (a `CLAUDE.md`, a `GEMINI.md`, tool rule files) do not exist in this project. Every assistant reads `AGENTS.md` directly. If a tool ever genuinely cannot read `AGENTS.md`, it gets a one-line shim that does nothing but import or point to `AGENTS.md` in whatever include syntax the tool understands. A shim is not a document: it is not indexed, it carries no content of its own, and it never grows a second line.

Beyond the spine, documentation grows organically. Any further document the project needs is added under `docs/` (UPPERCASE markdown, one subject per file, one species per file) and registered in the index. The one exception in location is a directory whose purpose needs stating where a reader stands, which may carry its own `README.md` beside its contents, registered in the index like any other document. A subfolder under `docs/` is a record folder, nothing else; living organic documents are flat UPPERCASE files at the top of `docs/`, because the naming and budget rules see only that shape. A record folder beyond `decisions/`, and beyond `inherited/` where a project carries one, holds dated documents named `YYYY-MM-DD-short-kebab-title.md`, ordered by date rather than by number, immutable like every record, and registered by its own row in the index. Growth changes the number of documents, never the species rules of an existing one.

## The index contract

`AGENTS.md` holds the single index of all technical documents, each with a one-line description of what it contains and when to read it. A document that is not listed there does not exist. No reader can be expected to find it, and no agent will. Creating a document and registering it in the index happen in the same change, as does delisting on removal.

## Rules for living documents

- Present tense only; describe what is, never what was or how it got here.
- No dates and no changelog narration (`STATE.md` entries are the one exception; each carries an absolute date). A `STATE.md` date is the entry's last-verified stamp, not its birthday. Re-dating requires actually re-verifying the entry against the tree or the world; touching the text does not count. An entry older than 90 days is expired, meaning nothing may rely on it or repeat it until it is re-verified and then re-dated or removed, and the docs audit fails on it so the sweep cannot be forgotten. An in-flight `Now` entry expires after 30 days instead, since work that has not moved in a month is finished or stalled.
- Record intent and decisions, never inventory the tree can answer. A premise like "the app has no icon of its own" is the tree's fact and rots silently the day someone adds one; state the wish and let the tree carry the facts.
- A sentence in a living document is a claim, not a fact. Verify a claim before relying on it or repeating it, and end every change by sweeping `STATE.md` for entries the change completed or invalidated. Both halves bind agents and humans alike.
- Rewrite in place; never append-and-preserve. Deleting stale text is the job; git is the archive.
- Size budgets come in two classes. `AGENTS.md` and `docs/ARCHITECTURE.md` grow with the system rather than against a number, since a manual and a map must cover whatever exists; they still say everything as briefly as it can be said, and an agent guide that keeps growing usually means the project's boundary was drawn too wide, which is a scoping problem no budget fixes. Every other living document is bounded at 150 lines, the docs audit fails one that exceeds its bound, and the remedy is fission, a split by subject into child documents, each registered in the index and each bounded itself. `README.md` stands outside both classes; its shape is governed by the README schema in BASELINE.md. Growth happens by fission.
- The mechanical half of freshness is checked rather than reviewed. The docs audit verifies that every root-anchored repository path a living document names exists, a token whose first segment the root does not know being read as prose, that every relative link resolves, that no `STATE.md` entry has outlived its horizon, that no bounded document exceeds its budget, that every document under `docs/` is registered in the index or is a record in a registered record folder, numbered in `decisions/` and `inherited/` and dated elsewhere, that every tracked directory near the root and every root file has a room in the map or the baseline, that a record changes only on its Status line, that a docstring documenting parameters names the signature and carries the trio together, that the layout conventions were held over a tree that exists, and that names and the STATE schema hold their shapes. Decision records are exempt from every rule in this section; they describe the past, which does not rot.

### The STATE.md schema

`STATE.md` has exactly four sections: `Now` (in flight), `Next` (queued), `Deferred` (consciously postponed), and `Blocked` (waiting on something external). An entry earns `Now` only while its work is genuinely unfinished, or while it names a condition future work must honor that no other document carries. Completing the work deletes the entry in the same change, and a narration of the landing never replaces it, because finished work is git's memory, not STATE.md's. Every entry is one line, ends with its last-verified date (YYYY-MM-DD), and is deleted when it no longer applies; striking a line through does not delete it. The file is swept at both ends of every change. Before starting anything new, delete entries describing finished work and re-verify or delete any entry the tree no longer confirms. After finishing, sweep for entries the change completed or invalidated. The docs audit caps `Now` at five entries, so accretion fails the build instead of accumulating quietly. Re-verifying an entry means re-checking its claim or re-making its choice; a fresh date over an unexamined claim re-verifies nothing. A `Deferred` or `Blocked` entry re-affirmed unchanged across several horizons is a decision record trying to be born, and moves there. After a long absence, expired stamps everywhere are the horizon working as intended, and the first task back is the sweep.

## Rules for records (decision records)

Write a decision record when a choice shapes future work and its reasoning would otherwise be lost: an architectural boundary, a convention, a rejected-but-tempting alternative, a reversal of an earlier decision, a dead end. Records live in `docs/decisions/`, named `NNNN-short-kebab-title.md` with a zero-padded sequence number, and follow this template:

```markdown
# NNNN. Title stating the decision

Status: Accepted
Date: YYYY-MM-DD

## Context

The situation that forced a decision, and the constraints that shaped it.

## Evidence

What was run or measured and what came back. This section appears only where
the decision rests on something measured or run; a record resting on reasoning
alone omits it. The results the decision rested on are quoted here in full,
never pointed at, because a record must stay accurate after the tree it
measured moves on.

## Options considered

Each realistic option with the one-or-two-line reason it lost. This section is the highest-value part of the record, because it is what stops the same alternative from being re-proposed a year later.

## Decision

What was decided, stated plainly.

## Consequences

What becomes easier, what becomes harder, and what future work this implies.
```

An accepted record is immutable. When a decision changes, write a new record explaining why, and flip the old record's `Status:` line to `Superseded by [NNNN](NNNN-the-new-record.md)`; that status line is the only edit an accepted record may ever receive.

A dead end is written when its evidence arrives, not when work completes. A reverted approach leaves no bytes in the tree, so nothing else will remember it, and the finding is lost exactly when it is most worth keeping. Where the attempt cost real effort or could plausibly be retried, its record names the evidence that killed it, the condition that would reopen it, and the commit that held the attempt, which after the revert is the only surviving proof the attempt existed. Ordinary iteration earns no record; the test is whether someone might plausibly walk back in a month later.

## Where a "why" belongs

Rationale has exactly two homes here, chosen by reach:

1. A "why" that fits in a sentence or two and only explains one change goes in the **commit message body**.
2. A "why" that will shape future decisions, or that would be re-litigated without a record, becomes a **decision record**.

A changelog exists only where consumers upgrade through releases, so a project that versions none maintains none (the trigger lives in BASELINE.md). A versioned artifact, such as a packaged library, adds `CHANGELOG.md` as a third home, carrying the curated per-release summary for its consumers; it summarizes impact, not reasoning.

Chronology itself is never documented. Git already is the complete log, and any document that re-narrates it degenerates into a worse git log.

## Naming

Spine and organic technical documents use UPPERCASE basenames at predictable locations (`STATE.md`, `docs/ARCHITECTURE.md`), matching the ecosystem convention that uppercase markdown means "meta-document about the project". Decision records use `NNNN-short-kebab-title.md` because they are many, ordered, and cited by number. The inherited folder keeps the template's numbers untouched and a project's own records start at 0001, so a number is unique within its folder and the two sequences never meet. Other record folders name their files `YYYY-MM-DD-short-kebab-title.md`, since a briefing or a progress report is ordered by when it happened.

## Code-level documentation

Docstrings follow the NumPy style, with one house addition: classes carry a `Usage` block (not part of the NumPy standard) that holds a minimal, runnable end-to-end example. `Usage` is not a replacement for NumPy's `Examples` section; the two serve different purposes (`Usage` shows the one canonical way to construct and drive the component, whereas `Examples` illustrates specific behaviors or edge cases), and `Examples` may still be added wherever it is warranted. Where a function warrants a full docstring, all three of `Parameters`, `Returns`, and `Raises` are always present, using the `None.` sentinel when a section is empty (no arguments, or nothing raised); `Raises` otherwise lists every exception raised directly in the body, including the defensive argument-validation guards. A returned or yielded value is named only where its type cannot carry the meaning, so an opaque `str`, `bool`, or `dict[str, Any]` gets a name that says what it holds while a `RunResult` or an `AuthToken` is left bare, since repeating the type as a name tells the reader nothing twice. `Parameters` and `Attributes` always carry the name the code gives them, and `Raises` and `Warns` have no name to give.

Not everything is documented that heavily, by design. Purely internal helpers and thin mappers, such as the translator functions that bridge schemas across a boundary, keep a one-line summary. Unlike a service with an HTTP edge, this package has no layer whose contract is expressed elsewhere, so the `facade` is documented in full like every other layer. It is the surface an embedding application imports and calls directly, and its docstrings are the only place its failure modes are stated.

The rest of the NumPy vocabulary is used where it fits and omitted where it does not: a caveat becomes a `Notes` section rather than a loose sentence, a generator would document `Yields`, a `warnings.warn` would document `Warns`, and `See Also`/`References` are there for cross-references. Sections you do not see are simply not called for by that code; generated code should add them as it introduces the behavior.

A module carries no docstring; its name and its room in the map say what it is, and only a script run as a command opens with one.

Test files stand outside the every-export rule, because a suite documents itself through the name of each case and the assertion it makes. A comment belongs in a test only where the reason a case exists is invisible from its name, as with a regression guard that should name the defect it pins.

## Prose

Most of this family's prose is written by machines, so the law names the failure modes of machine writing precisely enough for review to check. The rules below govern every tracked byte of living prose and every new record. Words quoted inside this section as examples of what to cut are exempt where they are quoted, and nowhere else.

The house voice is plain declarative sentences that argue their case. Judgment is welcome when it carries its reasons, and the family's idiom of animate machinery, a gate that lives somewhere, a claim that rests, stays. What the voice never does is let a vague actor hide a decision, so "the owner removed the check" beats "the check was removed" and both beat "the decision emerged".

A small census of language-model tells is tolerated one at a time and forbidden stacked: the balanced antithesis, the triadic list, the not-X-but-Y reversal, the em dash aside. At most one such flourish per paragraph, and the rest plain sentences. The clause-colon splice, a sentence shaped as claim, colon, elaboration, is banned outright; in prose a colon introduces only a list, a quote, or a label.

An em dash is legal where it clearly beats the comma, the parenthesis, or the period it replaces, and it spends its paragraph's one flourish. A tracked file carries at most two, because the plague arrives as clusters and a cluster is countable, so CI counts that boundary while the judgment of fit stays with review.

Every sentence must survive the portability test. A sentence that could sit unchanged in another repository's documentation states nothing about this one, so it is cut or bound to this subject with a fact, a mechanism, a consequence, or a judgment this subject earned. The same test condemns the inflated vocabulary that means nothing anywhere, words in the family of delve, tapestry, paradigm shift, game changer, ever-evolving, cutting-edge, supercharge, transformative, multifaceted, meticulous, paramount, embark, empower, and elevate, and the padding phrases in the family of "it's worth noting", "at the end of the day", "in today's world", "let's dive in", and "going forward". CI greps a domain-safe subset of these on living prose, the records and the treasury excluded as quoting ground, and advises; the verdict is review's, because a banned word can be an honest domain term and only a reader knows which. A spell check runs over the same ground with the same standing, because a misspelling in the message a developer reads while something is already failing is part of the form the template teaches; a flagged word is corrected, or, when it is a real term of the domain, named in the check's ignore list, so the decision is written where the check runs.

A claim about the world names its source or dies. "Experts agree", "studies show", and "widely regarded as" are not sources; cite the work or cut the sentence, and when no source exists, say so instead of inventing weight. A specific fact enjoys the same protection, so a number is never smoothed into an adjective and "cuts the run from 40 minutes to 4" never becomes "significantly faster". Plain verbs carry claims best, "is" and "has" beat "serves as", and a trailing participle that pretends to explain, the "highlighting" and "underscoring" family, is replaced by the actual mechanism or dropped.

Theater is cut wherever it appears. That covers throat-clearing openers, setups that flatter the writer as the lone honest expert, rhetorical questions the next sentence answers, importance puffery in the family of "marks a pivotal moment" and "a testament to", negative listing, staccato fragments for drama, and endings that recap what the reader just read. A final line that turns the point into an aphorism or a mic drop is deleted, never rewritten into a better one; the piece ends on its clearest concrete sentence, and when the ending needs more, it gets a plain takeaway or the next action.

Formatting obeys the same law. No emoji in headings, no bold sprinkled mid-sentence for emphasis, no bullet list where two sentences of prose read better, no header over a two-sentence section. Format carries structure the content actually has.

A project adopting this style brings prose it did not write under a law written for prose it will. The law binds the whole tree from adoption, because a gate that excuses a class of files teaches that the class is exempt, and the adopting refactor is where the corpus is brought under it. Inherited prose that cannot be brought under the law in the same change is listed in STATE as debt, one entry per document or group, and paid before the adoption is called done; nothing converges by waiting for someone to edit it next. A path whose bytes another guard hashes or pins, such as data files with manifest digests, is excluded by name in the workflow with the reason beside it, since a comment edit that moves a provenance hash is not a prose fix.

A report to a person opens with one paragraph a reader outside the work could follow, what happened and what it means, before any detail, and every abstract finding is paired with one concrete instance, the input that broke the invariant or the line that carried the drift. This is not a schema and not layman's terms; it is the order in which an expert who did not do the work can check it. Chat replies, upstream reports, and handoffs are reports to a person and follow it.

Before shipping prose, the writer checks its own output against this section: colons only for lists, quotes, and labels; at most one flourish per paragraph and two em dashes per file; every generic sentence bound to the subject or cut; every emphasis argued rather than labeled; a report to a person opened with its plain account; the ending concrete. Beyond the counts named above no tool judges any of this, so the check is the writer's own, and review reads behind it.
