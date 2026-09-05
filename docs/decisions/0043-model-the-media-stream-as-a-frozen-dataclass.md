# 0043. Model the media stream as a frozen dataclass

Status: Accepted
Date: 2026-09-05

## Context

Every domain schema in this package is a Pydantic model, which is the style's
dialect and buys validation at the door for the values that arrive from a
caller. `MediaStream` is the one schema that does not fit. It pairs a
`MediaProperties` record with the decoded frames, and those frames are a live
iterator, produced lazily so a long video never lands in memory whole.

An iterator has nothing to validate. It has no shape to check, no bounds to
enforce, and no meaningful equality. It also cannot survive being copied, and a
schema library's job is very largely copying.

## Options considered

- **A Pydantic model holding the iterator.** Pydantic v2 can be told to accept
  an arbitrary type, but the model then validates nothing about the field it
  exists to carry, and every construction pays model overhead once per medium
  in a batch. It reads as a validated schema while validating the one thing it
  holds not at all.
- **Materialise the frames into a list.** Makes the value ordinary data and
  destroys the reason for the type. A ten-minute video at thirty frames a second
  becomes eighteen thousand decoded images in memory.
- **Split the type, a validated properties model plus a bare iterator passed
  alongside.** Two parameters that must travel together and can be paired
  wrongly, which is the argument for having a record in the first place.
- **A frozen dataclass.** Pairs the two, costs nothing, and says plainly that
  this is a handle rather than a document.

## Decision

`MediaStream` is a frozen dataclass. `MediaProperties` inside it stays a
Pydantic model, because its numbers are worth checking and a codec reporting a
zero width should fail at the door.

## Consequences

The rule for this package reads: Pydantic where a value is data that arrives and
must be checked, a dataclass where a value is a handle to work in progress.
`MediaStream` is the only member of the second category today, and a second one
would want this record read before it is added.

A stream is single use, which the dataclass makes no attempt to hide. Reading a
medium twice means asking the codec twice, and that is what the runner does in
sequential mode, once per augmentation, deliberately, so each augmentation sees
the untouched medium.

Frozen buys shallow immutability only. The iterator inside can still be advanced
by whoever holds it, which is the whole point, so nothing here should be read as
a claim that a stream is a value.
