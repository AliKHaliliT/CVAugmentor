# 0002. Document only directly raised exceptions in Raises

Status: Accepted
Date: 2026-07-16

## Context

The docstring convention requires a `Raises` section on every fully documented function, but the NumPy style does not settle which exceptions belong in it: only those raised by the function's own body, or also those that propagate out of the methods it calls. Propagated exceptions made the section unstable. Whether `EngineBuilder.build` raises `DuplicateToolError` is a fact about the registry it calls, not about `build` itself, and any change inside a callee could silently invalidate every caller's docstring above it.

## Options considered

- **Document every exception that can escape the function.** Rejected: the set of escaping exceptions is a property of the entire call tree, so it cannot be verified by reading the function, and it rots as callees change.
- **Document only exceptions raised by a literal `raise` statement in the function's own body.** Accepted: "is there a raise statement here?" is the only boundary a reader or an agent can check locally and decide unambiguously.

## Decision

`Raises` lists exactly the exceptions raised directly in the function's body, including the defensive argument-validation guards. An exception that merely propagates from a called method is documented on the method that raises it, not on the caller. An exception that is raised and caught within the same function is not listed. When nothing is raised directly, the section carries the `None.` sentinel.

## Consequences

Each exception is documented exactly once, at the site that raises it, and any docstring can be verified against its own function body without reading the call tree, which keeps the section stable as internals evolve. The cost is that a caller's docstring does not enumerate every failure mode that can reach it; a reader tracing failure modes follows the call chain, starting from the facade docstrings, which are documented in full.
