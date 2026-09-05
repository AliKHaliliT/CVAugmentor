# 0015. Demonstrate the reasoner seam on a validatable provider

Status: Accepted
Date: 2026-08-10

## Context

The LLM adapter existed to show where a frontier model plugs into the engine, and it named Anthropic. Its own disclaimer called it a theoretical example, untested against live traffic, because validating it costs a paid API key, and STATE carried that debt from the template's first week. A demo that cannot be demonstrated teaches the seam but proves nothing about the wire.

The owner ruled the demos must really work, and offered a free-tier Gemini key for one validation call, with one condition: a single LLM demo adapter, not a gallery of providers.

## Options considered

- **Keep the Anthropic adapter and validate it.** Rejected by economics: validation needs a paid account forever, so the debt would return with every future re-validation.
- **Keep both adapters.** Rejected by the owner: one demo example, because the adapter exists to teach the seam, and two providers teach nothing the first did not.
- **Swap to Gemini and pin the wire with a recorded fixture.** Accepted.

## Decision

`GeminiReasoner` replaces `AnthropicReasoner`, same seam, same shape: a lazily imported SDK behind a `gemini` extra, credentials resolved from the environment and never read by this package, and a translator pair that speaks plain dictionaries outward and duck-typed attributes inward, so every translator test runs without the SDK installed and CI stays offline.

Validation is a one-time recording rather than a standing dependency. `scripts/record_gemini_fixture.py` makes one real call with the key arriving from the environment, serializes the response shape into `tests/fixtures/gemini-decide.json`, and a replay test pins the parser against it from then on, skipping cleanly while the recording does not yet exist. STATE carries the pending recording under Blocked until the key is handed over.

## Consequences

The demo adapter becomes provable at zero standing cost, and the suite gains cases the Anthropic adapter never had, seven translator tests plus the replay. The costs are a provider rename across the documentation, and the honest caveat that until the recording exists the adapter's wire behavior rests on the SDK's documented shapes, which is exactly the situation the fixture ends.
