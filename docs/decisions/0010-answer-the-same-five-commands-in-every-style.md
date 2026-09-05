# 0010. Answer the same five commands in every style

Status: Accepted
Date: 2026-08-05

## Context

The styles are meant to differ in form and agree in contract, so a person or an agent arriving at any of them should find the same questions answered. Comparing the `## Commands` blocks showed they did not agree. This template and the client template both listed Lint and Type-check; the server template listed neither, because it had nowhere to configure or install them. The blocks also ordered the same verbs differently, which is a small thing that makes comparing the styles harder than it needs to be.

A second gap was larger and applied here too. None of the three styles had any continuous integration. Every rule in the family was therefore checked when somebody remembered to type a command, which is not the same as being checked. That undercuts the family's own stated preference for machine-checked rules over reviewed ones.

## Options considered

- **Leave each block shaped by what its language happens to offer.** Rejected: the differences then read as choices rather than as consequences of the language, and a reader cannot tell which is which.
- **Unify the tools rather than the contract.** Rejected: ruff is not ESLint and pytest is not vitest. Only the contract can be shared, and pretending otherwise would force a worse tool on one of the styles.
- **Fix the five verbs and their order, and run them in CI.** Accepted.

## Decision

The five commands are Install, Run, Test, Lint, and Type-check, in that order, in every style. Commands beyond the five are listed after them rather than in place of them.

The type checker now covers the suites as well as the package, matching what the client template already did through its `tsconfig` includes. It passes under the same strict settings with no suppressions.

Each style runs the five commands in continuous integration on push and on pull request. The workflow installs, then lints, type-checks, and tests, so a rule that a config file claims to enforce is actually enforced.

## Consequences

The styles now agree on what a project must be able to answer, and where the answers differ the difference is attributable to the language rather than to an omission.

Enforcement stops depending on memory. That matters most for the rules this family has deliberately pushed into tooling, since a checked rule that nothing runs is a reviewed rule with extra steps.

The cost is a workflow file in each style and a slower feedback loop on pull requests. Both are small, and neither adds a dependency to the package itself.
