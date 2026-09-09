# 0060. Keep pdoc's own theme and stop looking for another

Status: Accepted
Date: 2026-09-09

## Context

[Decision 0059](0059-theme-the-reference-from-a-template-directory.md) answered
a request for a better-looking reference by writing a stylesheet by hand. The
owner read the result and judged it worse than the default it replaced, and
asked for a premade theme rather than one built from scratch.

That is the right instinct and it was mine that was wrong. The question this
record settles is which premade theme, and the answer turns out to be that the
only one available is the one pdoc already ships.

## Evidence

There is no premade pdoc theme to adopt. pdoc installs one template set plus a
deprecated one:

```
pdoc/templates/  ->  default/  deprecated/  resources/
default/         ->  error.html.jinja2  frame.html.jinja2
                     index.html.jinja2  module.html.jinja2
```

and the obvious published names do not exist:

```
pypi.org/pypi/pdoc-material-theme   HTTP 404
pypi.org/pypi/pdoc-theme-material   HTTP 404
pypi.org/pypi/pdoc3-theme           HTTP 404
```

Premade themes live in the Sphinx ecosystem, so Sphinx was reconsidered
properly this time. The reason 0059 ruled out mkdocstrings does not apply to
it: griffe resolves an object by walking a dotted path statically and fails on
this package's namespace packages, while Sphinx autodoc imports, and every
module imports fine.

```
import cvaugmentor.adapters                       fine
import cvaugmentor.adapters.augmentations.blur    fine
import cvaugmentor.facade.pipeline.builder        fine
```

`sphinx-apidoc --implicit-namespaces` generated 62 rst files covering the whole
tree with no hand-maintained list, and a build with furo produced 106 pages.
Sphinx rules itself out on the docstrings instead. The house `Usage` block
carries a Markdown fenced example, which reStructuredText does not parse, so
the fence survives into the page as text:

```
Usage
The radius is the standard deviation the softening approximates ...
```python
from cvaugmentor import augmentations as aug
blurred = aug.Blur(2.5).apply(frame)
```
```

The backticks and the language tag render literally and the example is neither
highlighted nor set as code. The build also emitted warnings for it on every
class carrying a `Usage` block, of the form `Inline literal start-string
without end-string`, alongside duplicate-object warnings where the facade
re-exports what a submodule also documents.

Fixing that means either wiring a Markdown parser into autodoc or rewriting
every `Usage` block into reStructuredText. The second changes the docstring
dialect, which the frozen rulebook prescribes and the exemplars carry, so it is
not a local decision to take.

## Options considered

- **Keep the hand-written stylesheet.** Refused by the owner, who read it.
- **Adopt a premade pdoc theme.** Nothing to adopt.
- **Move to Sphinx for its themes.** Refused on the evidence above. It renders
  this project's docstrings worse than pdoc does, which is a strange price to
  pay for a nicer frame around them.
- **Use the theme pdoc ships.** Chosen.

## Decision

The reference uses pdoc's own template. `util_resources/reference/` and its
stylesheet are deleted, and the build passes no template directory.

Two flags survive from 0059 because neither is a styling choice: the version as
footer text, and a per-module edit URL into the source on GitHub. The inline
source listings return, since suppressing them was also my taste rather than an
improvement and the default is what the owner preferred.

pdoc stays the generator for a reason worth stating plainly, because it is not
the one 0058 gave. pdoc treats a docstring as Markdown, which is the dialect
this project writes, and it is the only generator tried that renders the
`Usage` block correctly. That is a compatibility fact rather than a
convenience.

## Consequences

The site looks as it did when the owner approved it, and the two useful
additions stay.

Any future request to restyle it runs into the same wall, so the next person
should read this record first. The realistic paths are a stylesheet somebody
else wrote and maintains, which does not exist for pdoc today, or a generator
that parses Markdown docstrings and ships themes, which none of the three
tried does.

This is the second decision in two days to reverse itself on a documentation
site. Both reversals came from acting before measuring, 0059 on whether a
framework could read this package and this one on whether a hand-written theme
was any good. The measurement was cheap in both cases and would have been
cheaper first.
