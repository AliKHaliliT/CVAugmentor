# 0058. Publish the API reference from main with pdoc

Status: Accepted
Date: 2026-09-09

## Context

[Decision 0045](0045-retire-the-generated-documentation-site.md) retired the
1.x Sphinx site and its `gh-pages` branch, on the grounds that the arrangement
had three moving parts and rendered text already readable at its source. It
listed publishing from `main` into an artifact as an option and refused it,
because it kept Sphinx, its configuration, its theme, and a build step that
fails for reasons unrelated to the package.

The owner wants the rendered docstrings back. That reopens the question rather
than the old answer, and the option 0045 refused is the one worth re-examining,
because two of its three objections were about Sphinx rather than about
publishing.

## Evidence

pdoc 16.0.0 was run against the installed package before any of this was
written down, to find out what a config-free tool actually produces here.

Pointed at the package alone it documented one page:

```
cvaugmentor.html
index.html
```

The layer directories are deliberately namespace packages with no `__init__.py`
([the layout convention in the map](../ARCHITECTURE.md)), and no submodule
walker discovers those, so the catalog has to be named:

```
pdoc cvaugmentor cvaugmentor.adapters.augmentations
  -> a page per augmentation, fifteen of them, plus the curated surface
```

The rendered augmentation page carries the whole docstring, checked by
substring against the source:

```
Softens a frame with three box passes   present
Usage / Parameters / Raises             present
radius / seed / reseed / RADIUS_RANGE   present
```

The shared frame helpers are internal to the adapters and excluded by pdoc's
negative pattern, leaving exactly the fifteen augmentation pages:

```
!cvaugmentor.adapters.augmentations.frames
  -> blur brightness cutout exposure flip grayscale hue negative
     no_augmentation noise rotate saturation shear translation zoom
```

A search index is generated. No configuration file exists at any point.

The curated package page carries the names of the augmentation classes but not
their docstrings, which is why naming the catalog matters: documenting only the
facade would publish the surface and lose the text this decision exists to
restore.

## Options considered

- **Restore Sphinx as 1.x had it.** Refused for the reasons 0045 gives, which
  still hold.
- **Sphinx, built from `main` into an artifact.** Better than 1.x and still
  carries `conf.py`, a theme, and a build whose failures are its own. The
  written documentation here is Markdown, which Sphinx reads only through a
  further extension.
- **MkDocs with mkdocstrings.** A real contender, Markdown-native, and it would
  publish the written documents beside the reference. Refused because its source
  directory would be `docs/`, whose contents are a rulebook, a baseline, and
  ninety-odd decision records, none of which a package's user came for; keeping
  them out means a second source tree and a config file listing what to include.
- **pdoc, from `main`, into an artifact.** Chosen.

## Decision

The API reference is published again, built by pdoc from `main` and served from
an upload artifact. No branch holds generated output, no configuration file
exists, and the whole build is one command that AGENTS.md lists after the
family's five.

It is a deployment and not a check. It lives in its own workflow, and its
failure never blocks a merge, because what the gate holds about docstrings is
their shape and the docs audit already decides that.

The command names the catalog explicitly and excludes the frame helpers. Both
are consequences of the architecture rather than preferences, so both carry
their reason in the workflow and in the guide.

pdoc sits in a `docs` dependency group of its own rather than in `dev`, so
running the suite does not install a publishing tool.

## Consequences

The docstrings are readable as a site again, and the three moving parts 0045
objected to are gone rather than rearranged: one branch, no configuration, one
command.

Publishing needs GitHub Pages set to build from GitHub Actions, which is a
repository setting no command in this tree can reach. STATE.md carries it as
blocked until the owner turns it on, exactly as the reverse of this decision
did when the site was retired.

An augmentation added to the catalog appears in the reference with no change
here. A new layer, or a module outside the catalog worth publishing, means
editing the command in two places, the workflow and the guide, which is the
price of not owning a configuration file.

The written documentation stays where it is and is not published. Anyone who
wants it reads it in the repository, which is where its links resolve.
