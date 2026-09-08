# 0032. Prove the built artifact, not the editable install

Status: Accepted
Date: 2026-08-28

## Context

Every CI gate ran against an editable install. `pip install -e .` points the
interpreter at the source tree, so lint, types, and tests all exercise the
tree and none of them exercise the thing `python -m build` would ship. A
wheel that silently drops a package through wrong discovery configuration, or
a dependency imported in `src` but declared only in the dev group, would pass
every gate and fail at the first real install. The gap surfaced while reading
an external repository, ayghri/i-have-adhd, whose CI installs its plugin into
a scratch configuration and fails unless the plugin reports enabled. The
lesson generalizes past plugins, since the load layer is a contract of its
own, and only loading tests it.

## Decision

CI gains a Package step after the test step. It builds the wheel, installs it
into a scratch virtual environment, and imports the package by the name read
from `pyproject.toml`, so the step is name-agnostic and survives verbatim
transplant into an arrow or an instantiated project.

The step is CI-only and joins no gate command list, because the delivery gate
is family-shared text and a wheel is this genre's artifact alone. Helm proves
its own artifact with its build step, and an application has no wheel to
prove.

## Consequences

Packaging breakage turns CI red the day it happens instead of the day someone
installs. The scratch environment starts from a bare interpreter, so a
runtime dependency hiding in the dev group cannot ride along unnoticed. The
demo arrow inherits the step byte-verbatim through its carried inert
workflow, and the import-by-declared-name form is what lets one text serve
every package cut from this template.
