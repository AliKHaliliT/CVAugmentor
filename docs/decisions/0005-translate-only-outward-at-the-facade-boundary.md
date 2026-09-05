# 0005. Translate only outward at the facade boundary

Status: Accepted
Date: 2026-08-01

## Context

Keel inherited its boundary discipline from ArchetypeCore, where the API layer owns a wire contract and every request is translated from an API schema into a domain schema. Transplanted into a package, that produced a `RunRequest` facade schema that mirrored the domain's `RunSpec` field for field, a one-line inbound translator that unpacked one into the other, and OpenAPI example configuration that no Swagger page would ever render, since a library has no HTTP surface. The caller of `Engine.run` already passes plain Python arguments, so the facade was wrapping primitives into a schema only to immediately unwrap them. The outbound direction is different in kind, because the reports genuinely reshape the domain, flattening the `ToolCall | Finish` action union into a stable record consumers can consume without matching on domain types.

## Options considered

- **Keep the inbound mirror schema for symmetry with ArchetypeCore.** Rejected: a server's request schema exists because the wire contract validates, versions, and documents independently of the domain; a package has no wire, so the mirror duplicates a domain schema without ever diverging from it and rots as pure ceremony.
- **Drop facade schemas entirely and return domain objects.** Rejected: that leaks the domain's action union to every consumer and couples the public surface to internal representations, which is the drift the template exists to prevent.
- **Translate outward only, with facade schemas existing only where the public shape differs from the domain shape.** Accepted: the boundary keeps its protective value on the side where representations actually diverge and sheds the ceremony on the side where they never did.

## Decision

The facade translates in one direction. `Engine.run` builds the domain `RunSpec` directly from the primitives its caller passes, and `facade/schemas` holds only the report types, which the outbound translators produce from domain results. A facade schema is added only when the public shape must differ from the domain shape; a schema that would mirror a domain schema field for field is not written.

## Consequences

The `RunRequest` schema, its `keel.RunRequest` export, and the inbound translator module are gone, which is a visible removal for any consumer who imported the name, so the change is recorded in the CHANGELOG. The rule generalizes for derived packages, since inbound wrapping becomes justified again the moment the public input shape diverges from the domain's, for example when a public argument needs renaming, defaulting, or validation the domain schema should not carry; at that point the mirror stops being a mirror and earns its translator back.
