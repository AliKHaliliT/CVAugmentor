# Repository Baseline

This file is the living rulebook for the repository's always-present files: which files must exist, which must never be tracked, and how each may be modified. Unlike [CONVENTIONS.md](CONVENTIONS.md), this document is not frozen. The baseline evolves with tooling, and changes that reshape it are recorded as decision records (its adoption is [0003](decisions/0003-adopt-the-repository-baseline.md)).

## Always present

| File | Role | Modification rule |
| --- | --- | --- |
| `README.md` | Human-facing overview. | Living document; its structure and inheritance rules are fixed by the README schema below. |
| `.gitignore` | What git must never track. | Every rule must correspond to the actual stack: add into the matching labeled section (project rules under `Project specific`), and remove a rule when the tool or framework it serves leaves the project, including when instantiating this template for a different stack. Never remove a rule that still matches something real without an owner decision. The same stack-matching curation applies to `.dockerignore`. |
| `.gitattributes` | Line-ending and binary policy, so repository bytes never depend on a contributor's local git configuration. | Near-frozen; changes are owner decisions, because they silently rewrite every contributor's checkout. |
| `.editorconfig` | Vendor-neutral editor baseline (charset, indentation, final newline). | Near-frozen; same reasoning as `.gitattributes`. |

The documentation spine (`AGENTS.md`, `STATE.md`, `docs/`) is also always present; it is governed by [CONVENTIONS.md](CONVENTIONS.md), not by this file.

## The README schema

The README's sections appear in this order, each with a content contract. Heading stems are fixed; the prose voice inside a section is the project's own.

1. **Title and badges.** Badges are required in public repositories and optional in private ones. Their content is the project's choice, but every badge must state something true about this repository; the template's own badges are never inherited, since they point at the template's repository. Badges are written in plain Markdown image syntax on a single line. When a showcase image follows the badges (a logo or a screenshot, either is fine, stored under `util_resources/readme/` and sitting between the badges and the pitch), the badges and the image are wrapped together in a `<div align="center">` block with blank lines around the Markdown inside it; Markdown alone cannot center, `align` is the one attribute GitHub's sanitizer honors, and inline `style` is stripped. Without such an image, the badges stay as left-aligned plain Markdown with no HTML.
2. **One-line pitch**, then a short expansion. In a project instantiated from this template, the expansion carries the attribution: one sentence linking the template and naming the template commit the project was cut from or last aligned to. It is required because the inherited conventions and decision records are unintelligible without their provenance, and the commit is what a later re-alignment starts from. The template itself has no upstream, so this applies to derived projects.
3. **The Philosophy: Why Does This Exist?** The problem the project exists to solve and the drift it defends against.
4. **The Domain.** Justifies why this domain demands the architecture. The template heads it `The Domain Example: Why ...?` because its domain is a demo; a derived project heads it `The Domain: ...` because its domain is real.
5. **Core Architectural Pillars.** Numbered, bold-named, and the project's own: adapted to the system, never copied from the template when untrue of it.
6. **Project Structure.** A condensed annotated tree; the full map stays in `docs/ARCHITECTURE.md`.
7. **Key Features.** Bulleted, each led by a bold name.
8. **Getting Started.** Copy-paste commands grouped by scenario.
9. **Conventions.** Two canonical paragraphs inherited verbatim from the template: one pointing at the rulebook, where the documentation system, the code-level convention, and the prose law live, and one on style-level ownership and the upstream report. The README carries no law of its own; project-specific conventions may be appended as new sentences, and the canonical text is never rewritten, since paraphrase is drift.
10. **License.** Present in public repositories only, accompanying the `LICENSE` file. Its body is always exactly one line: `This work is under an [someLicense](url) License.`, with the license name and its URL filled in (for example `[MIT](https://choosealicense.com/licenses/mit/)`).

Link and image referencing follows the repository boundary. Internal document links are always relative, because they never leave the repository that resolves them, and relative paths survive forks and renames. Images are referenced relatively too, until the README itself leaves the repository. When the project is published to a package index, every image switches to the absolute raw form, `https://github.com/<owner>/<repo>/blob/<branch>/util_resources/readme/<file>?raw=true`, since the index page has no repository to resolve a relative path against. Pin the branch to `main` by default; pin to the release tag instead when a version's index page must stay historically accurate, at the cost of updating the URL when tagging.

## Present when the trigger exists

Triggers are bidirectional. The file appears when its trigger appears and is removed when its trigger disappears. A conditional file whose trigger is gone is clutter, not caution.

| File | Trigger |
| --- | --- |
| `LICENSE` | The repository is public. The license text (American spelling: LICENSE), owner-only and effectively immutable; agents never touch it. A private repository or codebase omits it, and should, because with no license granted, default all-rights-reserved copyright applies, which is exactly the posture private code wants. |
| `.env.example` | Anything reads a `.env`. Tracked and secret-free, it mirrors every variable the project consumes; the real `.env` stays ignored. |
| `.dockerignore` | A `Dockerfile` exists. |
| `requirements.txt` / `pyproject.toml` | The project's dependency manifest, per project type. A deployed application declares its runtime dependencies in `requirements.txt`; an installable package declares everything in `pyproject.toml`, including its development dependency group. A project that runs tooling also needs a `pyproject.toml` to configure it, since ruff and mypy read their settings from nowhere else, and that file carries `[tool.*]` sections with no `[project]` table when the project is not a package. |
| `CHANGELOG.md` | The project is a versioned package that consumers upgrade through (see CONVENTIONS.md). |
| `.github/workflows/` | The project runs its checks on a hosted runner. `ci.yml` runs the commands AGENTS.md documents, on push and on pull request. GitHub reads workflows only from a repository root, so a copy of this project nested inside another repository carries the file inertly until it becomes a root of its own. |
| `util_resources/` | The repository carries tracked assets. `readme/` holds every image the repository embeds (a logo, screenshots, README figures), and nothing references an image from anywhere else. Further purpose-named subfolders may be added as new asset kinds arise, each under the same trigger logic: it exists only while something uses it. |

## Never tracked

- Editor and IDE directories (`.vscode/`, `.idea/`). A setting that matters to everyone is expressed vendor-neutrally in `.editorconfig` or in tool configuration (`pyproject.toml`); a setting that does not is personal and stays on the machine that likes it. This is the assistant-shim doctrine from CONVENTIONS.md applied to editors.
- Secrets and local environments: `.env`, virtualenvs.
- `LOCAL.md`, the private local ledger, created at the repository root the first time something sensitive needs recording. Every tracked byte and every commit message is written for a public audience, even while the repository is private, because visibility can flip with one settings change and git history keeps every byte ever tracked. So confidential facts, private repository names, deployment details, and the description of what was withheld and why go here instead of into STATE.md, a decision record, or a commit body; the tracked entry carries only the public-safe version, with at most a neutral pointer such as "details local". Screenshots get the same review before being embedded, since a tracked image is as permanent as tracked text. When it is unclear whether a fact is sensitive, surface it to the owner rather than recording it (adopted in [decision 0006](decisions/0006-write-tracked-content-for-a-public-audience.md)).
- Anything regenerable: caches (`__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`), build artifacts (`build/`, `dist/`, `*.egg-info/`), coverage output.
- Operating system junk: `.DS_Store`, `Thumbs.db`, `Desktop.ini`.

## Temporary development files

Files created only to support a task in progress (scratch scripts, debug outputs, one-off harnesses, refactoring aids) are not repository content. Prefer creating them outside the repository tree in the first place. When one does live inside the tree, it is purged in the same change that ends its usefulness; it is safe to purge once its task is complete and nothing tracked references it. A development utility worth keeping across tasks belongs in `local_util_resources/`, which is already untracked. If it is unclear whether a file is still needed, surface it to the owner rather than deleting it or silently leaving it behind.

## Line endings

`.gitattributes` is the single authority: text files are stored normalized (`* text=auto`), shell scripts always check out LF (they run inside Linux containers, where a CRLF shebang breaks them), and Windows script formats (`.bat`, `.cmd`, `.ps1`) always check out CRLF. Local `core.autocrlf` settings must never be load-bearing.
