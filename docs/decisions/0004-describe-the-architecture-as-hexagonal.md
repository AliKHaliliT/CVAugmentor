# 0004. Describe the architecture as Hexagonal rather than DDD

Status: Accepted
Date: 2026-08-01

## Context

The README and ARCHITECTURE.md described Keel as Domain-Driven Design plus Clean Architecture, wording inherited from ArchetypeCore's self-description when Keel was generated "in the caliber of" its sibling. A paradigm review found that the code does not practice DDD. There are no aggregates, no entities guarding invariants, no ubiquitous-language modeling, and no bounded contexts; the domain layer holds plain Pydantic records coordinated by a procedural orchestrator, which the DDD literature names the anemic domain model and treats as an anti-pattern. What the code does practice, almost textbook, is Ports and Adapters. The Protocols in `domain/interfaces` are the ports, `adapters/` holds the driven side, `facade/` is the driving side, and `AgentRunner` touches nothing concrete.

## Options considered

- **Keep the DDD label for symmetry with ArchetypeCore.** Rejected: a label the code does not practice misleads both readers and agents, and an agent told the project is DDD may start growing aggregates and entity hierarchies the design deliberately avoids.
- **Introduce real DDD machinery so the label becomes true.** Rejected: the engine's domain, which amounts to a loop, a step budget, and a trace, carries no invariant complexity that would pay for aggregates; DDD earns its cost only where business rules are rich.
- **Rename the documentation to what the code practices.** Accepted: honesty in the map costs nothing and steers future generation correctly.

## Decision

The documentation describes Keel as Hexagonal Architecture (Ports and Adapters) enforcing Clean Architecture's Dependency Rule, with functional-core discipline, meaning plain data records, pure decision logic, and every piece of IO behind a port. ArchetypeCore keeps its DDD label, because a server domain with users, quotas, and device lifecycles is the kind of domain that justifies it.

## Consequences

The two sibling templates now intentionally differ in their stated paradigm, and this record is the place that explains why, so the difference is not mistaken for drift. Projects derived from Keel inherit the hexagonal wording and should not reintroduce DDD vocabulary unless their domain actually develops the invariant complexity that warrants it, in which case a new decision record supersedes this one for that project.
