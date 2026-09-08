# 0051. Vectorise the PNG filters that are not recurrences

Status: Accepted
Date: 2026-09-08

## Context

PNG stores each scanline under one of five row filters, and decoding means
inverting whichever the encoder chose. The obvious reading is that all five are
sequential, since each predicts a byte from its neighbours, and that a
vectorised decoder is therefore impossible.

That reading is wrong for three of the five, and the difference decides whether
this package can own its own PNG path or has to hand every file to a library.

## Evidence

Inverting each filter over one 1920x1080 frame, NumPy against a per-pixel
Python loop:

```
Sub, whole image in one np.cumsum         12.4 ms   exact
Up,  whole image in one np.cumsum        108.7 ms   exact
Paeth, per pixel                        2317.0 ms   exact
Paeth, per pixel through NumPy          29.5 ms per ROW, so ~32 s per frame
```

Pillow decodes the same frame in roughly 74 ms, and Sub therefore inverts
faster than any library decodes.

The reason splits cleanly. Sub predicts from the pixel to the left, so its rows
never depend on each other and the whole image is one cumulative sum along x.
Up predicts from the row above, so its columns never depend on each other and
the image is one cumulative sum along y. None copies. Average and Paeth each
need a finished neighbour on both axes at once, which is a genuine
two-million-step recurrence that no array library reaches, and routing it
through NumPy per pixel is far worse than plain Python because the per-call
overhead dwarfs the work.

## Options considered

- **Write a full PNG decoder covering all five filters.** Rejected. Paeth
  would cost 2.3 s per frame against a library's 74 ms, and correctness is not
  the problem, so the effort buys a slower decoder.
- **Hand every PNG to OpenCV or Pillow.** Rejected. It gives up a decode that
  beats both of them on the files this package writes, and encoding is where a
  sequential-mode pass spends its time.
- **Cover the vectorisable filters and delegate the rest.** Chosen.

## Decision

`adapters/media/png.py` decodes eight-bit truecolour, non-interlaced PNGs whose
scanlines all carry the same filter and whose filter is None, Sub, or Up. Each
of those inverts in exactly one vectorised call. Anything else returns `None`,
which the codec reads as an instruction to hand the bytes to OpenCV or Pillow
rather than to guess.

Encoding always writes the Up filter, which one vectorised subtract produces.

## Consequences

A PNG this package wrote reads back through its own fast path. A PNG from
anywhere else usually does not, because adaptive encoders choose Paeth for
photographs, and those files take the general path at library speed. That is
the right asymmetry, since a pass reads each input once and writes many
outputs.

The declining branch is a silent fallback, so a malformed file and an
unsupported one look the same from inside `png.decode`. The codec reports the
failure, because it is the layer that knows whether a general decoder was
available to try.

Average is left unimplemented even though it is only half a recurrence. No
encoder this package has met chooses it often enough to measure, and an
untested branch is worse than an absent one.
