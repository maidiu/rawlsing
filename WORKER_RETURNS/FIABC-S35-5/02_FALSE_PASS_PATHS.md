# FIABC-S35-5 — False-PASS Paths and Exact Universality Gaps

Terminal target: `FIABC_S35_5_DIFFERENTIAL_SOURCE_UNIVERSALITY_HOSTILELY_TESTED`

Repository: `maidiu/rawlsing`  
Base: `agent/vozhd-premain-fiabc-wave3-fanin-r1` @ `6c6e43527da7f688a0fbe1c2fa960bfe79dfffcc`

## Claim under attack

> The current A/B/C architecture can be made source-neutral across all 35 simply because canonical source hashes are known.

That claim does not survive the current contracts.

A canonical raw SHA solves one necessary question:

`WHICH RAW BYTE SNAPSHOT IS THE ROOT?`

It does not solve:

- whether a derivative was actually produced from that root;
- which reader/configuration produced its physical incidence;
- whether display metadata, value dictionaries, missing declarations, MR topology, rank/order, forms, routing, identifiers and all-missing columns survived;
- whether a source-specific projection exists;
- whether documentary authority is sufficient to interpret the preserved physical facts;
- whether all three candidates consume information-equivalent physical realizations;
- whether the comparison terminal covers every source-native information class required for source certification.

The current architecture is substantially stronger than filename or row-count equivalence, but it is **claim-scoped semantic parity over LiTS-I and WVS7**, not a CLOSED_35 source-equivalence court.

## 1. Universality is presently mechanically impossible for 33 sources

The current Candidate-C production registry contains exactly:

- `LITS_I`;
- `WVS7`.

Every other source raises `unadmitted Candidate-C source`.

The current succession governing profile likewise freezes the court to:

`sources = [LITS_I, WVS7]`

and the exact claim:

`P2X_LITS_I_WVS7_RAW_SOURCE_LOCAL_WORKLOAD`.

A 35-source / 105-cell A/B/C manifest therefore cannot pass the current P01/P08 preflight. This is not a defect in the two-source court; it is a direct falsifier of the claim that the current architecture is already source-neutral across 35 because the SHA registry exists.

Authority72 does not bridge this. It contains one L0 source, twenty-six L1 sources and seven L2 sources. It explicitly does not certify any of them or mint current production projections.

## 2. Hash equality at the derivative boundary is not parentage

The generic common facade accepts two physical transport classes:

- `PhysicalSourceIncidence`;
- `ExactPhysicalCellStream`.

A direct `PhysicalSourceIncidence` produced by the frozen decoder is strong at the raw boundary because the decoder hashes the actual opened file.

`ExactPhysicalCellStream`, however, contains:

- a declared `source_sha256`;
- a row count;
- a cell iterator;
- a transport identity.

It contains no proof that the iterator was generated from the byte snapshot whose SHA it declares.

The facade checks:

`stream.source_sha256 == projection.expected_source_sha256`

and then requires physical completeness only for **the slots named by the projection**.

Therefore a derivative can be terminal-valid while failing whole-source ancestry or information-equivalence.

### False-PASS path FP-01 — projected-only derivative

1. Construct an `ExactPhysicalCellStream`.
2. Set `source_sha256` to the canonical root.
3. Supply every row for every projected slot.
4. Omit unprojected source variables or metadata.
5. Produce exactly the expected C11/I03/I05 terminal.

The common facade can accept this stream. The P2 oracle can also accept the candidate if all compared semantic dimensions match.

That is a valid **bounded workload realization** only if separately governed as such. It is not proof that the candidate consumed an information-equivalent realization of the canonical source.

The false inference is:

`P2 TERMINAL PARITY -> WHOLE SOURCE PARITY`.

Current law does not authorize that inference, but a CLOSED_35 universality claim based only on hashes would make it.

## 3. Candidate A preserved-carrier validation is strong internally and weak on raw ancestry

The frozen Route-A adapter performs a serious carrier audit:

- carrier schema and typed codec identity;
- source-artifact-ref SHA;
- source metadata SHA;
- exact variable ordinal/name inventory;
- exact row × variable cell cardinality;
- canonical ordering;
- logical stream digest;
- physical-root integrity.

This mechanically catches a carrier that honestly declares a different source SHA.

But the adapter does not reopen the raw source and does not prove a build receipt from raw bytes at consumption time.

More sharply, `_validate_metadata(...)` decodes:

- `reader_configuration`;
- `file_metadata`;

checks that they are mappings, and then returns only:

- source SHA;
- row count;
- variable count.

Likewise the variable validator syntactically decodes labels, display metadata and topology metadata but the physical descriptor reduces variables to ordinal/name pairs.

### False-PASS path FP-02 — preserved carrier with metadata drift

A self-consistent carrier can retain:

- canonical source SHA;
- canonical row count;
- canonical variable count;
- canonical projected cell values;

while carrying a different:

- reader configuration;
- file encoding metadata;
- display metadata;
- value-label dictionary;
- MR/topology metadata.

If those differences do not alter the frozen projection or I03/I05 workload, the current P2 comparison terminal has no dimension on which to reject them.

This is particularly relevant to Authority72 hazards such as:

- EVS 1999/2008 compatibility text;
- Asian Barometer W5 native MR sets;
- EVS 2008/2017 MR sets;
- WVS1 display-formatted IDs;
- WVS4 equal vectors with distinct dictionaries;
- all-system or all-user-missing columns.

Again: this can be a lawful workload-scoped reuse if separately authorized. It cannot establish CLOSED_35 physical universality.

## 4. Reader configuration is not determined by source SHA

The decoder's compatibility allowlist binds six exact SHA values to `latin1`, including EVS 1999, EVS 2008 and LiTS I-IV.

However `_compatibility_config(source_sha, encoding)` treats `encoding=None` as valid and returns no compatibility authority status. It rejects a *wrong explicit override* but does not itself require the frozen override whenever the SHA is allowlisted.

The format contract is stricter: exact reader configuration must be frozen per source and used deterministically; compatibility execution remains physical-only and must not become source-text authority.

Current LiTS P2 live code separately closes this for LiTS-I by explicitly calling:

`decode_dta(..., encoding="latin1")`.

The other allowlisted sources are not current P2 sources.

### False-PASS path FP-03 — same SHA, different decode, terminal-invisible difference

If future 35-source admission merely keys on SHA:

1. Candidate A consumes a preserved carrier built under compatibility decoding.
2. Candidate B directly decodes the exact same bytes with default/native text handling.
3. Candidate C receives another derivative.
4. The different decoded text exists only in metadata or unprojected fields.
5. P2 semantic outputs remain equal.

A semantic parity PASS would not prove physical-reader equivalence.

## 5. The WVS structural preimage authenticates itself, not its parent

The WVS7 projection path can persist:

`wvs7_projection_structural_input.json`.

The direct creation path first hashes the real WVS7 SAV, then records:

- canonical source SHA;
- row count;
- variable count;
- physical variable names/ordinals;
- missing declarations;
- B_COUNTRY values;
- a `structural_input_identity`.

On a later source-free stage, `materialize_from_structural_input(...)` verifies:

- schema;
- self-hash;
- asserted canonical source SHA;
- row count;
- variable count.

It does not possess a separate parent receipt proving that this exact structural preimage was emitted by the earlier raw-file hashing operation.

### False-PASS path FP-04 — detached preimage, unprojected mutation

1. Copy or manufacture the structural JSON.
2. Retain the canonical WVS7 SHA field and geometry.
3. Alter metadata that does not affect the current projection/frontier.
4. Recompute `structural_input_identity`.
5. Reopen source-free.

The current terminal can remain identical.

If a changed B_COUNTRY/routing value affects P2, the independent oracle catches it later. If the change is outside terminal-visible semantics, the court can still pass while physical source equivalence is false.

## 6. Projection identity is authority identity, not a full projection-content checksum

`GovernedC11Projection.cache_identity` hashes:

- the contract;
- `projection_identity_ref`;
- source SHA;
- required authority refs;
- optional slot-owner authority sets.

It does **not** hash the complete:

- row bindings;
- response value tables;
- coordinate value tables;
- routing facts;
- weights;
- every projection field.

This is sensible if the projection object is only ever materialized through a trusted governed producer. It means the cache identity alone is not a proof that an arbitrary projection object equals the accepted projection preimage.

### False-PASS path FP-05 — same authority identity, terminal-invisible projection drift

An altered projection that preserves the accepted identity/authority refs can have the same `cache_identity`. If its differences change terminal facts, the oracle catches them. If they lie outside the current declared frontier, a P2 PASS can coexist with projection-content drift.

Therefore a 35-source universality argument cannot use:

`expected source SHA + expected projection cache identity`

as a substitute for full governed projection materialization lineage.

## 7. The comparison terminal is intentionally narrower than source certification

The Wave-3 governing profile terminates at:

`I05_LEARNED_EMPIRICAL_PRODUCT__WITH_EXACT_SEMANTIC_REPLAY_AND_OUTPUT_IDENTITY`.

The independent oracle compares:

- source identity;
- court constitution;
- semantic authority closure;
- projection/release refs;
- frontier;
- I03 fact manifest;
- I05 learned product;
- replay;
- exact refs;
- negative-state manifest.

The Source-Native Constitution's certification rule is broader:

> a source is certified only when replay proves information-equivalence for every source-native information class relevant under the constitution and accepted M01-M18 law.

The current P2 terminal does not independently compare every source-native variable, metadata field, MR-set definition, display format, label dictionary, unprojected missing declaration, or source-local routing structure.

### False-PASS path FP-06 — terminal equality plus hidden physical inequality

Any candidate differential that survives outside the declared semantic frontier can satisfy P2 parity while violating source-native equivalence.

This is the central universality gap. It is not a flaw in the P2 court. It is a scope error to promote a P2 PASS into a CLOSED_35 source-equivalence PASS.

## 8. Authority71/72 hazards defeat "SHA implies neutral realization"

The accepted 34-source synthesis contains hostile burdens that require source-specific decisions even after exact raw SHA is settled.

### Identity / display / replay hazards

Examples:

- Afrobarometer R1: REFNUMB/CASENUMB distinction;
- Arab Barometer W5: ID collisions;
- Arab Barometer W8: 2,400 ID=0 rows;
- Latinobarometro 1995: noninjective interview IDs;
- South Asia W1: no safe native ID;
- South Asia W2: resno collisions;
- WVS1: S007 display F2.0 versus 9-10 digit raw IDs.

Hash equality does not decide the respondent-identity law. The constitution therefore keeps source SHA + row ordinal as the irreducible replay identity.

### Missing-state hazards

Examples:

- Afrobarometer R5: 997 declarations versus system missing;
- Arab Barometer W2: system missing versus ordinary 0 labeled missing;
- Asian Barometer W1: heavy typed missingness;
- EVS 1981: positive user-missing value;
- EVS 1990: all-user-missing q745;
- LiTS-I: all-system repeated slot;
- WVS1/WVS4: all-system/all-row typed-missing columns.

A SHA identifies the file containing those distinctions. It does not prove each derivative kept them.

### Topology / MR / rank / form hazards

Examples:

- Asian Barometer W5: three native MR sets and Q112/SE15 overlap;
- EVS 2008: thirteen native MR sets;
- EVS 2017: MR sets plus matrix/mixed mode;
- GSS: split forms, ballots, versions, ordered household slots, two-phase samples;
- LiTS III: 308 PR + 308 SR namespaces;
- LiTS IV: 134 `*_skip` fields and ten visits.

A byte hash does not choose the lawful flattening rule. In many cases the lawful rule is **do not flatten**.

### Internal-structure hazards

Latinobarometro 2024 records:

`raw header nominal_case_size=174 vs 332 dictionary/stream`.

One canonical SHA contains the disagreement. Therefore SHA identity cannot determine which internal structural interpretation a candidate should use. That requires the prepared hostile fixture / governed physical rule.

### Compatibility-text hazards

EVS 1999 and EVS 2008 are L2 because compatibility decoding is physical execution only and producer-authoritative text repair/alignment is missing.

Same SHA, same reader success, and same row count still do not create text semantics.

### Documentary blockers

Seven Authority72 sources are L2:

- Afrobarometer R5;
- Afrobarometer R9;
- EVS 1999;
- EVS 2008;
- GSS 1972;
- GSS 1973;
- Latinobarometro 1995.

No mechanical source hash can manufacture the missing documentary authority.

## 9. Existing alternate exports show the differential-source problem is real

Historical loader manifests in the repository name alternate carriers/releases such as:

- Arab Barometer Wave 2: `ABII.dta`;
- Asian Barometer W5: `20230505_W5_merge_15.sav`;
- EVS 1981: `EVS 1981 ZA4438_v3-0-0.sav`;
- EVS 1999: `EVS 1999 ZA3811_v3-0-0.sav`;
- EVS multi-wave trend: `EVS 1981-2017 TREND ZA7503_v3-0-0.dta`;
- South Asia W1/W2: `SDSA 2005.sav` and `SDSA 2013.sav`.

Those historical manifests contain paths and dimensions but no exact SHA-to-canonical-root derivation chain. Thus "different export" is an observed estate condition, not an invented hostile abstraction.

## 10. What current law does catch

The hostile court should not erase the strong parts of the architecture.

Current law mechanically rejects:

- direct raw-byte SHA drift;
- projection/source SHA mismatch;
- missing explicit projection;
- incomplete projected slots;
- duplicate projected row/slot cells;
- unbound physical value/state keys;
- wrong explicit compatibility override;
- Candidate-C source names outside LiTS-I/WVS7;
- a 35-source manifest against the current two-source preflight;
- carrier corruption and internal source-SHA inconsistency;
- WVS direct-source structural reads whose SHA/shape differ.

Current law semantically catches later:

- projected-value differentials that alter C11;
- routing differences that alter frozen I03 facts;
- negative-state collapse;
- learned-product/frontier divergence;
- terminal/replay identity divergence.

The false-PASS zone is narrower:

> candidate physical realizations differ in ancestry or source-native information, but the difference lies outside every mechanically compared physical field and outside the frozen semantic comparison terminal.

## Exact universality gaps

The claim fails on the following exact missing implications:

1. `KNOWN_CANONICAL_SHA -> DERIVATIVE_PARENTAGE` is false.
2. `KNOWN_CANONICAL_SHA -> FROZEN_READER_CONFIG_USED_BY_EVERY_CANDIDATE` is false.
3. `KNOWN_CANONICAL_SHA -> FULL_SOURCE_METADATA_PRESERVED_IN_EVERY_DERIVATIVE` is false.
4. `KNOWN_CANONICAL_SHA -> SOURCE_SPECIFIC_PROJECTION_AUTHORITY` is false.
5. `KNOWN_CANONICAL_SHA -> ROUTING_TOPOLOGY_WEIGHT_DESIGN_AUTHORITY` is false.
6. `KNOWN_CANONICAL_SHA -> DOCUMENTARY_AUTHORITY` is false.
7. `PROJECTION_CACHE_IDENTITY -> FULL_PROJECTION_PREIMAGE_EQUALITY` is false without trusted producer lineage.
8. `EXACT_PHYSICAL_CELL_STREAM.source_sha256 -> RAW_BYTE_ANCESTRY` is false.
9. `P2_I05_PARITY -> WHOLE_SOURCE_INFORMATION_EQUIVALENCE` is false.
10. `CURRENT_TWO_SOURCE_A/B/C_CAPABILITY -> CLOSED_35_A/B/C_CAPABILITY` is false.

The controlling conclusion is therefore:

```text
canonical source hash
    is necessary
    but not sufficient for
candidate-neutral physical realization

and

P2 semantic parity
    is necessary for the current court
    but not sufficient for
CLOSED_35 source equivalence.
```
