# 0050. Match the deflate backends by output, not by level

Status: Accepted
Date: 2026-09-08

## Context

The PNG encoder deflates its filtered scanlines through whichever backend is
installed, Intel ISA-L when the `fast` extra is present and the standard
library's `zlib` otherwise. Both expose a `compress(payload, level)` call, so
passing the level straight through looks obvious.

It is wrong. The two scales are unrelated. ISA-L's levels run 0 to 3 and
zlib's run 0 to 9, and the same integer buys a different trade in each.

## Evidence

Compressing the Up-filtered scanlines of one 1920x1080 photograph:

```
stdlib zlib level 1     131 ms     2779 KiB
stdlib zlib level 6     818 ms     2355 KiB
ISA-L      level 1       23 ms     2695 KiB
ISA-L      level 2       22 ms     2655 KiB
ISA-L      level 3       32 ms     2641 KiB
```

Pillow's own encoder, which links zlib-ng, sits at 114 ms and 3559 KiB at its
level 1 and 300 ms and 2123 KiB at level 6.

ISA-L at level 2 is both smaller and roughly six times faster than zlib at
level 1, and it is smaller and five times faster than Pillow's level 1.

## Options considered

- **Pass the caller's level through to whichever backend answers.** Rejected.
  Level 6 means a 300 ms encode on zlib and a nonexistent setting on ISA-L,
  so the same code would behave unrecognisably differently per platform.
- **Always ask for level 1, the one value both scales define.** Rejected. It
  leaves 124 KiB per frame on the table for nothing, since ISA-L's level 2
  costs a millisecond less than its level 1.
- **Normalise a nine-point scale onto ISA-L's four.** Rejected. The mapping
  would be invented rather than measured, and it implies a fidelity of control
  that four settings do not have.
- **Pick each backend's own best setting for this payload and name it once.**
  Chosen.

## Decision

`core/acceleration` resolves one constant, `DEFLATE_LEVEL`, to 2 under ISA-L
and 1 under zlib, and the encoder asks for that unless a caller overrides it.
The constant is chosen so the two backends produce comparable bytes, not
comparable numbers.

## Consequences

A PNG this package writes is the same size within a few percent whichever
backend produced it, so a dataset does not change shape when a user installs
or drops the `fast` extra. The stream is a plain zlib stream either way, so
every PNG reader accepts both.

The price is a platform-dependent encode time, 22 ms against 131 ms per
1080p frame, which is the accelerator doing its job rather than a defect.

An override argument stays on `deflate` for a caller who wants smaller files
than fast ones, and it is expressed in the resolved backend's own scale. That
is a sharp edge, and it is the honest one, because no single scale spans both.
