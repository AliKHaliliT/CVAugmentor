# 0059. Theme the reference from a template directory

Status: Accepted
Date: 2026-09-09

## Context

[Decision 0058](0058-publish-the-api-reference-from-main-with-pdoc.md) brought
the API reference back with pdoc and counted having no configuration file among
its reasons. The published site works and reads as the tool's default, and the
owner asked for a better one.

That reopens the generator question, because a nicer theme is the usual reason
to reach for a documentation framework rather than a reference tool. 0058
refused MkDocs with mkdocstrings on the grounds that its source directory would
be `docs/`, which is an argument about tidiness. This time the tool was
installed and run, and the answer turned out to be structural.

## Evidence

mkdocstrings resolves a documented object by walking its dotted path through
each parent, which fails on the first layer directory:

```
griffe.GriffeLoader(search_paths=["src"]).load("cvaugmentor")
  -> Module, members: AugmentationException, PipelineConfig, augmentations, ...

load("cvaugmentor.adapters")                            KeyError: 'adapters'
load("cvaugmentor.adapters.augmentations")              KeyError: 'adapters'
load("cvaugmentor.adapters.augmentations.blur")         KeyError: 'adapters'
```

A build over the same tree stops on it:

```
ERROR - mkdocstrings: cvaugmentor.adapters.augmentations.blur.Blur could not be found
ERROR - Could not collect 'cvaugmentor.adapters.augmentations.blur.Blur'
Aborted with a BuildError!
```

The cause is that the five layer directories are deliberately namespace
packages with no `__init__.py`. Two workarounds were tried. Pointing the search
path deeper reaches the module and renames it, `augmentations.blur` rather than
`cvaugmentor.adapters.augmentations.blur`, so every documented name would be
wrong. Loading by file path fails outright with `KeyError: 'blur'`.

The remaining workaround is to give the layer directories an `__init__.py`, and
the map forbids it for a reason that has nothing to do with documentation: the
import graph the Dependency Rule contract runs over lists those directories as
portions, and one carrying an `__init__.py` is rejected as not being a
top-level module, which would silently shrink the graph to whatever the
contract could still see. Documenting the package that way would quietly stop
the architecture from being enforced.

Material for MkDocs also printed a warning of its own during the probe, that
MkDocs 2.0 will remove the plugin system with no migration path, which is worth
recording but was not the deciding factor.

pdoc's own customization surface was read from its templates rather than
assumed. Styling through its Jinja `style` blocks is deprecated in favour of a
`custom.css` in the template directory, and the generated markup gives real
selectors to aim at: every docstring section arrives as an `h6` whose id is
`usage`, `parameters`, `returns`, or `raises`, and every parameter list as a
`ul` of `li` holding a `strong` name and a parenthesised type.

## Options considered

- **Switch to MkDocs with mkdocstrings.** Refused on the evidence above. It
  cannot name this package's modules correctly without a change that disables
  the Dependency Rule check.
- **Override pdoc's Jinja style blocks.** Refused because pdoc deprecates them
  and says so in the template itself.
- **Restyle through a `custom.css` in a template directory.** Chosen.

## Decision

The reference carries a theme, `util_resources/reference/custom.css`, which
pdoc picks up as the tool's supported extension point. It appends to pdoc's own
sheet rather than replacing it, so an upgrade changes the layout underneath and
never leaves the page unstyled.

The sheet does four things and stops. It sets a palette that answers
`prefers-color-scheme`. It gives the section labels a size and a rule, since
every docstring here carries three or four of them and `h6` renders as an
afterthought by default. It turns parameter lists into indented definitions
with the name in monospace, because a bullet buries the name a reader is
scanning for. And it marks the hovered or linked member, which is what makes a
long page navigable.

The published build also passes the version as footer text and an edit URL per
module, and drops the inline source listings. The listings tripled a page,
42 KB against 108 KB, and the edit links reach the same code on GitHub with its
history and blame, which is the better copy to send a reader to.

This changes one sentence of 0058, which counted the absence of a
configuration file among pdoc's merits. The tree now carries one stylesheet.
Everything else that decision settled still holds: one branch, one command, no
generated output committed anywhere.

## Consequences

The reference reads as this project's rather than as pdoc's default, and the
cost is one CSS file with no build step of its own.

The stylesheet is coupled to markup pdoc generates. A pdoc release that renames
a class or stops emitting `h6` section headings leaves rules that match
nothing, which degrades to the default theme rather than breaking the page.
That is the failure mode worth having, and it is why nothing here overrides
layout.

`util_resources/` gains a purpose-named subfolder, which the baseline permits
as new asset kinds arise, so no new room is needed at the root.

The mkdocstrings finding is worth more than this decision. Any tool that
resolves modules by walking dotted paths will fail on this package, and the
next person reaching for one should read this record before installing it.
