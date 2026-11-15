# SR06 STORAGE R3 RETURN ADJUDICATION AND R4 FUNCTIONAL-DEPENDENCY COMPACTION AUTHORITY

Status: `AUTHORIZED__SR06_STORAGE_R4__WHOLE_MACHINE_VISION_PRESERVED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Returned worker branch: `agent/vozhd-trii-sr06-relational-scale-correction`

Returned continuation head: `1f25a9a011d51c47d11f6b78d306a6e916063774`

Returned commit: `4db4599bdb3582c806525beaeb6af46cb64eeb09`

Parent authorities:

- whole-machine architecture closure and Rawlsing Governing Spirit;
- `00_COMMAND_CHARTER.md`;
- `43_SR06_RELATIONAL_SCALE_CORRECTION_IMPLEMENTATION_AUTHORITY.md`;
- `44_SR06_RELATIONAL_SCALE_STORAGE_BUDGET_AND_TRANSIENT_ARTIFACT_LAW.md`;
- `46_SR06_RELATIONAL_SCALE_STORAGE_R2_COMPACT_CANONICAL_ENCODING_AUTHORITY.md`;
- `47_SR06_STORAGE_R2_RETURN_ADJUDICATION_AND_R3_NORMALIZED_RELATIONAL_ENCODING_AUTHORITY.md`.

This ruling does not reopen architecture.

## 1. Whole-machine containment adjudication

`NO_WHOLE_MACHINE_VISION_DRIFT_FOUND`

The R3 delta is exactly one commit above its authorized continuation head and changes only:

- `rawlsing_next/pre553_normalized_relation.py`;
- `rawlsing_next/tests/test_pre553_normalized_relation.py`.

No V553/V554/V555/V556/V557/V558/V3/V2 runtime file changed.

The R3 representation explicitly treats local keys as execution-only, reconstructs through the existing `RespondentEvent` constructor, and preserves exact logical identity.

Reported full PRE553 regression:

- `620 passed`;
- `2` unchanged pre-existing unrelated failures in `test_pre553_source_relations.py`;
- `1 skipped`.

Therefore the R3 return remains inside the already-closed whole-machine architecture. The failure below is physical representation only.

## 2. R3 storage adjudication

HQ accepts the returned evidence and accepts:

`SR06_STORAGE_R3_BLOCKED__PERSISTENT_STORAGE_SCALE`

Measured synthetic million-event courts:

### WVS7-like

- 613 variables;
- 1,000,000 events;
- 100,000 respondents;
- event fact: `58.592889 bytes/event`;
- total canonical: `65.795816 bytes/event`;
- peak RSS: approximately `485.5 MiB`;
- projection-only WVS7: approximately `3.50 GiB`.

### LiTS-I-like

- 1,198 variables;
- 1,000,000 events;
- 250,000 respondents;
- event fact: `60.359144 bytes/event`;
- total canonical: `74.395620 bytes/event`;
- peak RSS: approximately `570.7 MiB`;
- projection-only LiTS I: approximately `2.32 GiB`.

Projection-only CLOSED_35 using the LiTS-like profile is approximately `32.46 GiB`, above the Authority-44 hard stop.

Memory remains acceptable. Storage does not.

## 3. R3 diagnosis

R3 proved that normalized typed fact/dimension storage and exact reconstruction are viable, but it did not yet exploit enough physical functional dependency.

The current `RespondentEvent` fact row still physically carries many values that are commonly relation-, partition-, variable-, or enum-level constants/defaults, including:

- release-wide empirical universe key;
- duplicate `typed_state` and `response_state`, despite the frozen invariant that they are equal for RespondentEvent;
- 64-bit keys for dimensions whose actual source cardinality permits materially narrower deterministic dense ordinals;
- canonical-question/component/topology/transform material directly in the event fact even when exactly governed by question/variable-level defaults;
- producer replay root fields per event even when invariant for the relation/partition;
- JSON multiplicity/order/rank material in every event row;
- event authority membership rows even where the same authority set applies to an entire release/partition/question family;
- string event/group identifiers even where exact deterministic source-native ordinals or composite locators can recover them.

R2 already proved an event relation near `26 bytes/event` is physically attainable while retaining semantic parity. R3 proved bounded normalized dimensions can reconstruct exact semantic objects. R4 must combine those two wins.

## 4. R4 mission

Implement semantic-family-aware physical compaction using:

`typed narrow fact columns + deterministic dense dimension ordinals + relation/partition/question defaults + sparse exact overrides`

while reproducing the exact same frozen C11 semantic objects.

This is execution representation only.

Do NOT alter:

- C11 public/internal semantic families;
- M01-M18 meaning;
- semantic projections;
- ExactRef semantics;
- object-id/content-hash formulas;
- source authority semantics;
- I03/I05 truth conditions;
- I04 structural admission law;
- V553-V558/V3/V2 semantics;
- whole-machine stage ownership or causal jurisdiction.

Any apparent need to alter those returns:

`SR06_STORAGE_R4_BLOCKED__FROZEN_CONTRACT_CONTRADICTION`.

## 5. Mandatory Phase A — storage anatomy before implementation

Before changing the R3 schema, rerun bounded WVS-like and LiTS-like courts and produce a storage anatomy receipt.

Measure separately:

- bytes for every R3 fact column or tightly coupled column family by controlled rewrite/ablation;
- bytes for every dimension/member relation;
- cardinality and distinct-count ratio for every fact column;
- null/default rate for every optional fact field;
- cardinality of authority/dependency sets;
- frequency of producer replay roots;
- frequency of topology/component/transform/canonical-question defaults per native question;
- distribution of multiplicity/order/rank payloads;
- event/group identifier forms and whether they are deterministic functions of source traversal locator.

Classify every persisted field as exactly one:

- `EVENT_INTRINSIC_MUST_STORE`;
- `DERIVABLE_FROM_EVENT_LOCATOR`;
- `RELATION_CONSTANT`;
- `PARTITION_CONSTANT`;
- `QUESTION_DEFAULT_WITH_SPARSE_OVERRIDE`;
- `RESPONDENT_DIMENSION_DERIVABLE`;
- `BOUNDED_ENUM_OR_DIMENSION_KEY`;
- `SPARSE_EVENT_OVERRIDE_REQUIRED`.

Do not remove or relocate a field without exact reconstruction proof for its classification.

## 6. Dense local ordinals

R3's 64-bit hash-derived local keys are lawful but not storage-optimal.

R4 may use deterministic dense local ordinals, with the narrowest safe unsigned physical type selected from exact cardinality:

- `uint8` where sufficient;
- `uint16` where sufficient;
- `uint32` where sufficient;
- `uint64` only when required.

Dense ordinal assignment must be deterministic and replay-bound, preferably by canonical sorted exact-ref order or an already-governed source-native ordinal.

The ordinal is execution-only and never becomes semantic identity.

Collision-free reversibility is mandatory.

## 7. Fact-row compaction laws

### 7.1 Universe

If exactly one empirical universe governs the relation/partition, store it once in the relation/partition manifest, not per event.

Support explicit partitioning or sparse override only if a lawful package genuinely requires multiple universes in one physical member.

### 7.2 Response state

For `RespondentEvent`, the frozen semantic invariant is:

`typed_state == response_state`.

Persist one compact state code and reconstruct both logical fields.

The code-to-state mapping must be immutable and relation-manifest-bound.

### 7.3 Question-governed defaults

Where exact bounded proof establishes that a field is a deterministic function of native question/variable plus frozen authority, store the default once in the question-variable dimension.

Candidate fields include:

- canonical question if authorized;
- component/subitem identity;
- response topology;
- value-transform authority;
- event-group identity;
- ordinary multiplicity/order schema.

If a field can vary by event, preserve exact variation through a sparse override relation rather than widening every event row.

### 7.4 Producer replay root

If producer replay root is invariant for the relation/partition, store it once in sealed relation metadata.

If it varies only by bounded subgroup/question, use a bounded dimension/default.

If genuinely event-varying, store the exact sparse/event value.

### 7.5 Event locator / identity

Do not persist verbose event/group strings when the exact existing semantic values are deterministically recoverable from governed source-native row ordinal, variable ordinal, component/slot ordinal, and frozen event-index rule.

If arbitrary source-native string identity exists and is not derivable, preserve it exactly.

A source-native event locator may be encoded with narrow typed ordinals and reconstruct the existing `response_event_id_or_deterministic_index` exactly.

### 7.6 Multiplicity/order/rank

Do not persist canonical JSON in every row when the overwhelming default is empty/common topology.

Use typed bounded columns and/or a sparse exact override relation. Reconstruction must reproduce the exact preexisting semantic mapping.

### 7.7 Canonical response value

Where canonical response is absent, do not pay a dense wide-column cost beyond Parquet null encoding.

Where it is deterministically produced from raw value plus an exact frozen transform authority, omission is permitted only if reconstruction recomputes the exact existing canonical value and bounded parity proves identity.

Otherwise retain the exact canonical value.

## 8. Authority and dependency compaction

Do not create one membership row per event when the exact authority/dependency set is a relation/partition/question default.

Permit:

- relation-level default set;
- partition-level default set;
- question-level default set;
- sparse event additions/removals/overrides.

The exact `authority_snapshot_refs` and `dependency_refs` for every reconstructed event must equal the old object exactly.

No semantic authority may become implicit or unreplayable merely for size.

## 9. Canonical event relation target

R4 should target the stricter WVS7 budget.

Preferred synthetic WVS-like result:

- event fact `<= 24 bytes/event`;
- all event-scaled sparse/override/member relations combined `<= 4 bytes/event` average;
- total event-scaled canonical storage `<= 28 bytes/event`;
- fixed/respondent/question/authority/replay dimensions small enough that projected WVS7 steady-state is `<= 2 GiB`.

These are engineering targets, not semantic permission to drop information.

If exact lossless semantics cannot meet them, return the measured lower bound honestly.

## 10. Two million-event courts remain mandatory

Repeat both:

### WVS7-like

- 613 variables;
- >=1,000,000 events;
- realistic WVS-like respondent density;
- realistic missing/state/value/topology variation.

### LiTS-I-like

- 1,198 variables;
- >=1,000,000 events;
- realistic LiTS-like respondent density;
- realistic numeric/string/state/topology variation.

Do not read full real sources.

For each court report:

- R3 baseline bytes by relation;
- Phase-A storage anatomy;
- R4 bytes by relation;
- event fact bytes/event;
- event-scaled sparse relation bytes/event;
- respondent dimension bytes;
- question dimension bytes;
- authority/dependency/default/override bytes;
- fixed metadata/replay bytes;
- total canonical bytes/event;
- peak RSS;
- write/read/audit times;
- exact cardinalities.

## 11. Projection law

Project WVS7, LiTS I and CLOSED_35 separately by scaling the correct dimensions:

- event-scaled;
- respondent-scaled;
- variable-scaled;
- source/release-fixed.

Do not use one generic bytes/event multiplier for all relations.

Preferred steady-state targets remain:

- WVS7 `<= 2 GiB`;
- LiTS I `<= 1.5 GiB`;
- CLOSED_35 `<= 20 GiB`.

Hard stops remain:

- WVS7 `>= 4 GiB`;
- LiTS I `>= 3 GiB`;
- CLOSED_35 `>= 32 GiB`.

## 12. Memory / query / replay acceptance

Both courts must remain under the external 4 GiB RSS tripwire; preferred peak RSS remains `<2 GiB`.

Require:

- direct DuckDB query without semantic-object universe reconstruction;
- lightweight verified open;
- streaming full audit;
- exact on-demand reconstruction;
- deterministic local-ordinal replay;
- exact member/hash verification;
- no fuzzy/latest/nearest fallback;
- no persistent DuckDB/PostgreSQL/SQLite;
- no retained disposable cache.

## 13. Supreme parity

Bounded old/R3/R4 logical reconstruction must match exactly for hostile fixtures:

- semantic fields;
- typed/response state;
- authority refs;
- dependency refs;
- producer replay root;
- object id;
- content hash;
- ExactRef;
- candidate semantic projection hash;
- ReplayManifest identity;
- semantic release hash;
- release ref;
- M01-M18 coverage.

No semantic expected value may be edited to make R4 pass.

## 14. Full regression

Run the full PRE553 suite.

Current frozen baseline:

- `620 passed`;
- `2` unchanged pre-existing `test_pre553_source_relations.py` failures;
- `1 skipped`.

No new failure is permitted.

## 15. Real-source boundary

Do NOT run full WVS7.

Do NOT run full LiTS I.

Do NOT run CLOSED_35.

SR07/SR08 remain blocked until G-SR06 closes.

## 16. Allowed R4 dispositions

Exactly one:

- `SR06_STORAGE_R4_RETURNED__PARITY_MEMORY_STORAGE_PASS`;
- `SR06_STORAGE_R4_BLOCKED__PERSISTENT_STORAGE_SCALE`;
- `SR06_STORAGE_R4_BLOCKED__SEMANTIC_IDENTITY_PARITY`;
- `SR06_STORAGE_R4_BLOCKED__RESOURCE_SCALE`;
- `SR06_STORAGE_R4_BLOCKED__FROZEN_CONTRACT_CONTRADICTION`;
- `SR06_STORAGE_R4_BLOCKED__RUNTIME_DEPENDENCY`.

Required token:

`PRE553_SR06_STORAGE_R4_FUNCTIONAL_DEPENDENCY_COMPACTION_RETURNED`

Then STOP.

Do not restart SR07 or SR08. HQ adjudicates R4 first.
