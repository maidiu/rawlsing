# SR06 RELATIONAL SCALE STORAGE R2 — COMPACT CANONICAL ENCODING AUTHORITY

Status: `AUTHORIZED__SR06_STORAGE_R2__SEMANTIC_IDENTITY_PRESERVING`

Parent authorities:

- `42_SR08_P1_RESOURCE_TRIPWIRE_ADJUDICATION_AND_SR06_SCALE_REOPEN.md`
- `43_SR06_RELATIONAL_SCALE_CORRECTION_IMPLEMENTATION_AUTHORITY.md`
- `44_SR06_RELATIONAL_SCALE_STORAGE_BUDGET_AND_TRANSIENT_ARTIFACT_LAW.md`

Returned implementation branch:

`agent/vozhd-trii-sr06-relational-scale-correction`

Returned implementation commit:

`86de36d49f81a2b38491ac660ffc84b60993dd64`

## 1. Adjudication

HQ accepts the returned 1,000,000-event relation-first court as proof that the Python-object RAM contradiction is solved in the new path:

- one million RespondentEvent rows completed;
- measured peak RSS was approximately 125 MiB;
- the 4 GiB tripwire was not approached;
- staging/scratch were removed;
- no persistent DuckDB/PostgreSQL/SQLite/cache was retained.

However G-SR06 remains OPEN because persistent storage violates Authority 44.

Measured corrected event relation:

- `78,367,539` bytes for `1,000,000` events;
- `78.367539` event-relation bytes/event.

Returned projections were explicitly lower bounds because they scale only the event-bearing relation and exclude full-source fixed/other C11 relations:

- WVS7: approximately `4.35 GiB` -> Authority-44 hard stop;
- LiTS I: approximately `2.54 GiB` -> above preferred target;
- CLOSED_35: approximately `35.48 GiB` -> Authority-44 hard stop.

Disposition `SR06_SCALE_CORRECTION_BLOCKED__PERSISTENT_STORAGE_SCALE` is accepted.

## 2. Diagnosis

The relation-first implementation fixed materialization but still writes the preexisting wide `_object_row()` physical representation nearly verbatim.

That row representation physically repeats or text-encodes identity material such as:

- `object_family` even where relation membership already fixes family;
- deterministic `object_id` strings;
- hexadecimal `content_hash` strings;
- exact refs and authority refs serialized as canonical JSON strings;
- dependency/replay refs serialized as canonical JSON;
- structured semantic fields serialized as tagged JSON where typed physical columns or compact local dictionaries can recover exactly the same logical value.

These are logical identity requirements, but they are not all mandatory duplicated UTF-8 storage fields.

The correction target is therefore compact physical encoding with exact semantic reconstruction, not semantic simplification.

## 3. Supreme parity law

The compact representation MUST reconstruct exactly the same old logical object projection.

For bounded parity fixtures, compact persisted rows reconstructed through the existing object constructors must produce EXACTLY the same:

- object family/schema/version;
- semantic fields;
- typed state;
- authority refs;
- dependency refs;
- producer replay root;
- per-object content hash;
- per-object object id;
- ExactRef;
- candidate semantic projection hash;
- ReplayManifest identity;
- semantic release hash;
- release ref;
- M01-M18 coverage.

No hash or semantic formula may change.

## 4. Derivable identity must not be redundantly persisted

Where an identity field is a deterministic function of other canonical persisted material, the compact storage MAY omit the redundant physical copy and reconstruct it on demand.

In particular, for canonical public/internal objects whose existing `object_id` is deterministically formed from family + semantic content hash:

- do not persist the long object-id UTF-8 string per event merely as duplication;
- do not persist both hex object id suffix and a second hex content-hash string when both are deterministically recoverable;
- prefer a fixed-width 32-byte binary digest only where a persisted digest is operationally required;
- if the digest itself can be deterministically recomputed from the compact semantic row and is not required as a steady-state lookup index, omission is permitted.

Object identity must remain independently checkable by reconstruction/audit.

## 5. Relation-fixed constants

Do not store a per-row column for values fixed by the relation/schema unless physical persistence is needed for exact reconstruction and cannot be supplied by the relation manifest.

Candidates include:

- object family;
- schema id/version;
- fixed topology/state/default markers;
- release/source scope refs that are exactly invariant for the entire relation or partition.

Such constants may live once in exact relation metadata/manifests and be injected during reconstruction.

## 6. Compact exact-ref and authority-ref encoding

Repeated `ExactRef` / `AuthorityRef` values must not be stored as verbose tagged canonical JSON on every event when a compact dictionary/key representation is losslessly reversible.

Permitted execution encoding:

- release-local dictionary tables with exact content-addressed identity;
- small unsigned integer dictionary keys;
- fixed-width binary hashes;
- relation-level defaults for exactly invariant refs;
- compact typed columns for ref kind/version components.

Every local dictionary must itself be immutable, exact, replay-bound and auditable.

Reconstruction must yield the exact preexisting `ExactRef` / `AuthorityRef` values.

## 7. Structured JSON elimination

For high-cardinality event relations, canonical JSON text is a semantic serialization format, not a required physical storage format.

Replace per-row tagged JSON columns with typed Parquet columns/dictionary keys wherever exact reconstruction is possible.

This especially applies to:

- authority-ref tuples;
- dependency refs;
- source/question/respondent refs;
- producer replay locators;
- topology/order/rank structures with a bounded source-native schema;
- raw-value type tags where native Parquet typed columns can retain exact value kind and value;
- repeated typed-absence/default structures.

Canonical JSON remains binding for semantic hashing after logical reconstruction.

## 8. Replay closure storage amendment

Authority 43 required exact replay closure but did not intend a second 32+ byte random-hash copy of every event when those exact refs are already derivable from canonical event rows.

For storage R2, the replay closure MAY be a **derived canonical relation** rather than a separately materialized steady-state table, provided all of the following hold:

1. bounded old/new parity proves the derived closure yields exactly the old ordered logical closure refs;
2. build/seal computes the exact existing ReplayManifest semantic identity;
3. a streaming full audit can regenerate every closure ExactRef from canonical relations and verify the stored ReplayManifest root;
4. no full closure tuple/list is materialized in RAM;
5. scratch external-sort material is deleted after successful sealing/audit;
6. no semantic or authority information is lost.

The same rule applies to per-event object-id/content-hash columns when exact values are deterministically derivable from canonical compact rows.

This is an execution-storage amendment only. Replay closure semantics remain unchanged.

## 9. Exact object resolution

Steady-state storage is not required to carry a duplicated permanent hash index for every event.

Exact object resolution may use:

- streaming/relational recomputation of exact object hashes;
- deterministic native row selectors where available from the resolved relation context;
- a separately governed NONAUTHORITATIVE regenerable index/cache.

Any optional cache must be excluded from canonical steady-state bytes and safely deletable.

No fuzzy/latest/nearest resolution is permitted.

## 10. Storage target

The strictest preferred Authority-44 source budget is WVS7:

`2 GiB / 59,595,860 cells ~= 36.03 bytes/cell`

Because other relations/fixed metadata also consume space, the corrected million-event **event-bearing relation** should target:

`<= 32 bytes/event`

Preferred outcome:

- event relation `<= 32 bytes/event`;
- projected WVS7 canonical steady state `<= 2 GiB`;
- projected LiTS I canonical steady state `<= 1.5 GiB`;
- projected CLOSED_35 canonical steady state `<= 20 GiB`.

Authority-44 hard stops remain binding:

- WVS7 `>= 4 GiB`;
- LiTS I `>= 3 GiB`;
- CLOSED_35 `>= 32 GiB`.

A result above the preferred target but below hard stop remains HQ-adjudicated, not automatically accepted.

## 11. Required comparative storage court

Repeat the 1,000,000-event synthetic court after compact encoding.

Report side by side:

- prior wide relation bytes/event: `78.367539`;
- compact relation bytes/event;
- percent reduction;
- canonical bytes by relation;
- fixed metadata bytes;
- event relation bytes;
- dictionary/ref-table bytes;
- replay/closure steady-state bytes;
- optional cache bytes;
- staging peak;
- scratch peak;
- post-cleanup retained bytes;
- peak RSS by phase.

Also test at least three Parquet physical configurations on the same canonical million-event fixture without changing semantics:

- ZSTD level 3;
- a higher ZSTD level chosen reasonably for archival/steady-state size;
- row-group size at least one materially larger than 4,096 rows.

Choose the smallest configuration unless measured write/read cost is operationally pathological. Record the tradeoff; do not assume level 3 / 4,096 is optimal.

## 12. Realistic cardinality law

The storage court must not win merely because a toy fixture has unrealistically low cardinality.

The million-event fixture must include realistic variation in:

- respondents;
- questions/source variables;
- raw numeric/string values;
- physical missing states;
- event identity/order fields;
- repeated and nonrepeated refs.

Report cardinalities for every compact dictionary/key relation.

## 13. Full parity and regression remain required

Storage R2 does not waive unfinished Authority-43 obligations.

Before returning PASS, run:

- bounded old/new exact semantic parity suite;
- hostile physical-state parity suite;
- million-event memory court under 4 GiB tripwire;
- streaming full audit;
- direct DuckDB queries;
- exact on-demand reconstruction;
- full existing PRE553 regression suite, preserving the frozen unrelated baseline failures/skips only.

Focused tests alone are not sufficient for G-SR06 closure.

## 14. Real-source boundary

Do NOT run full WVS7, full LiTS I or CLOSED_35 in this correction cell.

After HQ accepts compact relation-first SR06, real proving-source scale courts resume.

## 15. Gate state

`G-SR06 = STORAGE_R2_COMPACT_CANONICAL_ENCODING_REQUIRED`

`G-SR07 = BLOCKED_ON_G_SR06`

`G-SR08 = BLOCKED_ON_G_SR06`

`G-SR09 = BLOCKED`

## 16. Allowed return dispositions

Exactly one:

- `SR06_STORAGE_R2_RETURNED__PARITY_MEMORY_STORAGE_PASS`
- `SR06_STORAGE_R2_BLOCKED__PERSISTENT_STORAGE_SCALE`
- `SR06_STORAGE_R2_BLOCKED__SEMANTIC_IDENTITY_PARITY`
- `SR06_STORAGE_R2_BLOCKED__RESOURCE_SCALE`
- `SR06_STORAGE_R2_BLOCKED__FROZEN_CONTRACT_CONTRADICTION`
- `SR06_STORAGE_R2_BLOCKED__RUNTIME_DEPENDENCY`

Required token:

`PRE553_SR06_STORAGE_R2_COMPACT_CANONICAL_ENCODING_RETURNED`
