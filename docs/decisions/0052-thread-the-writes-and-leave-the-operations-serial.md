# 0052. Thread the writes and leave the operations serial

Status: Accepted
Date: 2026-09-08

## Context

A sequential-mode pass reads one medium and writes one output per registered
augmentation, so fifteen augmentations mean one decode, fifteen operations, and
fifteen encodes. Making the operations faster was the obvious work and it was
also the wrong target.

At 1920x1080 the fifteen operations total roughly 190 ms while the fifteen
encodes total several seconds. Compression is the pass, and everything else is
rounding.

## Evidence

Encoding fourteen 1920x1080 frames to PNG, serial against a pool of eight:

```
Pillow, serial                  1572 ms
Pillow, 8 threads                442 ms     3.6x
OpenCV, serial                  2574 ms
OpenCV, 8 threads                579 ms     4.4x
```

Threads pay here because every codec releases the GIL while it compresses. The
same measurement at the wrong granularity does not pay:

```
8 images, 112 outputs, threads over the 14 writes     2988 ms    11.6x
8 images, 112 outputs, threads over the images        5421 ms     6.4x
```

Threading the outer loop is half as good, because OpenCV already runs its own
operations across eight threads and the two pools oversubscribe the machine.

## Options considered

- **Leave everything serial.** Rejected. It gives up 3.6x on the stage that
  is most of the runtime.
- **Thread the augmentations as well as the writes.** Rejected. They are 190
  ms of a multi-second pass, and threading them would put two threads on one
  augmentation instance, which several augmentations cache state inside.
- **Thread the outer walk across input media.** Rejected on the measurement
  above. It also makes progress reporting arrive out of order.
- **Thread only the per-output writes, one task per augmentation.** Chosen.

## Decision

`AugmentationRunner.run` opens one thread pool for the job and
`_apply_separately` submits one task per registered augmentation. Each task
reads the medium, applies its own augmentation, and writes its own output, so
no two threads reach the same augmentation instance and none shares a decoded
frame.

`PipelineConfig.workers` sizes the pool. `None` sizes it from the machine and
caps it at eight, and `1` skips the pool entirely, which keeps a debugging run
single-threaded and preserves the exact serial behaviour. A pipeline holding
one augmentation never builds a pool.

## Consequences

`Executor.map` preserves submission order, so the written paths stay in the
order the augmentations were registered and a caller cannot tell threads were
used by reading the result.

Each task decodes the source again, which is redundant work the serial version
also did. It is left redundant deliberately: sharing one decoded frame across
threads is only safe while every augmentation treats its input as read-only,
and that is an invariant no tool checks. Decoding is one operation against
fifteen encodes, and the extra decodes parallelise too.

An augmentation that mutates the frame it is handed now corrupts a sibling's
output rather than only its own. The shared guard cannot detect it. This is
named in the delivery gate's test-honesty item and carried in review.

A failing write surfaces when the pool's results are iterated, so sibling
tasks already submitted still run to completion. The runner's existing
skip-or-halt handling then sees one exception, exactly as before.
