# SR06 STORAGE R2 RETURN ADJUDICATION AND R3 NORMALIZED RELATIONAL ENCODING AUTHORITY

Status: `AUTHORIZED__SR06_STORAGE_R3__WHOLE_MACHINE_VISION_PRESERVED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Returned worker branch: `agent/vozhd-trii-sr06-relational-scale-correction`

Returned continuation head: `86de36d49f81a2b38491ac660ffc84b60993dd64`

Returned commit: `1f25a9a011d51c47d11f6b78d306a6e916063774`

Parent authorities:

- `00_COMMAND_CHARTER.md`
- `42_SR08_P1_RESOURCE_TRIPWIRE_ADJUDICATION_AND_SR06_SCALE_REOPEN.md`
- `43_SR06_RELATIONAL_SCALE_CORRECTION_IMPLEMENTATION_AUTHORITY.md`
- `44_SR06_RELATIONAL_SCALE_STORAGE_BUDGET_AND_TRANSIENT_ARTIFACT_LAW.md`
- `46_SR06_RELATIONAL_SCALE_STORAGE_R2_COMPACT_CANONICAL_ENCODING_AUTHORITY.md`

Whole-machine parent law remains the already-closed whole-machine architecture and post-closure implementation-release program. This ruling does not reopen architecture.

## 1. Whole-machine containment adjudication

`NO_WHOLE_MACHINE_VISION_DRIFT_FOUND`

The returned delta is exactly one commit above the authorized continuation head and changes only:

- `rawlsing_next/pre553_relation_first.py`
- `rawlsing_next/tests/test_pre553_relation_first.py`

No V553/V554/V555/V556/V557/V558/V3/V2 runtime file changed.

The returned implementation reconstructs compact rows through the existing semantic constructors and retains exact parity requirements for:

- semantic fields;
- typed state;
- authority refs;
- dependency refs;
- producer replay roots;
- ExactRefs;
- candidate semantic projection;
- logical relation digests.

The full PRE553 regression returned:

- `618 passed`;
- `2` unchanged pre-existing unrelated failures in `test_pre553_source_relations.py`;
- `1 skipped`.

Therefore the returned work remains within the already-closed whole-machine architecture. The failure below is physical representation only.

## 2. Storage R2 adjudication

HQ accepts the returned evidence and accepts the worker disposition:

`SR06_STORAGE_R2_BLOCKED__PERSISTENT_STORAGE_SCALE`

Measured million-event results:

- event relation, ZSTD 3 / RG 4096: `27.026938 bytes/event`;
- event relation, ZSTD 9 / RG 4096: `25.712552 bytes/event`;
- event relation, ZSTD 3 / RG 16384: `27.026938 bytes/event`;
- dictionary bytes at ZSTD 3 / RG 4096: `52,815,592`;
- dictionary bytes at ZSTD 9 / RG 4096: `53,139,614`;
- total canonical bytes/event remains approximately `79`;
- peak RSS remained below the 4 GiB tripwire and around the Authority-43 target band.

The event-bearing relation achieved the R2 row target, but total steady-state storage did not improve materially because high-cardinality logical material was displaced into side dictionaries.

## 3. Exact diagnosis

The R2 codec is still too generic for the respondent-grain fact relation.

`_CompactDictionary` interns every encountered:

- string;
- `ExactRef`;
- `AuthorityRef`;

and writes dictionary entries as canonical JSON.

For low-cardinality repeated constants this is useful.

For high-cardinality respondent/event identity and exact refs this is not compression. It is a second physical representation of material that should instead be represented by normalized relation keys or deterministically reconstructed from canonical dimension/fact rows.

Therefore:

`THIN_EVENT_ROW + HIGH_CARDINALITY_SIDE_DICTIONARY != ACCEPTABLE_NORMALIZATION`

The next correction is not another generic compression pass. It is a semantic-family-aware physical normalization of the already-frozen C11 relations.

## 4. R3 mission

Replace the generic per-relation `pickle + dictionary-every-string/ref` steady-state encoding for high-volume C11 fact relations with an explicit normalized relational physical schema.

This is execution representation only.

Do NOT alter:

- C11 public semantic object families;
- internal C11 record families;
- M01-M18 meaning;
- object semantic projections;
- object-id/content-hash formula;
- ExactRef semantics;
- source authority semantics;
- I03 exact-query truth conditions;
- I05 exact-bounded discovery truth conditions;
- I04 structural-admission law;
- V553-V558 semantics;
- V3/V2 semantics;
- whole-machine stage ownership or causal jurisdiction.

Any apparent need to alter one of those returns:

`SR06_STORAGE_R3_BLOCKED__FROZEN_CONTRACT_CONTRADICTION`

with a minimal hostile proof.

## 5. Normalized relation law

The physical representation may introduce release-local execution keys only as lossless foreign keys into canonical relations.

Release-local execution keys:

- are NOT semantic IDs;
- do NOT replace ExactRefs;
- do NOT create a new ontology;
- must be deterministically assigned within a sealed release;
- must be replay-bound and independently auditable;
- must reconstruct the exact pre-existing logical object through existing constructors.

For `RespondentEvent`, prefer a fact-table shape whose repeated semantic dependencies are represented by compact local keys into already-canonical dimensions/relations rather than by one JSON dictionary row per encountered ExactRef/string.

At minimum evaluate explicit typed columns / local keys for:

- empirical universe;
- scoped respondent;
- native question / source variable;
- canonical question if separately authorized;
- component/subitem identity;
- event-group identity;
- source-native deterministic event index / row-variable locator;
- raw response value kind and exact representation;
- canonical response value only if authorized;
- value-transform authority;
- response topology;
- multiplicity/order/rank fields;
- response state / typed state.

Where a dependency is already represented canonically in another C11 relation, the event row should normally carry only the compact deterministic local foreign key needed to join that relation.

## 6. High-cardinality material law

Do NOT place high-cardinality material into a separate steady-state dictionary merely to make the event fact row smaller.

Specifically:

- respondent-specific refs must normally resolve through the canonical respondent relation / deterministic respondent local key;
- question-variable refs must normally resolve through the canonical question-variable relation / deterministic variable local key;
- event-specific refs/object IDs/content hashes must be derived from the normalized logical row when exact reconstruction/audit requires them;
- event-specific or near-event-cardinality strings must not be copied into JSON dictionary rows;
- raw high-cardinality strings may be stored directly in typed Parquet columns and left to Parquet/ZSTD encoding unless a measured bounded dictionary is genuinely smaller;
- authority refs that are release-, source-, variable-, topology-, or transformation-level constants should be relation/partition constants or bounded dimension keys rather than repeated JSON.

A dictionary table is permitted only for genuinely repeated bounded-cardinality material where its measured total canonical bytes are lower than direct typed storage and exact reconstruction remains lossless.

## 7. No opaque canonical event blob

The canonical steady-state `RespondentEvent` fact relation may not be a single opaque per-event `pickle` payload plus side dictionaries.

Typed Parquet columns are required for the high-volume event fact relation.

A bounded compatibility serializer may remain for parity tests, but it is not the full-source canonical carrier.

Python `pickle` is not a canonical semantic authority and must not be necessary for long-term exact release interpretation.

## 8. Exact reconstruction law

For every bounded parity fixture, the normalized physical row plus its joined canonical dimensions/constants must reconstruct through the existing `RespondentEvent` constructor to exactly the old object.

Require exact equality of:

- all required semantic fields;
- typed state / response state;
- authority refs;
- dependency refs;
- producer replay root;
- content hash;
- object id;
- ExactRef;
- candidate semantic projection hash;
- ReplayManifest identity;
- semantic release hash;
- release ref;
- M01-M18 coverage.

No expected semantic identity may be edited to make R3 pass.

## 9. Local-key determinism and replay

Every release-local dimension/key mapping must have deterministic identity and ordering.

Permitted bases include:

- exact source-native ordinal where already governed and sufficient;
- deterministic sorted exact-ref order;
- deterministic first-occurrence order only if source traversal order is itself frozen replay identity and parity proves invariance.

The selected basis must be explicit in the release manifest and must replay exactly after reopen.

No mutable database sequence, filesystem order, process hash order, or wall clock may affect local keys.

## 10. Two realistic million-event courts

The prior generic million-event fixture is no longer sufficient by itself.

Run two source-shape synthetic courts without reading full real source bytes:

### Court A — WVS7-like

- exactly 613 source variables;
- at least 1,000,000 respondent-event rows;
- respondent count chosen to produce the event frontier at approximately the real WVS7 cells/respondent density;
- realistic repeated question refs, respondent refs, response states, numeric/categorical values, topology/order fields and bounded authorities.

### Court B — LiTS-I-like

- exactly 1,198 source variables;
- at least 1,000,000 respondent-event rows;
- respondent count chosen to produce the event frontier at approximately the real LiTS-I cells/respondent density;
- realistic DTA-like numeric/string/raw-value variation and bounded authorities.

Both courts must remain synthetic and may not inspect full WVS7/LiTS-I source data.

Report exact cardinality for every physical dimension/key relation.

## 11. Storage acceptance

For each court report separately:

- event fact bytes;
- respondent dimension bytes;
- question-variable dimension bytes;
- authority/ref dimension bytes;
- topology/value dictionary bytes if any;
- fixed release metadata bytes;
- replay/manifest bytes;
- total canonical steady-state bytes;
- total canonical bytes/event;
- staging peak bytes;
- scratch peak bytes;
- post-cleanup retained bytes;
- peak RSS.

Preferred acceptance remains:

- projected WVS7 canonical steady state `<= 2 GiB`;
- projected LiTS I canonical steady state `<= 1.5 GiB`;
- projected CLOSED_35 canonical steady state `<= 20 GiB`.

Hard stops remain:

- WVS7 `>= 4 GiB`;
- LiTS I `>= 3 GiB`;
- CLOSED_35 `>= 32 GiB`.

Projection must account separately for event-, respondent-, variable-, authority-, and fixed-release-scaled relations. Do not multiply one generic bytes/event number across every relation.

## 12. Memory acceptance

Both million-event courts must complete under the existing external 4 GiB hard RSS tripwire.

Preferred peak RSS remains `< 2 GiB`.

No complete full-event object universe or full replay closure may coexist in Python memory.

## 13. Query / audit / exact access

R3 must still provide:

- direct DuckDB queries over normalized canonical Parquet;
- verified lightweight release open without full reconstruction;
- memory-bounded streaming full audit;
- exact on-demand object reconstruction;
- exact fail-closed member/hash verification;
- no fuzzy/latest/nearest fallback.

Querying the fact table may join canonical dimensions; it must not reconstruct all semantic objects merely to filter/count/group.

## 14. Full regression

Run the full PRE553 suite.

The current accepted baseline is:

- 618 passing;
- 2 pre-existing unrelated `test_pre553_source_relations.py` failures;
- 1 skip.

R3 may not introduce a new failure or alter expected semantic identities.

## 15. Real-source boundary

Do NOT run full WVS7.

Do NOT run full LiTS I.

Do NOT run CLOSED_35.

Real proving-source execution remains blocked on accepted G-SR06 closure.

## 16. Allowed R3 dispositions

Exactly one:

- `SR06_STORAGE_R3_RETURNED__PARITY_MEMORY_STORAGE_PASS`
- `SR06_STORAGE_R3_BLOCKED__PERSISTENT_STORAGE_SCALE`
- `SR06_STORAGE_R3_BLOCKED__SEMANTIC_IDENTITY_PARITY`
- `SR06_STORAGE_R3_BLOCKED__RESOURCE_SCALE`
- `SR06_STORAGE_R3_BLOCKED__FROZEN_CONTRACT_CONTRADICTION`
- `SR06_STORAGE_R3_BLOCKED__RUNTIME_DEPENDENCY`

Required token:

`PRE553_SR06_STORAGE_R3_NORMALIZED_RELATIONAL_ENCODING_RETURNED`

Then STOP.

Do not restart SR07 or SR08. HQ adjudicates R3 first.
