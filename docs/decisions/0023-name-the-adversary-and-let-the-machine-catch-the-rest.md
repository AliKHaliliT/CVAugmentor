# 0023. Name the adversary and let the machine catch the rest

Status: Accepted
Date: 2026-08-23

## Context

The treasury's third study catalogued the named vocabulary of software
security, 13,764 entries folded to 1,996 in eight families. Almost none of it
can become style law, and the reason is structural rather than a matter of
taste. Two entries in five end by naming what they cost, and every one of
those answers a question the entry itself cannot ask. Whether certificate
pinning is worth its price depends on who the attacker is and what breaks
when the pin is wrong. A template has no threat model, because the threat
model belongs to whatever gets built from the template. Imposing a priced
mechanism here would be this family pretending to know something it cannot
know, which the first study's disposition already refused under another name.

What survives is the part that needs no threat model. Two things qualify. The
first is that a change can name who it is defended against, or say plainly
that nobody is, and either answer is better than the silence that is the
current default. The second is the mechanical subset, the constructs that are
wrong whoever the attacker is and that a linter can see.

## Decision

The delivery gate gains **Adversary honesty** as its nineteenth item, placed
immediately before Boundary honesty so the pair reads in order, name who the
boundary is against and then check what crosses it. It asks that a change
creating or moving a trust boundary name who it withstands, and it accepts
"nobody is attacking this" as an answer, provided the answer is written rather
than assumed. The item is unconditional because knowing the adversary costs
nothing; acting on that knowledge is what costs, and the gate does not demand
the acting.

The toolchain gains ruff's `S` ruleset, the security checks
ported from bandit, which catch the constructs no threat model is needed to
judge: dynamic execution, unsafe deserialization, broken hash and cipher
choices, shell injection through the subprocess interface, disabled
certificate validation, and hardcoded temporary paths.

Everything else the study catalogued stays in the treasury as vocabulary. No
cryptographic choice, no authentication or authorization mechanism, no
isolation architecture, and no operational tooling enters this template, and
the treasury's family ruling records that refusal with the condition that
would reopen it.

## Consequences

The gate is nineteen items and stays byte-identical across the three styles.
A change that touches a trust boundary now owes one sentence it did not owe
before, and reviews will find that sentence missing more often than they find
it wrong, which is the point.

The lint additions were evaluated against this tree rather than adopted
blind. The full ruleset was run first and reported 46 findings, all of them pytest's
own assertions inside the suites. One per-file exclusion carries them and the
rule stays at full strength everywhere else. Each rule was proved against a planted defect before the
clean result was trusted, because a rule that never fires and a rule that
cannot fire look identical from a passing run.

The exclusions are narrow and each names its reason in the configuration
beside it, so a reader can see what was waived rather than finding a silent
blanket. Nothing here catches a design flaw, and nothing here is a substitute
for a threat model. The gate item is the part that scales; the linter is the
part that is free.
