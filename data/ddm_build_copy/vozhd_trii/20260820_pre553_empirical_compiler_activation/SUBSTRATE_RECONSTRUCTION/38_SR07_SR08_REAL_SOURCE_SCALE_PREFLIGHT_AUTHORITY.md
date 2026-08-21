# SR07 / SR08 — REAL-SOURCE SCALE PREFLIGHT AUTHORITY

Status: `AUTHORIZED__P0_SCALE_PREFLIGHT_ONLY`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

G-SR06 closure: `37_SR06_FINAL_ACCEPTANCE_AND_PROVING_SOURCE_RELEASE.md`

Accepted SR06 implementation lineage culminates at runtime commit:

`606813b01021eb2555017e028d5742b1e6f12e94`

and is integrated into the control line.

## 1. Purpose

Run two parallel bounded real-source P0 courts before any full proving-source C11 materialization:

- SR07-P0: WVS Wave 7 SAV;
- SR08-P0: LiTS I DTA.

P0 answers only:

1. do the exact real bytes enter the accepted SR06 decoder path successfully?
2. are source/metadata identities deterministic?
3. is bounded physical incidence replay stable across batch sizes?
4. what real memory/time behavior does the accepted reader path exhibit?
5. is there any immediate execution-scale contradiction that must be adjudicated before full I02 materialization?

P0 does **not** certify source semantics or C11 information-equivalence.

## 2. Exact source inputs

### SR07-P0 — WVS Wave 7

Library transport artifact:

`WVS Wave 7.sav.zip`

Exact extracted source SHA-256:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Frozen expected physical shape:

- rows: `97220`
- variables: `613`
- reader path: ordinary SAV metadata-first + chunked data read
- encoding override: none

Hostile metadata expected to remain visible includes at least:

- Q152-Q157 SPSS user-missing declarations;
- D_INTERVIEW;
- I_PSU;
- W_WEIGHT;
- S018.

No semantic ruling follows from those names.

### SR08-P0 — LiTS I

Library transport artifact:

`LiTS_I.dta.zip`

Exact extracted source SHA-256:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Frozen expected physical shape:

- rows: `29002`
- variables: `1198`
- reader path: exact-SHA compatibility full-read exception
- required compatibility encoding: `latin1`
- authority status: `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

Hostile metadata expected to remain visible includes at least:

- native `id`;
- `weight_0`;
- `weight_1`;
- `weight_2`;
- q301-family variables when present in metadata;
- ordinary labeled nonresponse-like codes remain physically ordinary.

No text-encoding or semantic authority is inferred from successful Latin-1 compatibility execution.

## 3. Library/input law

Each worker must:

1. locate the exact named ChatGPT Library artifact;
2. materialize it to worker-private scratch;
3. record ZIP byte size and SHA-256;
4. extract only the assigned source file;
5. verify the extracted source SHA-256 exactly;
6. keep Library/raw bytes immutable;
7. perform all outputs in worker-private `/private/tmp` or equivalent scratch.

If Library materialization is unavailable or source SHA mismatches, fail closed.

Do not silently substitute an unrelated local copy.

## 4. P0 bounded execution procedure

Use only the accepted runtime from the worker checkout:

- `rawlsing_next/pre553_physical_decoder.py`
- no local decoder patching;
- no source-specific semantic code.

### P0-A — source + metadata open

Instantiate the exact decoder:

- WVS7: `decode_sav(source_path)`
- LiTS I: `decode_dta(source_path, encoding="latin1")`

Record:

- source SHA from decoder;
- row count;
- variable count;
- reader configuration;
- file metadata;
- metadata/open wall time;
- process RSS before decode;
- RSS after decoder construction;
- peak RSS observed during decoder construction.

Fail closed if exact SHA or frozen row/variable shape differs.

### P0-B — metadata contract probe

Without semantic interpretation, emit a compact exact metadata receipt for the named hostile variables above:

- variable ordinal;
- storage type;
- variable label as physically decoded;
- value-label count;
- physical missing declarations;
- display metadata;
- topology/MR metadata physically exposed.

For WVS7 prove Q152-Q157 retain nonempty source-native missing declarations.

For LiTS I prove `reader_configuration.encoding == "latin1"` and exact compatibility-only authority status is retained.

Do not decide what labels mean.

### P0-C — bounded physical-cell replay

Freeze:

`PREFLIGHT_ROW_LIMIT = 2048`

For each source, consume physical cells only until all variables for physical source rows 1..2048 have been emitted.

Run the bounded consumption twice using two requested cell batch sizes:

- `8192`
- `32768`

For each pass compute one streaming SHA-256 over canonical JSON lines containing exactly:

- source_sha256
- row_ordinal
- variable_ordinal
- variable_name
- raw_value
- missing_state
- source_missing_declaration
- raw_value_label

Do not retain all cells merely to calculate the digest.

Expected consumed cell count:

- WVS7: `2048 * 613 = 1,255,424`
- LiTS I: `2048 * 1198 = 2,453,504`

Required:

- both passes consume exactly the expected cell count;
- both digests are identical;
- first emitted row ordinal = 1;
- last emitted row ordinal = 2048;
- variable ordinal range is exactly 1..N;
- no complete source-cell tuple/list is materialized.

Record wall time, cells/sec, RSS before/after and peak RSS for each pass.

For LiTS I, note that the compatibility decoder may already retain the full reader DataFrame. The bounded cell pass must not create a second complete cell-object universe.

### P0-D — deterministic restart

Destroy the first decoder object, force ordinary Python garbage collection, instantiate the exact decoder again from the same source bytes, and repeat one `8192` bounded digest pass.

Required:

- source SHA identical;
- metadata shape identical;
- bounded physical digest identical to P0-C;
- reader configuration identical.

### P0-E — execution-scale assessment

Produce measured, non-semantic estimates only:

- actual metadata/open RSS delta;
- actual bounded-pass peak RSS;
- actual cells/sec;
- linear full-source physical-cell traversal time projection, clearly labelled `PROJECTION_ONLY`;
- whether observed memory behavior is stable/bounded during the physical-cell pass;
- whether the compatibility full-read frame dominates LiTS-I memory;
- whether any unexpected full-frame materialization occurs for WVS7.

Do **not** estimate full C11 object memory by inventing an object-per-cell multiplier.

The correct P0 output may be `BLOCKED_SCALE_PREFLIGHT` if observed behavior makes safe full certification implausible.

## 5. Forbidden in P0

Do not:

- build a complete `C11SourceReleaseCandidate` for the source;
- build/persist a complete `C11LogicalRelease`;
- call full source certification;
- create source semantic authority;
- classify label meanings as DK/refusal/not-applicable/etc.;
- select a preferred weight;
- infer country semantics;
- run I03/I05 discovery over the source;
- use legacy PostgreSQL;
- use `DATABASE_URL`;
- modify `rawlsing_next/**`;
- modify raw source bytes;
- scan unrelated CLOSED_35 sources.

## 6. Worker return artifacts

Each worker writes only its own return directory:

SR07-P0:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR07_P0_WVS7_SCALE_PREFLIGHT/`

SR08-P0:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR08_P0_LITS1_SCALE_PREFLIGHT/`

Required small committed artifacts:

- `P0_RECEIPT.json`
- `HOSTILE_METADATA_RECEIPT.json`
- `RESOURCE_MEASUREMENTS.json`
- `P0_RESULT.md`

No raw data, extracted source, Parquet carrier, giant stdout, or large empirical result is committed.

`P0_RECEIPT.json` must contain at least:

- worker starting HEAD;
- exact source SHA;
- exact source shape;
- reader configuration;
- first-pass digest;
- second-batch-size digest;
- restart digest;
- consumed cell counts;
- timings;
- RSS measurements;
- explicit booleans for every required P0 assertion;
- final disposition.

Allowed dispositions:

- `P0_PASS__FULL_CERTIFICATION_MAY_BE_ADJUDICATED`
- `BLOCKED_SCALE_PREFLIGHT`
- `BLOCKED_SOURCE_IDENTITY_MISMATCH`
- `BLOCKED_DECODER_CONTRACT_MISMATCH`
- `BLOCKED_LIBRARY_INPUT_UNAVAILABLE`

## 7. Completion tokens

SR07-P0:

`PRE553_SR07_P0_WVS7_SCALE_PREFLIGHT_RETURNED`

SR08-P0:

`PRE553_SR08_P0_LITS1_SCALE_PREFLIGHT_RETURNED`

HQ must adjudicate the two returns separately.

No full SR07/SR08 certification execution is authorized by this file.
