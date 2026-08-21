# SR06 RELATIONAL SCALE CORRECTION — IMPLEMENTATION AUTHORITY

Status: `AUTHORIZED__CODEX_IMPLEMENTATION__SEMANTIC_IDENTITY_PRESERVING`

Parent contradiction authority:

`42_SR08_P1_RESOURCE_TRIPWIRE_ADJUDICATION_AND_SR06_SCALE_REOPEN.md`

## 1. Mission

Replace the full-source Python-object materialization requirement with a scalable relation-backed C11 execution representation while preserving the accepted C11 semantic architecture.

Target execution shape:

`physical incidence batches -> canonical validated relation batches -> immutable Parquet -> lightweight exact release handle -> direct DuckDB / exact on-demand object reconstruction`

This is an execution and storage representation correction.

It is NOT authorization to redesign source semantics, public C11 object meaning, M01-M18, I03/I05 truth conditions, structural admission, or downstream V553+ behavior.

## 2. Binding semantic parity

For every bounded package that can be processed by both old and new paths, the new path must reproduce exactly the same logical identity material:

- per-object `object_id` and `content_hash`;
- exact public object refs;
- exact internal record refs;
- order-invariant candidate semantic projection hash;
- ReplayManifest exact semantic identity;
- semantic release hash;
- M01-M18 coverage;
- source artifact ref;
- release ref.

The old bounded object path is the parity oracle for those tests.

Do not change a hash formula merely to make streaming easier.

## 3. Relation-first admission

Implement a scalable source-release admission API that does not require construction of a `C11SourceReleaseCandidate` containing complete tuple inventories.

The implementation may introduce new internal runtime types such as a relation candidate / relation batch / sealed release handle. Names are not frozen here.

The relation-first candidate must be able to consume deterministic bounded streams / Arrow RecordBatches / equivalent batch sources for logical sections.

At minimum support the logical families already required by I02:

- EmpiricalUniverse;
- RespondentIdentity;
- QuestionVariableBinding;
- RespondentEvent;
- RoutingEligibilityFact;
- EmpiricalCoordinateFact;
- WeightMeasureFact or typed absence;
- AuthoritySnapshot;
- SourceUniverseRelation or typed distinct default;
- replay-binding families or lawful typed absences;
- ReplayManifest identity/closure.

## 4. Streaming exact object validation

The scalable path must validate exact object identity and family law without retaining the full object universe.

It may:

- construct one object or one bounded batch transiently and discard it;
- validate canonical row projections directly;
- use DuckDB/Arrow relational checks where exactly equivalent.

It may NOT accumulate one Python semantic object per full-source event.

Every persisted canonical object row must still have an independently checkable deterministic object id/content hash under existing object semantics.

## 5. Candidate projection hash without giant lists

Existing I02 candidate projection semantics remain binding.

Implement deterministic streaming canonical hashing of the same logical projection that `_candidate_projection()` currently hashes after constructing sorted ref lists.

Small-fixture tests must prove byte/hash identity with the old `semantic_hash(_candidate_projection(candidate))` result.

The implementation may external-sort/spill exact refs or use sorted Parquet/DuckDB relations. It may not replace the semantic projection with a different relation-digest formula unless the resulting canonical semantic bytes are exactly equivalent to the existing projection.

## 6. Replay closure without giant Python tuples

Replay closure remains exact and exhaustive.

Persist closure refs as a canonical, deterministic relation suitable for streaming validation/hashing.

Do not require all closure refs to coexist as a Python tuple for a full release.

The persisted replay-manifest representation may separate a lightweight header row from the canonical closure-ref relation for execution purposes, PROVIDED that the exact semantic ReplayManifest identity computed from the persisted material equals the identity the old bounded `ReplayManifest` object would produce.

Small-fixture parity is mandatory.

## 7. Variable/source metadata normalization

Do not repeat invariant source-variable metadata inside every respondent event merely because the P1 execution-only fixture did so.

Canonical source substrate relations may store once per source variable / exact dictionary:

- source variable ordinal/name;
- storage/display/measure metadata;
- variable label;
- value-label dictionary;
- source-native missing declarations/ranges;
- topology/MR declarations;
- reader/configuration provenance.

Event/cell rows may retain only the exact raw event material plus exact refs/keys needed to recover the governing source-variable metadata.

This is lawful only if replay proves complete recoverability of the physical information required by the source-native constitution.

No physical declaration, label dictionary, topology fact or raw state may disappear because it was normalized out of the event row.

## 8. Lightweight sealed release handle

Implement a validated lightweight exact release handle for full releases.

It must expose at minimum:

- exact release ref;
- source artifact ref;
- semantic release hash;
- exact replay-manifest ref;
- M01-M18 coverage;
- canonical relation/member inventory;
- relation logical digests;
- canonical member byte hashes;
- exact release directory / carrier identity.

Creating or opening this handle must not reconstruct the complete event/object universe in Python.

## 9. Parquet carrier

`PARQUET_DUCKDB_DIRECT` remains binding.

The scalable admission path must write canonical Parquet incrementally/atomically from validated relation batches.

Requirements:

- staging writes cannot become visible releases;
- exact deterministic relation/member identity;
- ZSTD compression;
- no second authoritative empirical copy;
- no persistent `.duckdb` authority;
- no PostgreSQL / SQLite / DATABASE_URL;
- corruption/missing-member failure remains fail-closed;
- idempotent identical publication;
- conflicting same-release identity rejection.

## 10. Full audit and ordinary access separation

Ordinary verified open/query MUST NOT perform full Python object reconstruction.

Provide a streaming/full-audit operation that can prove every relation/object/ref/authority/replay invariant while remaining memory-bounded.

A bounded compatibility helper may still reconstruct an old `C11LogicalRelease` for tests or small packages, but full-source certification must not depend on it.

## 11. Exact object resolution on demand

A relation-backed repository/access layer must resolve an exact object ref on demand from verified canonical Parquet and reconstruct only the requested object (or bounded requested set).

No latest/fuzzy fallback.

The old in-memory `C11Repository` may remain for bounded compatibility tests but cannot be the required production store for full survey releases.

## 12. Physical-to-I02 bridge

Add a scalable bridge from accepted physical incidence batches + explicit source authority projection into the relation-first I02 admission path.

Preserve the existing fail-closed laws:

- source SHA binding;
- exact AuthorityRef binding;
- no semantic missing inference;
- no canonical question/value inference;
- no routing inference;
- no default weight;
- no country interpretation;
- compatibility encoding remains execution-only unless separately authorized.

Keep the old object-returning bridge as bounded compatibility if useful.

## 13. Direct DuckDB

Verified DuckDB sessions continue to query canonical Parquet directly.

They must consume the new lightweight release identity/root verification and must never trigger full relation reconstruction.

## 14. Required parity tests

Using small synthetic candidates processed through BOTH old and new paths, require exact equality of:

1. every public/internal object ref;
2. candidate semantic projection hash;
3. ReplayManifest ref/content hash;
4. semantic release hash;
5. release ref;
6. M01-M18 coverage;
7. exact query results over canonical Parquet.

Include hostile parity for:

- observed value;
- system missing;
- SAV user-missing declaration/value/range representation;
- DTA ordinary absence-looking value;
- ordered/ranked event identity;
- competing weight candidates;
- explicit typed absences.

## 15. Required scale court

Run a synthetic relation-first scale court of at least:

`1,000,000 RespondentEvent rows`

with realistic repeated respondent/question refs and source-variable metadata.

It must complete:

- relation-first admission;
- exact semantic/replay identity derivation;
- Parquet publication;
- lightweight verified open;
- streaming full audit;
- multiple direct DuckDB queries;
- exact single-object on-demand reconstruction.

Run under an external 4 GiB hard RSS tripwire.

Target acceptance condition:

- completes below 2 GiB peak RSS;
- no phase reaches 4 GiB;
- no complete event object tuple/list is materialized;
- no complete replay closure tuple/list is materialized.

If 1,000,000 rows cannot complete below 2 GiB, return measured evidence; do not silently lower the requirement and claim pass.

## 16. Regression law

All accepted PRE553 semantic/runtime tests must continue to pass except already-frozen unrelated baseline failures.

Do not edit accepted expected semantic identities to make the new path pass.

## 17. Real-source boundary

Do NOT run full WVS7 or full LiTS I in this implementation cell.

Synthetic/bounded fixtures only.

After HQ accepts this implementation, the proving-source scale courts will be rerun against the new path.

## 18. Allowed implementation disposition

Exactly one:

- `SR06_SCALE_CORRECTION_RETURNED__PARITY_AND_SCALE_PASS`
- `SR06_SCALE_CORRECTION_BLOCKED__SEMANTIC_IDENTITY_PARITY`
- `SR06_SCALE_CORRECTION_BLOCKED__RESOURCE_SCALE`
- `SR06_SCALE_CORRECTION_BLOCKED__FROZEN_CONTRACT_CONTRADICTION`
- `SR06_SCALE_CORRECTION_BLOCKED__RUNTIME_DEPENDENCY`

## 19. Required return token

`PRE553_SR06_RELATIONAL_SCALE_CORRECTION_RETURNED`
