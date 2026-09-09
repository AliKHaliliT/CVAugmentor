# 0061. Publish on a version tag through trusted publishing

Status: Accepted
Date: 2026-09-09

## Context

The API reference rebuilds on every push to the default branch, and the owner
asked for releases to be automatic in the same way. Taken literally that does
not work, and the reason is worth writing down rather than discovering on a
second release.

A package index refuses a version it already holds. A publish triggered by a
push would upload once and then fail on every subsequent push, because the
version in `pyproject.toml` has not moved. Worse, the failure would be
indistinguishable from a real problem, so a pipeline that is red by design
teaches everyone to ignore it.

What the request actually asks for is that no human runs `twine` and no
credential sits on anyone's machine. Both are achievable on the right trigger.

## Options considered

- **Publish on every push to the default branch.** Refused for the reason
  above. It works exactly once.
- **Publish on a push whose commit changed the version.** Refused. It reads the
  diff to infer intent, so a version bump merged with other work publishes as a
  side effect, and a revert publishes nothing while looking like it should.
- **Publish on a GitHub release.** Close, and it puts the trigger in a web form
  rather than in the repository, so the tag and the release can disagree about
  which commit shipped.
- **Publish on a version tag.** Chosen. A tag is a deliberate act, it names one
  commit, and it lives in the repository where the history keeps it.

## Decision

A tag matching `v*` runs three jobs in order, and nothing uploads until the
earlier two pass.

The first re-runs the gate against the tagged tree, because a release built
from a red commit is the one release that must not exist. It also checks that
the tag agrees with the version the project declares, which is the cheapest
guard available and the only one that matters, since an index entry cannot be
withdrawn. A tag of `v2.0.1` against a declared `2.0.0` fails before anything
is built.

The second builds both artifacts, runs `twine check`, and installs the wheel
into a scratch environment to import it, because an editable install never
exercises packaging and a broken build configuration would otherwise reach the
index unnoticed.

The third uploads through OpenID Connect rather than an API token. It asks for
an `id-token`, runs in its own `pypi` environment, and stores no secret
anywhere.

## Consequences

Releasing is two commands, a tag and a push, and the rest is mechanical. No
credential exists to leak or rotate.

Publishing needs a trusted publisher configured once on the index side, naming
this repository, the workflow file, and the environment. Until that exists the
upload job fails while the gate and build jobs pass, which is legible rather
than mysterious. STATE.md carries it as blocked.

A mistyped tag fails loudly and costs nothing. A tag on a commit that does not
pass the gate fails before building. Neither can reach the index, which is the
property worth having, because the index is the one place in this project where
a mistake is permanent.

The gate now runs twice for a release, once on the push and once on the tag.
That is deliberate duplication: the tag may point at a commit whose earlier run
is old, and a check that has not been run against the exact tree being shipped
is not a check.
