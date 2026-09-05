# 0025. Let a check imply no more than it decides

Status: Accepted
Date: 2026-08-24

## Context

While settling how a returned value is named, the question arose of whether to
enforce the new rule with a linter. Part of it is decidable, since a name that
merely echoes its own type is a pattern a tool can match. The larger part is
not, because no tool can decide whether a type carries its own meaning.

The owner's first formulation was that a rule is checked completely or not at
all, and the instinct behind it is right. A check that covers part of its rule
reports a clean run while never examining the question the rule is about, and a
clean run is read as enforcement. The unchecked part then rots behind a green
light, which is worse than rotting in the open, because nobody is looking.

Held against the family's actual checks, the strict form proved too strong in
four ways. It discards a sound net, since a scanner with misses but no
meaningful false alarms still licenses the inference that a finding is real.
The word completely does unexamined work, since no type checker fully decides
type safety and no suite fully decides correctness, and every check here
survives only because its question is narrowed until it is decidable. The harm
lives in the reader's belief rather than in the tool, so it can be cured by
fixing what a check claims instead of removing the check. And it prices no
consequence, though a credential in public history is the one failure here a
later commit cannot undo.

The family had also already solved this once without naming it. The test rule
imposes no coverage threshold, so breadth is a judgment call while placement
and substitution are law. That is the same idea, stated for one case.

## Decision

A check may never imply more than it decides.

Three obligations follow. A check is named for the question it actually
settles, so a green run claims only that. A check that cannot settle its
question advises rather than gates. Whatever a check leaves undecided is
stated beside the rule as review's work, never left to look automated.

This creates two tiers, and the agent guide now states both. A failure is a
verdict from a check that fully decides its question. A warning is advice from
a check that cannot, and it is not optional reading. Every warning is looked at
and then fixed or dismissed in writing in the change that produced it, and no
warning is silenced with a suppression to make a run look clean. The delivery
gate's commands item carries that obligation so it cannot be skipped quietly.

## Consequences

An audit against the new rule found six checks in the family that could pass
while the thing they were named for was broken. None was deleted, because
under this rule none needed to be.

Two credential heuristics, S105 and S106, left the gating selection and return as
advice through a dedicated command and a continue-on-error step in the pipeline.
They read any suggestive string as a possible secret, so they cannot gate. The
advisory run currently reports nothing in this repository.

Two job names were wrong rather than the checks beneath them. The job that
greps one character was called Prose while the prose rules also ban the
clause-colon splice and stacked tells, which no tool judges; it is now named
for em dashes. The job running the secret scanner was called Secrets; it is now
named as a scan, and it still gates, because the question it settles is whether
anything matches its pattern set and that question is worth gating on. Whether
a confidential fact reached a tracked byte is the hard rule's question, no
scanner decides it, and review carries it.

The family gains no check from this and loses none. What changes is that a
passing run now means what it says.
