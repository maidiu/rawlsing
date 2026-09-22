# Runtime and Nonexecution Guards

## Authoritative runtime gate

The source-backed census is authorized only when **all** of these are exact:

- OS: `Darwin`
- machine: `x86_64`
- CPython: `3.11.3`
- pyreadstat: `1.3.6`
- pyarrow: `25.0.1`

Both `02_RUN_CLOSED35_QUALIFIED_REPRESENTATION_CENSUS.sh` and `closed35_representation_census_harness.py` enforce the gate. A mismatch is a global court-integrity failure and occurs before any source opens.

The gate is intentionally not weakened for Linux, arm64, another Python patch version, another pyreadstat version, or another pyarrow version.

## Repository guard

The runner is bound to:

`agent/rabochii-premain-closed35-qualified-representation-census-harness-r1`

After source-free qualification the runner is rebound to the exact qualified code head. A later closure commit is admissible only if the qualified code head remains an ancestor and every post-qualification changed path is in the frozen documentation/guard allowlist.

No post-green mutation of the implementation, tests, source registry, governed-surface registry, or classification law is admitted.

## Source path boundary

The runner accepts only:

1. one source-acquisition/path manifest;
2. one work/output root.

The manifest joins paths to frozen `source_id` values. No basename, extension, directory, fuzzy title, or neighboring-file inference is used to identify a canonical source.

Every available file is SHA-256 checked against the frozen 35-source registry before metadata or bounded variable reads.

## Read economy

The harness does not issue a default all-cell scan.

For each available source it performs:

1. exact source SHA verification;
2. metadata-only read under the accepted decoder/config candidate;
3. raw SAV fixed-header read when applicable;
4. at most one bounded all-row read containing only that source's governed typed surfaces.

Sources with no governed typed surfaces require no data-frame row scan.

## Decoder/config boundary

The harness preserves accepted config rather than guessing:

- native SAV: no encoding override;
- exact-SHA latin1 compatibility SAV/DTA: only frozen allowlisted SHA/config pairs;
- Asian W1 BIG-5 and EVS 1981/1990 WINDOWS-1252: explicit declared-encoding **candidate** lanes, accompanied by `GENERIC_SAV_DECLARED_ENCODING_ADMISSION_GAP` because the current generic decoder does not admit them;
- WVS7: bounded selected numeric SAV lane, without decoder-derived source semantics.

No `auto`, `guess`, or fallback encoding mode is authorized.

## Semantic wall

The harness cannot infer semantics from:

- numeric equality;
- string rendering;
- labels;
- value frequencies;
- missingness;
- observed applicability;
- native-ID uniqueness;
- weight values;
- display formats;
- dictionary adjacency;
- cross-wave name equality.

Representation-candidate diagnostics are explicitly non-authoritative and cannot count as exact joins.

## Historical replay dependency wall

LiTS historical typed-key provenance is decomposed into pinned key-producing origins:

- historical facade commit/blob;
- historical canonicalize/semantic-hash blob;
- historical physical missing-state enum blob;
- current successor R5 codec/blob;
- current successor physical-key contract/blob;
- bounded LiTS representation authority.

WVS7 retains the accepted pyreadstat/ReadStat version evidence from its bounded representation authority.

An origin outside `HISTORICAL_PINNED`, `CURRENT_SUCCESSOR_PINNED`, or `PINNED_EXTERNAL_EVIDENCE_IN_AUTHORITY` is rejected as an accidental ambient current dependency leak.

## Explicit nonexecution guards

This harness contains no import or dispatch path for:

- Candidate A;
- Candidate B;
- Candidate C;
- measured P2X;
- P3;
- architecture selection.

It does not invoke the final launch scripts, oracle freeze, T3, I03 candidate execution, I05 candidate production, or measured six-cell execution.

Source-free hostile tests inspect the harness import graph and runner text for those forbidden execution paths.

## Receipt continuity

A per-source receipt is immutable after creation. On rerun, an identical receipt is resumed without re-observing the source. A receipt whose source SHA, qualified runtime, or path-manifest fingerprint differs is a global integrity failure.

Source-local measurement errors are BLOCKED receipts, not global aborts, unless they expose registry, runtime, repository, or historical-dependency corruption.
