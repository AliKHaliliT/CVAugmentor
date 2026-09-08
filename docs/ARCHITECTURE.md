# Architecture

This project follows a strict Hexagonal Architecture (Ports and Adapters), adapted to the shape of an installable Python package and enforcing Clean Architecture's Dependency Rule throughout. The domain holds plain data records and the pure decisions an augmentation pass makes, with every piece of IO behind a port in the spirit of the functional-core school. The core business logic (`domain` and `services`) is completely isolated from the public surface (`facade`) and the concrete implementations (`adapters`).

The rule this project buys with that separation is a hard one, that nothing under `domain` or `services` may import Pillow, OpenCV, NumPy, or ISA-L. An augmentation pass is decided there and executed nowhere else, so the orchestration reads no file, decodes no pixel, and draws no progress bar. A frame crosses the core as an opaque handle that only the adapters on either side can read, which is what lets an imaging library be swapped without the loop that walks a directory noticing ([decision 0042](decisions/0042-carry-a-frame-as-an-opaque-handle.md)). The import contracts in `pyproject.toml` check that boundary on every run rather than leaving it to memory.

Two layout conventions hold throughout the package. First, every directory contains either subpackages or modules, never a mix; the package root is the sole exception, because Python requires `__init__.py`, `__main__.py`, and the PEP 561 `py.typed` marker to live there beside the layer packages. Second, an `__init__.py` appears only where it does real work (re-exporting a subpackage's public names), so the five layer directories are bare [namespace packages](https://peps.python.org/pep-0420/) with no `__init__.py` at all. That second convention is load-bearing rather than cosmetic: the import graph the Dependency Rule contract runs over lists the layer directories as portions, and a layer directory carrying an `__init__.py` is rejected as not being a top-level module, which would silently shrink the graph to whatever the contract could still see.

A `translators/` package marks a layer boundary. In `facade/` it holds the outbound bridge that flattens domain results into the public report schemas; there is no inbound counterpart, because the facade builds domain schemas directly from the primitives its callers pass.

```text
CVAugmentor/
├── AGENTS.md                   # Agent entry point and the single documentation index
├── CHANGELOG.md                # Curated per-release summary for the package's consumers
├── pyproject.toml              # PEP 621 metadata, build backend, entry points, tool config
├── README.md                   # Project documentation and setup guide
├── STATE.md                    # Living project state (Now / Next / Deferred / Blocked)
│
├── docs/                       # Technical documentation for maintainers and agents (indexed in AGENTS.md)
│   ├── ARCHITECTURE.md         # This file; the annotated map of the package
│   ├── BASELINE.md             # The repository baseline (always-present files and their rules)
│   ├── CONVENTIONS.md          # The documentation rulebook (frozen; do not edit)
│   └── decisions/              # Immutable decision records; the project's "why" log
│
├── local_util_resources/       # Untracked development scripts, sample media, and experiment output
│
├── scripts/                    # Tracked repository tooling
│   └── audit_docs.py           # The docs audit; the gate's Docs command
│
├── src/                        # The src layout; prevents importing the uninstalled tree
│   └── cvaugmentor/            # The installable package
│       ├── __init__.py         # Curated public surface and __version__ resolution
│       ├── __main__.py         # `python -m cvaugmentor` delegation to the CLI
│       ├── py.typed            # PEP 561 marker; ships the package as typed
│       │
│       ├── facade/             # Public surface: what an embedding application imports
│       │   ├── pipeline/       # Pipeline facade + PipelineBuilder (guarded fluent construction)
│       │   ├── cli/            # Argparse CLI wired to the console script and __main__
│       │   ├── schemas/        # Frozen dataclasses for the public report payloads
│       │   └── translators/    # Flatten domain results into the public reports (outbound only)
│       │
│       ├── core/               # Package-wide infrastructure and configuration
│       │   ├── acceleration/   # Optional-backend resolution: OpenCV, ISA-L, and the fallbacks
│       │   ├── config/         # PipelineConfig (frozen dataclass; no env at import)
│       │   ├── logging/        # Package logger with NullHandler (library citizenship)
│       │   └── plugins/        # Entry-point discovery for third-party augmentations
│       │
│       ├── domain/             # Absolute source of truth: the pass's decisions and vocabulary
│       │   ├── exceptions/     # Pure Python domain-level exceptions
│       │   ├── interfaces/     # Protocols (IAugmentation, IMediaCodec, IProgressSink, IWorkspace)
│       │   └── schemas/        # Domain models (media, jobs, results)
│       │
│       ├── adapters/           # Concrete implementations of the domain interfaces
│       │   ├── augmentations/  # The catalog, one module per augmentation, over shared frame helpers
│       │   ├── media/          # Codecs: this package's own PNG path, then OpenCV or Pillow
│       │   ├── progress/       # Progress sinks (one rewritten terminal line)
│       │   └── workspace/      # Filesystem reader; listing and media-kind detection
│       │
│       └── services/           # Business logic orchestration (coordinates the ports)
│           └── execution/      # AugmentationRunner; the walk over media and augmentations
│
├── tests/                      # Automated test suite (mirrors the src structure)
│   └── src/
│       └── cvaugmentor/
│           ├── adapters/       # The catalog contract, and the workspace's ordering
│           ├── facade/         # The door checks, the builder's guards, the translator properties
│           ├── services/       # The runner's contract, with fakes at the outward ports
│           └── test_package.py # Library citizenship, pinned (logger, environment, version)
│
└── util_resources/             # Tracked repository assets
    └── readme/                 # Every image the repository embeds
```

## The shape of a pass

A pass is described by an `AugmentationJob`: two paths, a medium kind, a process type, and an application mode. The process type says whether the paths name one medium or two directories. The mode says how the augmentations combine, and the two modes are the package's central distinction. In `singular` mode every augmentation is chained onto the same medium and one output is written. In `sequential` mode each augmentation is applied to the untouched medium and written on its own, under the label it was registered with; that label is what names the file, which is why registering the same augmentation twice needs an explicit label.

A frame crosses the ports as an opaque handle, and every adapter this package ships agrees that the handle is a contiguous HxWx3 `uint8` array in RGB order ([decision 0049](decisions/0049-carry-a-frame-as-an-rgb-array.md)). The agreement is the adapters' own; the annotation in `domain` stays `Any`, which is what keeps the import contract satisfiable. `adapters/augmentations/frames.py` holds the one guard that checks it and the helpers every augmentation shares.

Speed is bought in two places and nowhere else. Each operation asks `core/acceleration` for OpenCV and takes a NumPy path when it answers `None`, so a platform with no OpenCV wheel keeps every format and loses only time ([decision 0053](decisions/0053-declare-the-accelerators-optional-and-fall-back-in-code.md)). And the runner threads the per-output writes, because compression is most of a pass and every codec here releases the GIL while it runs ([decision 0052](decisions/0052-thread-the-writes-and-leave-the-operations-serial.md)). The operations themselves stay serial.

Randomness is drawn once per instance rather than once per frame, so a value left unspecified is fixed when the augmentation is constructed and every frame of a video receives the same treatment. `reseed()` is what redraws it, and the runner calls it between batch items only when the configuration asks. Where an effect must be placed on a frame whose size is not known until it arrives, the instance holds a seed instead of the value, and the placement is derived from that seed on every frame.

## Testing

Three rules hold however broad the suite is. Suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by a hand-written fake satisfying the port in `domain/interfaces` that it stands in for, never by patching a module's internals, since a test bound to an implementation voids the substitutability the ports exist to provide. And no coverage threshold is imposed, because a percentage gate buys assertions that assert nothing, so breadth stays a judgment call while placement and substitution do not.

`tests/src/cvaugmentor/services/test_augmentation_runner.py` is the worked example. All four outward ports are stood in for, because all four reach a file, a codec, or a terminal in production, and the fakes carry plain strings where production carries pixels, which is the opaque-frame rule paying for itself in the suite. It pins the runner's contract rather than its internals: the two modes write what they promise, a batch entry of the wrong kind is recorded rather than read, an unreadable medium becomes data unless the configuration says to halt, a single-file run always raises instead, redrawing happens between batch items only when asked, and every progress unit names one item.

`tests/src/cvaugmentor/facade/translators/test_domain_to_facade.py` is the worked example of the property shape. It states the translator's invariant, that nothing is lost or invented crossing the boundary, over generated outcomes rather than hand-picked ones, and every property runs derandomized with no example database so the suite reproduces on every run. A green property test claims no counterexample in its generated cases, never a proof.

`tests/src/cvaugmentor/adapters/augmentations/test_catalog.py` covers the catalog as one unit, because all fifteen augmentations answer one contract and fifteen near-identical suites would say the same thing fifteen times. It reads the catalog off the package door, so an augmentation that ships is covered the moment it lands.

## Exemplars

The map says where things live; these files say how they read. An artifact of a kind listed here is cut from its exemplar and rewritten, never written fresh from the rule, because the rule names what must exist and only these bytes carry the dialect.

- A guarded builder class with a `Usage` block: `src/cvaugmentor/facade/pipeline/builder.py`.
- An outbound translator: `src/cvaugmentor/facade/translators/domain_to_facade.py`.
- An augmentation behind its port: `src/cvaugmentor/adapters/augmentations/blur.py`.
- An adapter wrapping an SDK: `src/cvaugmentor/adapters/media/video_codec.py`.
- A domain schema: `src/cvaugmentor/domain/schemas/results.py`.
- An operation with an accelerated path and a NumPy fallback: `src/cvaugmentor/adapters/augmentations/frames.py`.
- A suite with hand-written fakes at every outward port: `tests/src/cvaugmentor/services/test_augmentation_runner.py`.
- A property suite over a stated invariant: `tests/src/cvaugmentor/facade/translators/test_domain_to_facade.py`.
