# C05-R2A — SOURCE-BACKED C11 / I03 FACADE IMPLEMENTATION

Exact start HEAD: `d16d988ea51e02482e9f6887fa8ecdcde3c7eb66`

Disposition: `C05R2A_PASS__GENERIC_FACADE_PROVED__NAMED_REAL_SOURCE_INSTANCE_AUTHORITY_PENDING`

## Implementation

Added:

- `rawlsing_next/pre553_source_backed_c11_facade.py`
- `rawlsing_next/tests/test_pre553_source_backed_c11_facade.py`

No frozen I03/I05 truth condition, C11 semantic object definition, decoder semantic, R5 storage semantic, V553-V2 semantic, or production selector was modified.

The implementation is carrier-neutral at the semantic boundary. It accepts either:

1. exact `PhysicalSourceIncidence` plus its physical-cell stream; or
2. an `ExactPhysicalCellStream` carrying the same immutable source SHA, row count, and exact physical cells.

Native incidence delegates through the already-governed `PhysicalSourceAuthorityProjection` bridge. Replay-equivalent cell transport uses the same explicit governed candidate builder. Both paths converge on the same mandatory construction path:

`physical/native incidence -> explicit GovernedC11Projection -> C11SourceReleaseCandidate -> validate_c11_source_release() -> C11LogicalRelease -> C11Repository -> frozen I03`

There is no direct construction of `C11LogicalRelease` and no bypass or mutation of `_C11_VALIDATION_SEAL`.

## Explicit governed inputs

`GovernedC11Projection` carries exact immutable material for:

- source/release identity and source SHA;
- row-to-respondent replay coordinates;
- native physical slot ordinal/name identity;
- native/canonical question/component bindings where authorized;
- explicit physical-value to typed response-state/value bindings;
- explicit zero/one/many occurrence rules, event-group/event-index determinants, topology, multiplicity, order/rank/repetition;
- routing/applicability/risk-set facts independent of response missingness;
- coordinate identity/value authority;
- weight/design/estimand authority;
- source-universe relation or explicit distinct-by-default state;
- immutable authority snapshots and required authority closure;
- replay protocol, tie-order, source-retention, and provenance determinants.

Missing bindings fail closed. The implementation does not infer semantic meaning from variable names, label text, observed frequencies, missingness frequencies, carrier ordering, or convenience heuristics.

## Determinism and transport parity

The proving fixture was independently materialized as logical C11 and also projected through the source-backed facade. The two routes produced the exact same:

- `C11LogicalRelease` ref/content hash;
- `ReplayManifest` ref/content hash;
- public object refs;
- internal record refs;
- frozen-I03 `EmpiricalFact` ref/content hash and result content.

A replay-equivalent physical-cell stream with reversed carrier order produced the same semantic release and replay identities as native incidence.

## Cache / persistence law

`SourceBackedC11SessionCache` is optional and nonauthoritative. Cache deletion changes recomputation cost only. Mismatched/tampered cache identity fails closed. Exact recomputation from source + governed projection reproduces the same release identity.

Permanent persistence of a full semantic event payload is therefore **not required by this implementation proof**. A transient exact projection can construct a validated logical release from exact source cells plus governed semantic/replay authority. This does not decide the final physical architecture or forbid any later lawful cache/storage choice.

## Execution proof

Focused facade/parity/hostile suite:

`10 passed, 0 failed, 0 skipped`

Supplemental frozen-I03 regression probes over the same exact dependency slice:

`5 passed, 0 failed, 0 skipped`

Python syntax compilation of both additive files: PASS.

No semantic inference was necessary.

No real-source WVS7 execution was performed. The generic implementation contract is proved; exact WVS7 source-specific semantic projection/source-certification authority remains pending.
