# 0049. Write the README for the product and keep the pin in the upstream file

Status: Accepted
Date: 2026-09-09

## Context

A project built from Keel showed its README, and three of its nine sections
argued for an architecture: a philosophy about code rot and import contracts,
a domain section justifying the layers, and pillars in the template's own
words. The schema had asked for exactly that. Its Philosophy contract named
"the drift it defends against", its Domain contract "why this domain demands
the architecture", and the exemplar every child cuts from is a template whose
product is the architecture, so a product README came out as an architecture
apologia with a product name on it. The same README carried a forty-character
commit hash in its second sentence, because the schema put the alignment pin in
the attribution, and a features list that compared release figures, before and
after, in a document the rulebook says holds no history.

## Decision

The schema now splits the frame. In a project built from this template the
Philosophy states the problem its users have, for whom, and the stance the
project takes against the alternatives; the architecture's own why stays in
the map and the records. The Domain section states what about the domain is
harder than it looks and justifies no architecture. The Pillars are short in a
child, a few load-bearing decisions in a sentence each with a link into the
map. A feature states what is, never what changed since a release; a figure
may stand once with the record that measured it. The attribution is one
sentence linking the template by name, and the commit the project is aligned
to moves to the first line of `UPSTREAM.md`, `Aligned to <template> at
<commit>`, or at the host's own commit for an arrow carried inside its style's
repository; the audits hold the line, and the gate's pin item points there.
The canonical Conventions paragraph names the upstream file. The demo arrow's
README and upstream file carry the exemplar.

## Options considered

- Dropping the attribution's commit altogether was refused, because a
  re-alignment starts from it; it needed a home that is about the project's
  relationship to its style, and the upstream file is that home.
- Letting a child rewrite the section headings was refused. The stems stay
  fixed so every project reads the same way; only the contracts inside them
  now say whose why each section carries.

## Consequences

A child's README reads as a product's. The pin sits beside the entries it
governs, and a reader of the second sentence meets a name and a link rather
than a hash.
