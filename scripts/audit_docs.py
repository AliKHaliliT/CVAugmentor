"""Audit the tree against its own documentation and layout conventions.

A living document rots when a sentence that was true at writing stops being true after
reality moves through a path that never touches the file. The mechanical kinds of rot are
checked here, along with the shapes the rulebook fixes: budgets, the index contract over the
whole docs zone, names, the STATE schema, the version floor claims, the Python layout
conventions, the room every directory and root file has in the map or the baseline, the
coverage of the import graph the Dependency Rule contract runs over, the immutability of
records, and the decidable half of the docstring convention. Decision records are exempt from
the freshness rules because they describe the past, which does not rot; what is held about
them is that nobody rewrites the past.
"""

import ast
import re
import subprocess
import sys
import tomllib
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LIVING = [
    "AGENTS.md",
    "README.md",
    "STATE.md",
    "docs/ARCHITECTURE.md",
    "docs/BASELINE.md",
    "docs/CONVENTIONS.md",
]

# An entry older than this is expired and must be re-verified before anything relies on it.
HORIZON_DAYS = 90
# In-flight work that has not moved in this long is either finished or stalled, and Now is
# for neither; the shorter horizon is what makes the sweep mechanical where it can be.
NOW_HORIZON_DAYS = 30
# Now is for in-flight work only; past this many entries the section is accreting, not tracking.
NOW_CAP = 5
# Bounded documents fail past this; AGENTS.md, docs/ARCHITECTURE.md, and README.md are the
# documents that grow with the system instead.
BUDGET_LINES = 150
FREE_GROWING = {"AGENTS.md", "docs/ARCHITECTURE.md", "README.md"}

BACKTICK = re.compile(r"`([^`\n]+)`")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
STATE_DATE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")
RECORD_NAME = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
DATED_RECORD_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$")
# The numbered record folders: decisions/, this project's own, and inherited/, the template's
# own carried whole in a project built from it, keeping the template's numbers so the two
# sequences never meet. A template has no inherited folder.
NUMBERED_RECORD_FOLDERS = ("decisions", "inherited")
# The upstream file a project built from the template carries: one Open section, entries dated by
# heading with a kind, a pin, and four labeled parts, expiring on the same horizon as STATE.
UPSTREAM_ENTRY = re.compile(r"^### (\d{4}-\d{2}-\d{2}) (.+)$", re.MULTILINE)
UPSTREAM_KIND = re.compile(r"^Kind: (improvement|defect)$", re.MULTILINE)
UPSTREAM_PIN = re.compile(r"^Pin: [0-9a-f]{7,40}$", re.MULTILINE)
UPSTREAM_PARTS = ("**What it is", "**How the work surfaced it", "**Records checked")
UPSTREAM_WHY = ("**Why it is believed better", "**What was worked around")
UPSTREAM_ALIGNED = re.compile(r"^Aligned to .+ at (`?[0-9a-f]{7,40}`?|the host's own commit)\.?$", re.MULTILINE)
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
DOTTED_MODULE = re.compile(r"[a-z_][a-z0-9_]*(?:\.[a-z_][a-z0-9_]*)+")
TREE_FILE = re.compile(r"[A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)+")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".ruff_cache", ".venv", "dist", "build"}
# Only a claim with the trailing plus is a floor claim; a bare version mention could be
# talking about anything, and a check may never imply more than it decides.
FLOOR_CLAIM = re.compile(r"Python (\d+\.\d+)\+")
# A changed diff line that is not a Status line; the +++ and --- headers are excluded by the
# lookahead and skipped by name where the diff is read.
ILLEGAL_RECORD_EDIT = re.compile(r"^[-+](?![-+])(?!Status: )")
NUMPY_SECTION = re.compile(
    r"^[ \t]*(Parameters|Returns|Raises|Attributes|Yields|Warns|Notes|Usage|Examples|See Also|References)[ \t]*\n[ \t]*-{3,}[ \t]*$",
    re.MULTILINE,
)
TRIO = ("Parameters", "Returns", "Raises")
# This sentence dates the immutability rule's arrival in the tree's own history, so it is what
# the check searches for, never the function's name, which a child's past may already carry.
# Changing what the check covers changes this sentence, and the anchor moves forward with it.
IMMUTABILITY_SCOPE = "records held immutable beyond their Status line: every file below a subfolder of docs/"


def git(*args: str) -> str:
    """One git call against the repository this file lives in; empty when git says no."""
    # The arguments are this script's own constants and git is the tool the family runs on.
    done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)  # noqa: S603, S607
    return done.stdout if done.returncode == 0 else ""


def tracked_files() -> list[str]:
    """Every tracked path, posix and relative to the root, so untracked local clutter never fires a check."""
    return [p for p in git("ls-files", "-z").split("\0") if p]


def drawn_entries(text: str) -> set[str]:
    """Every name drawn in a document's tree diagrams, directories without their trailing slash."""
    names: set[str] = set()
    for fence in FENCE.finditer(text):
        block = fence.group(1)
        if "──" not in block:
            continue
        for raw in block.splitlines():
            entry = raw.split("#", 1)[0].strip(" │├└─\t").rstrip("/")
            if entry:
                names.add(entry)
    return names


def looks_like_path(token: str) -> bool:
    """Whether a backticked token is claiming to be a repository path."""
    if "/" not in token or " " in token:
        return False
    if any(ch in token for ch in "<>*{}$|\\=\"'"):
        return False
    if "://" in token or token.startswith(("http", "-", "@")):
        return False
    # Only claims rooted in something that exists at the repository root are checked;
    # a first segment the root does not know is prose, not a path (media types, examples).
    first = token.lstrip("./").split("/")[0]
    return (ROOT / first).exists()


def repo_basenames() -> set[str]:
    """Every file basename in the tree, for verifying names drawn in tree diagrams."""
    names: set[str] = set()
    for p in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            names.add(p.name)
    return names


def python_roots() -> list[Path]:
    """The package trees whose layout conventions the audit holds, found by shape."""
    if (ROOT / "app").is_dir():
        return [ROOT / "app"]
    src = ROOT / "src"
    if src.is_dir():
        return [p for p in src.iterdir() if p.is_dir() and not p.name.startswith(".")]
    return []


def check_documents(problems: list[str]) -> None:
    """Paths, links, budgets, and the STATE horizon across the living documents."""
    today = date.today()
    basenames = repo_basenames()
    # Dotted names declared in pyproject.toml or in the code itself (entry-point groups,
    # contract layers) are not module claims, and their own readers verify the real ones.
    pyproject = ROOT / "pyproject.toml"
    declared = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
    for source in ROOT.rglob("*.py"):
        if not any(part in SKIP_DIRS for part in source.parts):
            declared += source.read_text(encoding="utf-8", errors="ignore")
    for rel in LIVING:
        doc = ROOT / rel
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")

        if rel not in FREE_GROWING:
            lines = text.count("\n") + 1
            if lines > BUDGET_LINES:
                problems.append(f"{rel}: {lines} lines against the {BUDGET_LINES}-line budget; split by fission")

        for match in BACKTICK.finditer(text):
            token = match.group(1).strip()
            if looks_like_path(token) and not (ROOT / token.lstrip("./").rstrip("/")).exists():
                line = text.count("\n", 0, match.start()) + 1
                problems.append(f"{rel}:{line}: names `{token}`, which does not exist")
            elif DOTTED_MODULE.fullmatch(token) and token not in declared:
                for root in python_roots():
                    if token.split(".")[0] != root.name:
                        continue
                    module_path = root.parent.joinpath(*token.split("."))
                    if not (module_path.is_dir() or module_path.with_suffix(".py").exists()):
                        line = text.count("\n", 0, match.start()) + 1
                        problems.append(f"{rel}:{line}: names the module `{token}`, which does not exist")

        for fence in FENCE.finditer(text):
            block = fence.group(1)
            if "──" not in block:
                continue
            block_line = text.count("\n", 0, fence.start()) + 1
            for offset, raw in enumerate(block.splitlines()):
                entry = raw.split("#", 1)[0].strip(" │├└─\t").rstrip("/")
                if entry and TREE_FILE.fullmatch(entry) and entry not in basenames:
                    problems.append(
                        f"{rel}:{block_line + offset + 1}: the tree names {entry}, "
                        f"which exists nowhere in this repository"
                    )

        # Links inside inline code spans are schema examples, not claims; blank the spans
        # with same-length padding so reported line numbers stay true.
        prose = BACKTICK.sub(lambda m: " " * len(m.group(0)), text)
        for match in LINK.finditer(prose):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (doc.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                line = prose.count("\n", 0, match.start()) + 1
                problems.append(f"{rel}:{line}: links to {target}, which does not resolve")

    state = ROOT / "STATE.md"
    if state.exists():
        text = state.read_text(encoding="utf-8")
        sections = re.findall(r"^## (.+)$", text, re.MULTILINE)
        if sections != ["Now", "Next", "Deferred", "Blocked"]:
            problems.append(f"STATE.md: sections are {sections}, not the four the schema fixes")
        section = ""
        for line_no, raw in enumerate(text.split("\n"), 1):
            if raw.startswith("## "):
                section = raw[3:].strip()
                continue
            stamp = STATE_DATE.search(raw)
            if not stamp:
                continue
            horizon = NOW_HORIZON_DAYS if section == "Now" else HORIZON_DAYS
            age = (today - datetime.strptime(stamp.group(1), "%Y-%m-%d").date()).days
            if age > horizon:
                problems.append(
                    f"STATE.md:{line_no}: entry last verified {stamp.group(1)}, {age} days ago against the "
                    f"{horizon}-day horizon of {section}; re-verify it against reality, then re-date or remove it"
                )
        now_section = re.search(r"^## Now\n(.*?)(?=^## )", text, re.MULTILINE | re.DOTALL)
        if now_section:
            entries = len(re.findall(r"^- ", now_section.group(1), re.MULTILINE))
            if entries > NOW_CAP:
                problems.append(
                    f"STATE.md: Now holds {entries} entries against the cap of {NOW_CAP}; "
                    f"sweep finished work into git's memory"
                )


def check_docs_zone(problems: list[str]) -> None:
    """The index contract, budgets, and naming for everything under docs/."""
    docs = ROOT / "docs"
    if not docs.is_dir():
        return
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").exists() else ""
    for f in sorted(docs.glob("*.md")):
        if f.name not in agents:
            problems.append(f"docs/{f.name}: not registered in the AGENTS.md index")
        if not f.stem.replace("-", "").isupper():
            problems.append(f"docs/{f.name}: organic documents are UPPERCASE markdown")
        if f.name not in ("ARCHITECTURE.md", "CONVENTIONS.md", "BASELINE.md", "UPSTREAM.md"):
            lines = f.read_text(encoding="utf-8").count("\n") + 1
            if lines > BUDGET_LINES:
                problems.append(f"docs/{f.name}: {lines} lines against the {BUDGET_LINES}-line budget; split by fission")
    for folder_name in NUMBERED_RECORD_FOLDERS:
        records = docs / folder_name
        if not records.is_dir():
            continue
        # Numbers are unique within a folder and never compared across the two, which is the
        # point of the split; a duplicate in the inherited folder means the copy is no longer
        # the template's folder.
        advice = (
            "renumber the newer record" if folder_name == "decisions"
            else "recopy the folder whole from the template"
        )
        numbers: dict[str, str] = {}
        for f in sorted(records.glob("*.md")):
            if not RECORD_NAME.match(f.name):
                problems.append(f"docs/{folder_name}/{f.name}: records are named NNNN-short-kebab-title.md")
                continue
            num = f.name[:4]
            if num in numbers:
                problems.append(
                    f"docs/{folder_name}/: {numbers[num]} and {f.name} share the number {num}; {advice}"
                )
            numbers[num] = f.name
    # Below the top level, docs/ holds record folders only: the numbered folders above, and
    # dated folders such as briefings or progress reports, each registered by its own row. A
    # living document belongs at the top as a flat UPPERCASE file, where the naming and budget
    # rules can see it, so anything else below a subfolder fails.
    for path in tracked_files():
        if not path.startswith("docs/") or path.startswith("docs/decisions/"):
            continue
        if path.count("/") == 1:
            if not path.endswith(".md"):
                problems.append(f"{path}: docs/ holds markdown documents only; assets live where the baseline sends them")
            continue
        folder = "/".join(path.split("/")[:2])
        if f"({folder}/)" not in agents:
            problems.append(f"{path}: {folder}/ has no row in the AGENTS.md index; a subfolder of docs/ is a registered record folder or it does not exist")
        if folder != "docs/inherited" and not DATED_RECORD_NAME.match(path.rsplit("/", 1)[-1]):
            problems.append(
                f"{path}: a file below a docs/ subfolder is a dated record named YYYY-MM-DD-short-kebab-title.md; "
                f"a living document is a flat UPPERCASE file at the top of docs/"
            )


def check_upstream(problems: list[str]) -> None:
    """The upstream file's schema and horizon, where a project carries one."""
    path = ROOT / "docs/UPSTREAM.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if not UPSTREAM_ALIGNED.search(text):
        problems.append("docs/UPSTREAM.md: no Aligned line naming the template and the commit the project is aligned to")
    if "## Open" not in text:
        problems.append("docs/UPSTREAM.md: no ## Open section")
        return
    body = text.split("## Open", 1)[1]
    entries = list(UPSTREAM_ENTRY.finditer(body))
    if not entries and "Nothing open." not in body:
        problems.append("docs/UPSTREAM.md: Open holds entries or the words Nothing open.")
    if entries and "Nothing open." in body:
        problems.append("docs/UPSTREAM.md: says Nothing open. beside open entries")
    today = date.today()
    for index, entry in enumerate(entries):
        end = entries[index + 1].start() if index + 1 < len(entries) else len(body)
        chunk = body[entry.end():end]
        label = f"docs/UPSTREAM.md: entry {entry.group(1)} {entry.group(2)[:40]}"
        if not UPSTREAM_KIND.search(chunk):
            problems.append(f"{label}: no Kind line reading improvement or defect")
        if not UPSTREAM_PIN.search(chunk):
            problems.append(f"{label}: no Pin line naming the template commit")
        problems.extend(f"{label}: part {part}** missing" for part in UPSTREAM_PARTS if part not in chunk)
        if not any(why in chunk for why in UPSTREAM_WHY):
            problems.append(f"{label}: neither Why it is believed better nor What was worked around")
        age = (today - datetime.strptime(entry.group(1), "%Y-%m-%d").date()).days
        if age > HORIZON_DAYS:
            problems.append(
                f"{label}: past the {HORIZON_DAYS}-day horizon; re-verify against the template and re-date,"
                " or make it the project's own decision and delete it"
            )


def check_rooms(problems: list[str]) -> None:
    """Every tracked directory near the root, and every root file, has a room in the map or the baseline.

    The tree is read one level deep at the root and one level below each Python root, which is
    the depth the form draws; deeper structure is the code's own and the layout check holds it.
    A directory is housed when its name is drawn in the map's tree, or the baseline names it.
    """
    arch = ROOT / "docs/ARCHITECTURE.md"
    if not arch.exists():
        return
    named = drawn_entries(arch.read_text(encoding="utf-8"))
    baseline = ROOT / "docs/BASELINE.md"
    if baseline.exists():
        for match in BACKTICK.finditer(baseline.read_text(encoding="utf-8")):
            token = match.group(1).removeprefix("./")
            named.update(seg for seg in token.split("/") if seg)
    roots = {r.relative_to(ROOT).as_posix() for r in python_roots()}
    directories: set[str] = set()
    files: set[str] = set()
    for path in tracked_files():
        parts = path.split("/")
        if len(parts) == 1:
            files.add(parts[0])
            continue
        directories.add(parts[0])
        for depth in (1, 2):
            if "/".join(parts[:depth]) in roots and len(parts) > depth + 1:
                directories.add("/".join(parts[: depth + 1]))
    problems.extend(
        f"{directory}/: exists in the tree but has no room in docs/ARCHITECTURE.md or the baseline; draw it or fold it"
        for directory in sorted(directories)
        if directory.split("/")[-1] not in named
    )
    problems.extend(
        f"{name}: sits at the root but neither the map nor the baseline names it; give it a room or remove it"
        for name in sorted(files - {"AGENTS.md", "README.md", "STATE.md", "LICENSE"})
        if name not in named
    )


def check_import_graph(problems: list[str]) -> None:
    """The import graph the Dependency Rule contract runs over covers every module on disk.

    A contract reporting KEPT over a partial graph implies more than it decided, so the
    modules grimp sees under the contract's roots are held to the modules on disk.
    """
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        return
    roots = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("tool", {}).get("importlinter", {}).get("root_packages", [])
    if not roots:
        return
    try:
        import grimp
    except ImportError:
        problems.append("the import graph library is not installed, so the contract's coverage cannot be verified; install the dev group")
        return
    for base in (ROOT / "src", ROOT):
        if base.is_dir() and str(base) not in sys.path:
            sys.path.insert(0, str(base))
    try:
        graph = grimp.build_graph(*roots, include_external_packages=False)
    except Exception as error:  # noqa: BLE001  # whatever stops the graph stops the contract too, and is reported as such
        problems.append(f"the import graph could not be built ({error}); install the project before auditing")
        return
    on_disk: set[str] = set()
    for root in roots:
        home = next((b for b in (ROOT / "src", ROOT) if b.joinpath(*root.split(".")).is_dir()), None)
        if home is None:
            problems.append(f"{root}: named as an import-linter root, yet no directory matches it")
            continue
        for module in home.joinpath(*root.split(".")).rglob("*.py"):
            if "__pycache__" in module.parts:
                continue
            parts = list(module.relative_to(home).with_suffix("").parts)
            on_disk.add(".".join(parts[:-1] if parts[-1] == "__init__" else parts))
    unseen = sorted(on_disk - set(graph.modules))
    if unseen:
        problems.append(
            f"the import graph covers {len(on_disk) - len(unseen)} of {len(on_disk)} modules under the contract roots, "
            f"so the Dependency Rule contract decides less than it reports; unseen: {', '.join(unseen[:5])}"
        )


def check_record_immutability(problems: list[str]) -> None:
    """A record changes only on its Status line, in the working tree and in every commit since this scope arrived.

    The rule binds from the commit that brought its current scope sentence into the tree, found
    in git's own history, so an adopting project is held from its adoption forward, never
    re-litigates a past it did not write under the rule, and is never caught by a widened scope
    reaching behind its own arrival. A shallow clone cannot show that history, so it fails rather
    than quietly checking less.
    """
    if not (ROOT / "docs").is_dir():
        return
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        problems.append("the clone is shallow, so record history cannot be checked; fetch the full history")
        return
    # Every subfolder of docs/ is a record folder, so the diff is read over docs/ and only
    # files below a subfolder count; the flat living documents at the top change freely.
    arrivals = git("log", "--reverse", "--format=%H", "-S", IMMUTABILITY_SCOPE, "--", "scripts/audit_docs.py").split()
    diffs = [("the working tree", git("diff", "HEAD", "--unified=0", "--diff-filter=M", "--", "docs"))]
    if arrivals:
        commits = [arrivals[0], *git("log", "--format=%H", f"{arrivals[0]}..HEAD", "--diff-filter=M", "--", "docs").split()]
        diffs.extend(
            (sha[:12], git("show", sha, "--format=", "--unified=0", "-M", "--diff-filter=M", "--", "docs"))
            for sha in commits
        )
    for where, diff in diffs:
        current = ""
        flagged: set[str] = set()
        for line in diff.splitlines():
            if line.startswith("+++ b/"):
                current = line[6:]
                below = current.split("docs/", 1)[1] if "docs/" in current else ""
                if "/" not in below:
                    current = ""
                continue
            if not current:
                continue
            if line.startswith(("--- ", "+++ ", "@@", "diff ", "index ", "similarity ", "rename ")):
                continue
            if ILLEGAL_RECORD_EDIT.match(line) and current not in flagged:
                flagged.add(current)
                problems.append(f"{current}: edited beyond its Status line in {where}; a record is immutable, so supersede it instead")


def section_entries(body: str) -> list[str]:
    """The names a NumPy section lists, read from the lines at its own indent; None. lists nothing."""
    lines = [line for line in body.split("\n") if line.strip()]
    if not lines:
        return []
    base = min(len(line) - len(line.lstrip()) for line in lines)
    names: list[str] = []
    for line in lines:
        if len(line) - len(line.lstrip()) != base:
            continue
        head = line.strip().split(" :", 1)[0].split(":", 1)[0].strip()
        if head and head != "None.":
            names.append(head.lstrip("*"))
    return names


def check_rhythm(problems: list[str], rel: str, lines: list[str], node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef, doc: str) -> None:
    """The house docstring rhythm, held byte by byte where a rule can see it.

    The exemplars open with a blank line after the header, a lone triple quote, and a blank
    line; they close with a blank line, a lone triple quote, and a blank line before the body;
    every section header stands after two blank lines; and every parameter entry is typed as
    name : type. Each of those is a shape, so each is decided here rather than reviewed.
    """
    opening = node.body[0]
    start, end = opening.lineno, opening.end_lineno or opening.lineno
    where = f"{rel}:{start}: {node.name}"
    if lines[start - 1].strip() != '"""' or lines[end - 1].strip() != '"""':
        problems.append(f"{where}'s docstring opens and closes with a triple quote alone on its line")
        return
    if start < 2 or lines[start - 2].strip():
        problems.append(f"{where}'s docstring follows a blank line after the header")
    if lines[start].strip():
        problems.append(f"{where}'s docstring opens with a blank line after the triple quote")
    if lines[end - 2].strip():
        problems.append(f"{where}'s docstring closes with a blank line before the triple quote")
    if len(node.body) > 1 and end < len(lines) and lines[end].strip():
        problems.append(f"{where}'s docstring is followed by a blank line before the body")
    body = doc.split("\n")
    for i, raw in enumerate(body):
        if NUMPY_SECTION.match(raw + "\n" + (body[i + 1] if i + 1 < len(body) else "")) and (i < 2 or body[i - 1].strip() or body[i - 2].strip()):
            problems.append(f"{where}'s {raw.strip()} section stands after two blank lines")


def check_docstrings(problems: list[str]) -> None:
    """The decidable half of the docstring convention: rhythm, the trio together, and names that match the code.

    Whether a docstring says something true, and which classes warrant a Usage block, stay
    with review; what is held here is the house rhythm of blank lines and lone triple quotes,
    that a function documenting any of Parameters, Returns, or Raises documents all three,
    that Parameters names exactly the signature with every entry typed, and that an
    Attributes section names only attributes the class declares.
    """
    for root in python_roots():
        for source in sorted(root.rglob("*.py")):
            if "__pycache__" in source.parts:
                continue
            rel = source.relative_to(ROOT).as_posix()
            text = source.read_text(encoding="utf-8")
            lines = text.split("\n")
            tree = ast.parse(text)
            # A module carries no docstring in this dialect; its name and its room in the map say
            # what it is, and only a script run as a command, which lives outside these roots,
            # opens with one.
            if ast.get_docstring(tree) is not None:
                problems.append(f"{rel}:1: a module carries no docstring; its name and its room in the map say what it is, and only a script opens with one")
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                doc = ast.get_docstring(node, clean=False)
                if not doc:
                    continue
                check_rhythm(problems, rel, lines, node, doc)
                marks = list(NUMPY_SECTION.finditer(doc))
                sections = {
                    m.group(1): doc[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(doc)]
                    for i, m in enumerate(marks)
                }
                if isinstance(node, ast.ClassDef):
                    if "Attributes" in sections:
                        declared = {t.target.id for t in node.body if isinstance(t, ast.AnnAssign) and isinstance(t.target, ast.Name)}
                        stray = [n for n in section_entries(sections["Attributes"]) if n not in declared]
                        if stray:
                            problems.append(f"{rel}:{node.lineno}: {node.name} documents attributes {stray} that the class does not declare")
                    continue
                present = [s for s in TRIO if s in sections]
                if present and len(present) != len(TRIO):
                    problems.append(
                        f"{rel}:{node.lineno}: {node.name} documents {present} alone; a full docstring carries "
                        f"Parameters, Returns, and Raises together, None. where a section is empty"
                    )
                if "Parameters" in sections:
                    arguments = node.args
                    ordered = [*arguments.posonlyargs, *arguments.args, arguments.vararg, *arguments.kwonlyargs, arguments.kwarg]
                    signature = [a.arg for a in ordered if a is not None and a.arg not in ("self", "cls")]
                    documented = section_entries(sections["Parameters"])
                    if documented != signature:
                        problems.append(f"{rel}:{node.lineno}: {node.name} documents parameters {documented} but its signature has {signature}")
                    entries = [line for line in sections["Parameters"].split("\n") if line.strip()]
                    base = min((len(line) - len(line.lstrip()) for line in entries), default=0)
                    untyped = [
                        line.strip() for line in entries
                        if len(line) - len(line.lstrip()) == base and line.strip() != "None." and " : " not in line
                    ]
                    if untyped:
                        problems.append(f"{rel}:{node.lineno}: {node.name} lists parameters without a type ({', '.join(untyped)}); an entry reads name : type")


def check_layout(problems: list[str]) -> list[Path]:
    """Folder purity and door-only __init__ files, the Python layout conventions, over a tree that exists.

    The audit says which roots it held, and fails when the tree's shape leaves it nothing to
    hold, because a run that examined nothing must not look like one that found nothing.
    """
    roots = python_roots()
    src = ROOT / "src"
    if src.is_dir():
        loose = sorted(p.name for p in src.iterdir() if p.suffix == ".py")
        if loose:
            problems.append(f"src/: holds loose modules ({', '.join(loose)}); the form is one package directory under src/")
        if len(roots) != 1:
            problems.append(f"src/: holds {len(roots)} package directories; the form is exactly one, so the layout has one tree to hold")
    elif not roots:
        problems.append("no app/ or src/ package tree exists for the layout conventions to hold, so this audit decides nothing about layout")
    for root in roots:
        for directory in [root, *[p for p in root.rglob("*") if p.is_dir()]]:
            if directory.name == "__pycache__":
                continue
            subpackages = [
                p for p in directory.iterdir()
                if p.is_dir() and p.name != "__pycache__" and any(p.rglob("*.py"))
            ]
            modules = [p for p in directory.iterdir() if p.suffix == ".py" and p.name != "__init__.py"]
            if subpackages and modules and directory != root:
                rel = directory.relative_to(ROOT)
                problems.append(f"{rel}: holds both subpackages and modules; a directory holds one or the other")

            init = directory / "__init__.py"
            if init.exists() and directory != root:
                tree = ast.parse(init.read_text(encoding="utf-8"))
                for node in tree.body:
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        continue
                    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                        continue
                    rel = init.relative_to(ROOT)
                    problems.append(f"{rel}: an __init__.py is a door and only re-exports")
                    break
    return roots


def declared_python() -> str | None:
    """The version ruff's target-version pins, which is the tree's one number."""
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        return None
    match = re.search(r'target-version = "py(\d)(\d+)"', pyproject.read_text(encoding="utf-8"))
    return f"{match.group(1)}.{match.group(2)}" if match else None


def check_version_story(problems: list[str]) -> None:
    """Every floor claim in living prose names the version the tree declares."""
    declared = declared_python()
    if declared is None:
        return
    for rel in LIVING:
        path = ROOT / rel
        if not path.exists():
            continue
        problems.extend(
            f"{rel}: claims Python {claimed}+ while the tree declares {declared};"
            " the version story is one number"
            for claimed in FLOOR_CLAIM.findall(path.read_text(encoding="utf-8"))
            if claimed != declared
        )


def main() -> int:
    """Run every check and report each disagreement between the tree and its conventions."""
    problems: list[str] = []
    check_documents(problems)
    check_docs_zone(problems)
    check_upstream(problems)
    check_rooms(problems)
    held = check_layout(problems)
    check_import_graph(problems)
    check_record_immutability(problems)
    check_docstrings(problems)
    check_version_story(problems)

    for problem in problems:
        print(problem)
    if problems:
        print(f"\n{len(problems)} problem(s). The tree disagrees with its own conventions.")
        return 1
    over = ", ".join(r.relative_to(ROOT).as_posix() for r in held) or "no package tree"
    print(f"The tree agrees with its own conventions (layout held over {over}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
