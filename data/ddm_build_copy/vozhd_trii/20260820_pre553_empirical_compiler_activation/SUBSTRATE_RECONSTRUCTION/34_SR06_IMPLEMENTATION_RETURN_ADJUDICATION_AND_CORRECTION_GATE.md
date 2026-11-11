# SR06 — IMPLEMENTATION RETURN ADJUDICATION AND BOUNDED CORRECTION GATE

Status: `RETURNED__NOT_ACCEPTED__BOUNDED_CORRECTION_REQUIRED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

SR06 implementation branch: `agent/vozhd-trii-sr06-c11-parquet-duckdb`

SR06 returned implementation commit: `c5e2c5c820c9b3917a4814bd7031074090763cb6`

Starting authority head for that implementation: `87e662b305956d8dc9b0f5a66c96317cf4452e6e`

## 1. Return accepted as evidence, not as gate closure

HQ accepts the implementation return as a real bounded implementation attempt.

The commit is exactly one commit ahead of its assigned base and adds only:

- `rawlsing_next/pre553_physical_decoder.py`
- `rawlsing_next/pre553_parquet_carrier.py`
- `rawlsing_next/pre553_duckdb_direct.py`
- `rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py`

The worker reports:

- SR06 tests: `4 passed`;
- full PRE553 tests: `601 passed, 2 pre-existing failures`;
- no persistent DuckDB database;
- no PostgreSQL/SQLite/DATABASE_URL dependency;
- required return token present.

Because the patch only adds the four SR06 files and does not modify the pre-existing `source_relations` implementation or tests, the two reported `source_relations` expectation failures are not adjudicated as SR06 regressions.

However, G-SR06 does **not** close. Static HQ inspection found exact contract failures that must be corrected before real WVS7/LiTS-I certification can begin.

## 2. Blocker A — Stata extended missing is not actually represented distinctly

The frozen DTA contract requires Stata system missing `.` and extended missings `.a` through `.z` to remain physically distinct.

The returned decoder defines `PhysicalMissingState.FORMAT_EXTENDED_MISSING`, but no execution path emits that state.

`metadata.missing_user_values` is currently converted into generic discrete missing declarations, and `_classify(...)` returns `FORMAT_USER_MISSING_VALUE` for those declarations.

Therefore a Stata extended missing returned through the reader's user-missing machinery would be collapsed into the generic format-user-missing class rather than `FORMAT_EXTENDED_MISSING`.

Disposition:

`BLOCKED_DTA_EXTENDED_MISSING_CLASS_COLLAPSE`

Correction requirement:

- distinguish Stata extended missing `.a`-`.z` from any other format-native user missing state;
- preserve the exact extended-missing token/code in the physical cell/declaration;
- add a direct classifier/unit fixture even if the selected synthetic DTA writer cannot emit an on-disk extended missing;
- if a lawful tiny raw DTA fixture can be produced by another deterministic fixture mechanism, test full decoder readback as well;
- do not infer semantic meaning from the extended missing code.

## 3. Blocker B — physical incidence is fully materialized as Python cell objects

The returned `_decode(...)` reads the entire source into one DataFrame and then constructs one `PhysicalCell` Python object for every source cell, finally returning `cells: tuple[PhysicalCell, ...]`.

This is not operationally viable for the accepted empirical corpus. SR03 measured `486,174,936` source cells across CLOSED_35, and the immediate proving sources themselves contain tens of millions of cells.

The frozen architecture selected a light append-only analytical substrate. Materializing every source cell simultaneously as Python dataclass objects would multiply memory far beyond raw/DataFrame size and makes SR07/SR08/full-source execution unnecessarily fragile.

Disposition:

`BLOCKED_PHYSICAL_DECODER_UNBOUNDED_CELL_OBJECT_MATERIALIZATION`

Correction requirement:

- expose deterministic batch/stream iteration for physical cells/incidence;
- do not require a tuple containing every source cell in memory;
- preserve exact global physical row ordinal and variable ordinal across batches;
- allow source-specific full-reader compatibility where the reader requires it, but stream/batch conversion out of that frame rather than creating the whole cell-object universe;
- keep metadata/source identity available independently of the cell stream;
- add a bounded synthetic multi-batch test proving batch boundaries do not change identities or output digest.

No raw proving-source scan is required for this correction.

## 4. Blocker C — returned Parquet is opaque duplicated object serialization, not the selected direct-query C11 carrier

The returned carrier writes only:

- `release.parquet`
- `objects.parquet`

`release.parquet` contains a base64 JSON encoding of the **entire `C11LogicalRelease`**, including its public/internal object tuples.

`objects.parquet` then serializes those same logical objects again, individually, as base64 JSON blobs.

This creates two persistent representations of the same logical empirical object content inside the alleged canonical carrier.

Worse, the embedded DuckDB adapter can directly query only wrapper columns such as object ref/family/content hash/blob. It cannot directly query the empirical fields required by I03/I05 without decoding opaque application blobs outside the selected relational Parquet path.

This does not implement the SR04-selected role:

`canonical empirical relations = Parquet -> embedded DuckDB direct analytical query`

and violates the SR06 requirement that there be no second canonical empirical copy.

Disposition:

`BLOCKED_OPAQUE_DUPLICATED_PARQUET_NOT_QUERYABLE_C11_RELATIONS`

Correction requirement:

Implement canonical columnar Parquet relations over the existing accepted logical C11 model.

At minimum:

- release/manifest identity relation;
- empirical universe relation;
- respondent identity relation;
- question-variable binding relation;
- respondent event relation with queryable event/respondent/question/raw-or-canonical state fields required by accepted I03/I05;
- routing eligibility relation;
- empirical coordinate relation;
- weight/measure relation or explicit typed-absence representation;
- authority snapshot relation;
- source-universe relation or explicit typed-absence representation;
- replay-binding/internal-record relation(s) sufficient to reconstruct the exact logical release;
- replay manifest relation.

Exact physical relation split may differ if a more compact normalized representation preserves all existing exact refs/semantic hashes and keeps I03/I05-critical fields directly queryable.

Rules:

- one authoritative canonical representation only;
- no full-release duplicate blob containing a second copy of all objects;
- opaque supplemental payload fields may exist only for fields not otherwise representable without loss and must not duplicate the entire release/object universe;
- reopening must reconstruct or resolve the exact accepted `C11LogicalRelease` from the canonical relations;
- DuckDB direct queries must operate on queryable canonical Parquet columns, not require base64 application-object decoding.

## 5. Blocker D — canonical query relation and logical reopen currently have different truth surfaces

The returned `reopen(...)` reconstructs the logical release solely from the serialized full-release blob in `release.parquet`.

The returned DuckDB adapter queries `objects.parquet` separately.

Thus the logical reopen path and analytical query path do not derive from one canonical logical representation. `objects.parquet` row content is not cross-checked against the reconstructed release object inventory except for file hash and row count.

A carrier cannot expose one truth surface to `C11Repository` and another to DuckDB/I03/I05.

Disposition:

`BLOCKED_SPLIT_LOGICAL_AND_QUERY_TRUTH_SURFACES`

Correction requirement:

- logical reopen and DuckDB direct query must derive from the same canonical Parquet relation set;
- readback validation must prove relation-level object/ref/content inventory equality to the accepted logical release;
- manifest must bind every canonical member and exact relation logical digest;
- mutating any canonical relation while recomputing only file bytes/manifest must still fail if relation semantics no longer match the release identity/replay identity;
- add hostile tests for cross-relation inconsistency, not only byte corruption.

## 6. Blocker E — no explicit physical-incidence -> existing I02 ingest bridge

The authority required one coherent machinery path:

`exact source bytes -> physical decoder -> source-native incidence -> existing C11 logical ingest/validation -> canonical Parquet`

The returned decoder ends at `PhysicalSourceIncidence`. The carrier begins from an already-created `C11LogicalRelease`. The tests obtain that release from an unrelated synthetic `_candidate(...)` fixture.

No adapter/builder connects decoded physical incidence to `C11SourceReleaseCandidate` / `validate_c11_source_release(...)` under explicit caller-supplied source authority.

SR06 must not invent source semantics, but it must provide the plumbing by which later SR07/SR08 authority can lawfully supply those semantics.

Disposition:

`BLOCKED_MISSING_NONSEMANTIC_PHYSICAL_TO_I02_BRIDGE`

Correction requirement:

Implement an explicit format-neutral bridge interface that:

- accepts physical incidence/batches plus explicit caller-supplied source-authority projection/mapping objects;
- never infers semantic states, canonical questions, routing, weights, country meaning, or structural meaning;
- fail-closes when required authority/mapping is absent;
- builds the existing `C11SourceReleaseCandidate` shape and invokes existing I02 validation rather than bypassing it;
- is testable with a synthetic explicit authority projection;
- leaves actual WVS7/LiTS-I semantic/source certification to SR07/SR08.

## 7. Good returned work to preserve

The correction should retain/reuse, unless technically superseded by the required fixes:

- exact SHA-bound compatibility encoding allowlist;
- rejection of automatic encoding guessing/fallback;
- compatibility-only authority status;
- SAV user-missing-preserving reader configuration;
- ordinary DTA labelled code remaining ordinary;
- exact source SHA computation;
- immutable content-addressed release path concept;
- staging-before-publication concept;
- member SHA verification;
- idempotent identical write / conflicting semantic hash rejection;
- in-memory DuckDB only;
- no `.duckdb`, PostgreSQL, SQLite or `DATABASE_URL` empirical authority path.

This is a bounded correction to the physical implementation. It does not reopen SR04 carrier selection, SR05 source constitution, I01-I07 semantics, M01-M18, I03/I05/I04 truth conditions, or V553-V558.

## 8. Required correction tests

In addition to preserving the prior passing SR06 tests, add/pass:

1. direct extended-missing classification test proving `FORMAT_EXTENDED_MISSING` is emitted distinctly;
2. multi-batch deterministic physical-incidence test with exact stable row/variable identities and digest across batch sizes;
3. test proving no API requires materializing the complete cell universe as a tuple;
4. canonical Parquet relation-schema tests showing respondent/event/coordinate/routing/weight fields are directly queryable;
5. exact logical release -> canonical relations -> reopen identity round-trip with no duplicate full-release object blob;
6. direct DuckDB I03/I05-shape smoke queries against canonical relational columns;
7. cross-relation semantic inconsistency hostile test;
8. explicit-authority physical-incidence -> `C11SourceReleaseCandidate` -> existing I02 validation bridge test;
9. missing-authority bridge fail-closed test;
10. existing SR06 corruption/atomicity tests;
11. existing PRE553 regression suite.

The correction should remain synthetic/cheap. Do not run WVS7, LiTS I, or CLOSED_35 as part of this correction unless HQ separately authorizes a bounded mechanical smoke.

## 9. Gate state

`G-SR06 = RETURNED__CORRECTION_REQUIRED`

G-SR07 and G-SR08 remain blocked.

Required corrected return token:

`PRE553_SR06_DECODER_C11_PARQUET_DUCKDB_CORRECTION_RETURNED`

HQ will inspect the corrected branch before any proving-source certification authority is issued.
