# CLOSED35 Representation Census — Output Schema and Classification Law

Status: `FROZEN_FOR_SOURCE_FREE_QUALIFICATION`

## Physical-only boundary

The harness measures this chain and nothing above it:

`canonical bytes -> accepted decoder/config -> Python physical token -> physical missing state -> source missing declaration -> PRE553_R5_TYPED_VALUE_CODEC -> PRE553_PHYSICAL_VALUE_BINDING@2.0.0 key -> exact governed owner/rule join`.

Labels, frequencies, neighboring values, missingness density, field names, display formatting, native-ID uniqueness, weight magnitude, and routing incidence do not mint semantics.

## Frozen source and surface counts

- canonical sources: **35**
- SAV: **31**
- DTA: **4**
- governed variable surfaces enumerated before source execution: **34**
- surfaces with an exact bounded/native-literal value owner: **14**
- governed item surfaces whose exact physical value-key owner is not presently enumerated: **20**

The 20 owner-incomplete surfaces are deliberately retained so a governed question/item cannot be silently upgraded into a governed typed key. Their lawful typed-join disposition is `TYPED_JOIN_BLOCKED_BY_MISSING_AUTHORITY` unless a later explicit authority supersedes this registry.

## Classification enum

Exactly one of the following is emitted for each governed surface observation:

- `EXACT_EXISTING_REGIME_APPLIES`: current typed physical representation joins the governed owner exactly.
- `EXACT_BOUNDED_SUCCESSOR_BRIDGE_APPLIES`: an already-authorized source/variable/type/token-bounded successor bridge closes the exact join. LiTS-I q301_2/q301_7 are the positive control.
- `NEW_GENERIC_REPRESENTATION_REGIME_REQUIRED`: exact typed join fails in a way matching a reusable physical regime candidate; this is a measurement classification, not HQ adoption.
- `SOURCE_BOUNDED_REPRESENTATION_BRIDGE_REQUIRED`: exact typed join fails in a source/variable-specific physical way not lawfully generalized.
- `TYPED_JOIN_BLOCKED_BY_MISSING_AUTHORITY`: bytes may be measurable, but the exact governed physical-value owner/key authority is incomplete.
- `SOURCE_BYTES_UNAVAILABLE`: no exact canonical source bytes were available for that source ID or the supplied path failed the canonical SHA gate.

No classification authorizes numeric equality, semantic remapping, response portability, routing inference, weight use, or architecture selection.

## Noncollapse law

The current R5 codec and physical-key contract remain authoritative. The harness must preserve distinct:

- Python `int` versus `float`;
- `float` versus `Decimal`;
- `Decimal("1")` versus `Decimal("1.0")`;
- string versus bytes;
- blank string versus null/system missing;
- physical missing-state enums;
- source missing declarations;
- display metadata versus raw storage;
- label text versus raw value.

A non-authoritative diagnostic may identify that an integer rule literal has a float64 representation candidate. That diagnostic may justify `NEW_GENERIC_REPRESENTATION_REGIME_REQUIRED`; it **never** counts as an exact join.

## Per-source immutable receipt

Each completed source writes:

`source_receipts/SOURCE_<NN>_REPRESENTATION_RECEIPT.json`

Schema: `CLOSED35_SOURCE_REPRESENTATION_RECEIPT@1.0.0`.

Required content includes source ID/SHA, exact runtime facts, manifest fingerprint, decoder lane, metadata/shape witnesses when bytes are available, surface observations, typed R5 tokens, missing-state/declaration material, exact binding keys, classifications, edge-preservation witnesses, and explicit semantic/nonexecution boundaries.

Existing receipts are immutable. An identical rerun resumes them without reopening the source. Input drift against an existing receipt is a global integrity failure.

## Aggregate authoritative-run outputs

- `CLOSED35_REPRESENTATION_OBSERVATIONS.json` — schema `CLOSED35_REPRESENTATION_OBSERVATIONS@1.0.0`
- `CLOSED35_TYPED_JOIN_MATRIX.csv`
- `CLOSED35_EDGE_PRESERVATION_RECEIPT.json` — schema `CLOSED35_EDGE_PRESERVATION_RECEIPT@1.0.0`
- `CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json` — schema `CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE@1.0.0`
- `CLOSED35_RUNTIME_RECEIPT.json` — schema `CLOSED35_RUNTIME_RECEIPT@1.0.0`
- `CLOSED35_CENSUS_SUMMARY.json` — schema `CLOSED35_CENSUS_SUMMARY@1.0.0`

These files are derived only from completed immutable source receipts and the frozen runtime/dependency audits. The harness contains no pre-populated source observations.

## Failure containment

Source-local failure writes a BLOCKED receipt and the census continues. A failure at source 23 therefore leaves source 01–22 receipts valid and allows source 24 onward to run.

Global court-integrity failures stop the pass immediately. They include:

- runtime mismatch;
- malformed/forked source registry;
- malformed/forked surface registry;
- repository/qualification guard failure;
- historical key dependency provenance failure.

## Edge-preservation law

Every source receipt carries all applicable S35 edge classes EC01–EC14 and the accepted physical hazard/UNKNOWN description. The census reports physical preservation only.

Special executable witnesses:

- Latinobarometro 2024: raw SAV nominal case-size witness `174` remains distinct from normalized dictionary/data width `332`; otherwise emit `GENERIC_RAW_HEADER_METADATA_CARRIER_GAP`.
- Asian Barometer W1: explicit BIG-5 candidate lane; current generic decoder admission gap is `GENERIC_SAV_DECLARED_ENCODING_ADMISSION_GAP`, never encoding guesswork.
- EVS 1981/1990: explicit WINDOWS-1252 candidate lanes are handled under the same generic declared-encoding admission debt; no source-specific semantic adapter is minted.

## Historical dependency law

Every key-producing dependency is tagged as one of:

- `HISTORICAL_PINNED`
- `CURRENT_SUCCESSOR_PINNED`
- `PINNED_EXTERNAL_EVIDENCE_IN_AUTHORITY`

Any ambient current dependency in a historical key path is a global failure. The LiTS legacy key path pins the historical facade, historical canonicalize/semantic-hash dependency, and historical missing-state enum separately rather than treating one old facade file as a complete historical environment.

## Runtime result boundary

The authoritative measurement is permitted only under Darwin / x86_64 / CPython 3.11.3 / pyreadstat 1.3.6 / pyarrow 25.0.1. The runner and the Python harness each independently enforce the gate before source observation.
