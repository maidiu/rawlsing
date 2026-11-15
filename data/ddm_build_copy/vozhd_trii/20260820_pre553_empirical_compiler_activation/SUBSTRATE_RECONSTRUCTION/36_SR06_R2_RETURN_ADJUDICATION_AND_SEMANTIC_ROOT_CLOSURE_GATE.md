# SR06 — R2 RETURN ADJUDICATION AND SEMANTIC ROOT CLOSURE GATE

Status: `R2_RETURNED__NOT_ACCEPTED__SEMANTIC_ROOT_CLOSURE_REQUIRED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

SR06 implementation branch: `agent/vozhd-trii-sr06-c11-parquet-duckdb`

Accepted-as-progress R2 return: `fc74879bdc3a1d987e3f19022116ac551da582e6`

Prior authority: `35_SR06_CORRECTION_RETURN_ADJUDICATION_AND_R2_GATE.md`

## 1. R2 return adjudication

HQ accepts the R2 return as substantial implementation progress.

Static inspection confirms the R2 patch is exactly one commit ahead of `250f43bfdf1432d60ea5c53b95a22a67a0160ae3` and modifies only the five authorized SR06 files.

The following R2 burdens are materially closed:

- reader-native Stata extended-missing tokens `a`-`z` are recognized as `FORMAT_EXTENDED_MISSING` and preserve both reader token and source-native `.a`-`.z` notation;
- default SAV/DTA execution uses metadata-first chunk reads, while exact compatibility-allowlisted sources retain the bounded full-read exception;
- `reopen(...)` validates selector syntax, source/release/semantic identity equality and canonical path binding;
- direct DuckDB execution uses `VerifiedDuckDBSession` and no longer calls full logical `reopen()` or relation-object reconstruction before analytical queries;
- the physical-to-I02 bridge requires exact `AuthorityRef` values, exact physical/candidate source SHA equality, packaged/declared authority closure and then invokes existing `validate_c11_source_release()`;
- no persistent DuckDB/PostgreSQL/SQLite/DATABASE_URL empirical authority path is introduced.

The worker reports:

- SR06/R2 tests: `12 passed, 1 documented skip`;
- full PRE553 suite: `611 passed, 2 unchanged baseline failures, 1 skip`;
- no WVS7, LiTS-I or CLOSED_35 execution;
- required R2 return token present.

The pyreadstat extended-missing writer/readback skip is accepted as a dependency limitation because the reader-native `a`-`z` classification path is directly tested and the known LiTS-I proving source contains no observed `.a`-`.z` values. This does not remove the general decoder requirement.

G-SR06 nevertheless remains open because one content-addressed integrity invariant is not yet independently enforced.

## 2. Final blocker — semantic release hash is not recomputed from canonical relation identity root

Existing I02 defines the sealed release semantic hash deterministically as:

```python
semantic_hash({
    "candidate_projection_hash": replay_manifest.semantic_projection_hash,
    "replay_manifest_ref": replay_manifest.ref.as_dict(),
    "m01_m18": {k: list(v) for k, v in coverage.items()},
})
```

The R2 carrier reconstructs `C11LogicalRelease`, but `semantic_release_hash` is supplied directly from `release_identity.parquet` into `_make_validated_release(...)`.

It then compares that supplied value to the caller selector and manifest release-ref content hash. Those values can all agree while still being a stale/false claim about a different self-consistent canonical relation set.

Likewise, `VerifiedDuckDBSession` verifies manifest/member byte identity and selector equality but does not independently verify the I02 semantic release root from the persisted replay-manifest identity + M01-M18 coverage.

The current hostile tests do not close this stronger case:

- selector R2 test changes the claimed release identity and proves old selectors reject it;
- relation mutation test changes a semantic field while leaving its stored object identity stale, so object reconstruction detects the mismatch.

Neither test constructs a fully rehashed/replayed alternate canonical relation set while retaining the old claimed release semantic hash.

Disposition:

`BLOCKED_CANONICAL_RELATIONS_NOT_INDEPENDENTLY_ROOTED_TO_SEMANTIC_RELEASE_HASH`

## 3. Required final correction

This is a narrow identity-root correction only. Do not redesign decoder, relations, I02, M01-M18, query semantics, or carrier selection.

### A. One shared release-root verifier

Implement one shared helper used by both full `reopen()` and `VerifiedDuckDBSession` that independently derives the expected sealed release semantic hash under the exact existing I02 formula.

Inputs must come from canonical persisted relations, not from the claimed semantic hash itself:

- replay-manifest canonical row -> reconstructed/verified `ReplayManifest` exact ref and `semantic_projection_hash`;
- release-identity canonical row -> M01-M18 coverage;
- exact I02 formula above.

The helper must prove:

`derived_semantic_release_hash == release_identity.semantic_release_hash == manifest.release_ref.content_hash == supplied semantic_hash`

and fail closed otherwise.

The helper must also prove the canonical release-identity row agrees with supplied/manifest:

- source artifact hash;
- release id;
- semantic hash.

### B. Replay-manifest row identity must itself be verified

Do not trust the stored replay-manifest `object_id` / `content_hash` columns as opaque claims.

Reconstruct or otherwise deterministically verify the single persisted replay-manifest row against existing `ReplayManifest` content-hash/ref law before using its ref in release-root derivation.

This is a tiny one-row verification and is permitted in the lightweight direct session. It must not reconstruct the full object universe.

### C. Full reopen relation-closure check

When full `reopen()` reconstructs the canonical object universe, verify that every persisted non-replay public/internal C11 object ref is represented in the replay manifest closure expected by the accepted I02 replay law, together with the exact source artifact ref.

Do not silently permit an added canonical object relation row that is absent from replay closure.

Where the pre-ingest `source_snapshot_retention_ref` cannot be reconstructed from `C11LogicalRelease` alone, preserve the existing replay-manifest value; do not invent one. The required check is that all canonical persisted object/source refs that *are* independently reconstructible are covered, not that SR06 fabricates unavailable pre-ingest state.

### D. Strong hostile test

Add a test that starts from a valid persisted release and creates a semantically different, internally self-consistent canonical relation set by changing at least one semantic object and updating:

- that object's content hash/object id;
- affected replay closure refs;
- replay-manifest semantic fields/ref as needed;
- affected member byte hashes;
- relation logical digests;
- manifest self-hash;

while deliberately retaining the OLD claimed `release_identity.semantic_release_hash`, manifest release-ref content hash and old path selector.

Both:

- full `reopen(old selectors)`; and
- `VerifiedDuckDBSession(old selectors)`

must reject the altered carrier because the independently derived I02 release semantic root no longer equals the old claim.

A simpler equivalent construction is acceptable if it exercises exactly this invariant rather than merely leaving a stale object hash.

### E. Lightweight direct-session law

`VerifiedDuckDBSession` may read/verify only the tiny identity-root material required for A/B:

- manifest;
- member byte hashes;
- one `release_identity` row;
- one `replay_manifest` row.

It must still not call full `reopen()`, `_read_rows()` across the full relation universe, or reconstruct respondent/event/etc. Python object inventories.

## 4. Preserve all accepted R2 work

Do not regress:

- DTA extended-missing reader-token handling;
- normal chunked source reads;
- compatibility-only full-read exception;
- selector/path closure;
- verified multi-query in-memory DuckDB sessions;
- exact source/authority physical-to-I02 binding;
- relational Parquet schema;
- relation digests/member hashes;
- cross-relation object identity checks;
- atomic/content-addressed publication;
- no persistent `.duckdb`, PostgreSQL, SQLite or DATABASE_URL;
- existing PRE553 semantic behavior/regression expectations.

## 5. Tests

Preserve the R2 suite and add at minimum:

1. exact I02 semantic-release-root recomputation equality on an untouched release;
2. strong fully-rehashed alternate-relation-set / stale-old-release-hash rejection by full reopen;
3. the same stale-old-release-hash rejection by `VerifiedDuckDBSession`;
4. replay-manifest persisted-row identity verification;
5. replay closure rejection for an independently reconstructible canonical object absent from closure;
6. proof direct session still avoids full object-universe reconstruction;
7. existing SR06 tests;
8. existing PRE553 regression suite.

No WVS7, LiTS-I or CLOSED_35 full execution is authorized by this correction.

## 6. Gate state

`G-SR06 = SEMANTIC_ROOT_CLOSURE_REQUIRED`

This is the final synthetic correctness correction expected before proving-source scale preflight. Any new issue after this gate must be classified as either:

- a demonstrated contradiction in frozen logical semantics; or
- a real-source execution-scale issue arising in the explicitly fail-closed SR07/SR08 preflight.

Do not open another speculative synthetic redesign cycle.

Required return token:

`PRE553_SR06_SEMANTIC_ROOT_CLOSURE_RETURNED`

HQ will inspect the returned patch and, if this invariant closes without regression, close G-SR06 and authorize the WVS7/LiTS-I proving-source scale preflight.
