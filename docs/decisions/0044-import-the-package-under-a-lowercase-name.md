# 0044. Import the package under a lowercase name

Status: Accepted
Date: 2026-09-05

## Context

Version 1.x installed as `CVAugmentor` and was imported as `CVAugmentor`. PEP 8
asks that module and package names be all lowercase. The 2.0 rewrite moved every
file in the tree anyway, so the cost of changing the import name would never be
lower than it was here.

The style's continuous integration also settles the question in one direction it
does not state outright. Its packaging step installs the built wheel into a
scratch environment and imports the name from the project's own metadata:

```
python -c "import importlib, tomllib; importlib.import_module(tomllib.load(open('pyproject.toml','rb'))['project']['name'])"
```

That step passes only where the distribution name and the import name are the
same string. Keeping `CVAugmentor` as the distribution name while importing
`cvaugmentor` would fail on any case-sensitive filesystem, which is every
runner the workflow uses.

## Options considered

- **Keep `CVAugmentor` for both.** No break for existing users, and a package
  name against PEP 8 that also disagrees with the style's own exemplar.
- **Distribution `CVAugmentor`, import `cvaugmentor`.** The common arrangement
  in the wider ecosystem, and the one the packaging check refuses.
- **Lowercase for both.** Costs every 1.x import statement.
- **Lowercase for both, plus a shim package re-exporting under the old name.**
  Softens the break and leaves a second name for the same thing indefinitely,
  which the style's own rule against forwarding files argues against.

## Decision

Both names are `cvaugmentor`. No shim is shipped.

## Consequences

`pip install CVAugmentor` still works and still resolves to this project,
because PyPI matches project names case insensitively and treats the two spellings
as one. What changes is the import line, and CHANGELOG.md leads with it.

Every 1.x program breaks at its import, loudly and on the first line, which is
the failure mode to prefer over a shim that lets a program keep running under a
name the project no longer maintains. The major version bump is what carries
this, and it is the reason the release is 2.0.0 rather than 1.2.0.

The `Augmentations` namespace moved with it and is now `augmentations`, reached
as `from cvaugmentor import augmentations as aug`, so the old idiom survives the
rename with only its case changed.
