# 0048. Convert every image to RGB at the codec

Status: Accepted
Date: 2026-09-05

## Context

Pillow opens a file in whatever mode it was saved as, so a PNG may arrive as
`RGBA` or `P`, a scan as `L`, and a JPEG as `RGB`. Version 1.x passed that mode
through untouched, and the fifteen augmentations disagreed about what to do with
it. `Negative` and `Grayscale` converted to RGB themselves before working.
`Cutout` wrote zeros across whatever channels it found, so on an `RGBA` image it
set alpha to zero and erased rather than blackened. `Hue` converted to `HSV`
and back to RGB, so it silently changed the mode of anything it touched.

The result was that the mode of an output depended on which augmentations ran
and in what order, and a chain of them in `singular` mode could produce a
different mode from the same set in a different order.

The video path had a related defect from the same cause. OpenCV hands out frames
in BGR order and the frames were wrapped into Pillow images without converting,
so every colour-dependent augmentation read blue as red for the whole of a video.

## Evidence

Passing a sample video through with no augmentation, before and after the
conversion was added at the codec, and comparing the first decoded frame against
the source:

```
mean absolute channel drift:            2.01
drift if the channels had been swapped: 25.66
```

The first number is mp4 re-encoding loss. The second is what the old path was
producing.

## Options considered

- **Leave the mode alone and fix each augmentation.** Fifteen places to get
  right, fifteen places to get wrong again, and it still leaves the output mode
  depending on which augmentations ran.
- **Preserve the input mode and convert around each augmentation.** Keeps alpha
  and pays a conversion per augmentation per frame, and the augmentations that
  cannot express themselves in the original mode still have to decide something.
- **Refuse any image that is not already RGB.** Uniform, and it rejects ordinary
  PNG files, which is most of what this package is pointed at.
- **Convert once, at the codec.** One place, one rule, and the augmentations
  stop asking.

## Decision

Every image is converted to RGB as it is read, in the codec, before any
augmentation sees it. The video codec converts BGR to RGB on the way in and back
on the way out, so both media kinds present the same contract.

## Consequences

An augmentation can assume RGB and none of them convert defensively any more.
The output mode is now a property of the package rather than of the augmentation
list.

Transparency is lost. An `RGBA` input is flattened on read, and the alpha channel
does not come back. That is a real cost, stated in the codec's own docstring, in
the README, and in the changelog, and it is the price of the uniform contract.
A future version wanting to keep alpha should carry it beside the frame rather
than inside the mode, because putting it back into the mode returns the package
to the situation this record describes.

The colour bug in the video path is fixed by the same decision rather than
separately, since both halves are the same question about where a conversion
belongs.
