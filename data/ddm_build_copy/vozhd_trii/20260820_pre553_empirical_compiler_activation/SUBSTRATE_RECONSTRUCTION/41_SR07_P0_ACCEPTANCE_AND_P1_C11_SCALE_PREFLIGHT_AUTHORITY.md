# SR07 — P0 ACCEPTANCE AND P1 BOUNDED C11 SCALE PREFLIGHT AUTHORITY

Status: `SR07_P0_ACCEPTED__P1_C11_SCALE_PREFLIGHT_AUTHORIZED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Accepted SR07-P0 branch: `agent/vozhd-trii-sr07-p0-wvs7-scale`

Accepted SR07-P0 return commit: `04500195fc024d88831e4f95982afcbf585374c6`

Exact P0 starting HEAD: `55d0a848f73faf2df8dfd07aefadf716671578d0`

## 1. P0 adjudication

HQ accepts the SR07-P0 WVS Wave 7 real-source physical scale preflight.

Publication is exactly one commit ahead of the mandated P0 starting HEAD and changes exactly four files, all under:

`SUBSTRATE_RECONSTRUCTION/SR07_P0_WVS7_SCALE_PREFLIGHT/`

Accepted exact source:

- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- rows: `97220`
- variables: `613`
- physical cells: `59595860`
- decoder: `decode_sav(source_path)`
- encoding override: none
- reader path: ordinary metadata-first + chunked SAV reads

Accepted bounded replay facts:

- 2048-row cell count: `1255424`
- 8192 digest: `41864260dd8e2f9e8911ef4a3101d1fa9546405772a72ee294a36798fa2882ae`
- 32768 digest: same
- restart digest: same
- batch-size equality: true
- restart equality: true
- metadata/open wall time: about 1.642 s
- metadata/open RSS: about 15.7 MB -> 94.9 MB
- peak measured bounded-pass RSS: about 131.0 MB
- projected full physical traversal: about 14.82-28.52 minutes, explicitly projection only

P0 also proves Q152-Q157 retain nonempty source-native SPSS missing declarations and that required metadata for D_INTERVIEW, I_PSU, W_WEIGHT and S018 remains physically visible without semantic interpretation.

P0 proves the accepted SR06 decoder can enter and deterministically replay bounded WVS7 physical incidence at acceptable resource cost.

P0 does **not** certify WVS7 and does not establish respondent identity semantics, country-local mapping, weight/design roles, routing/applicability, semantic response-state authority or source-document meaning.

## 2. Why P1 is required before full certification

Authority 35 explicitly deferred one scale risk to the proving-source gates: existing `C11SourceReleaseCandidate` / `C11LogicalRelease` APIs use materialized tuple inventories and had only been exercised synthetically.

WVS7 contains `59,595,860` source cells. A naive one-Python-object-per-cell full candidate could create an uncontrolled memory wall even though the ordinary SAV decoder itself is bounded and chunked.

Therefore full SR07 certification is **not yet authorized**.

P1 must measure the real accepted path:

`exact WVS7 bytes -> accepted physical decoder -> explicit execution-only source-bound projection -> existing validate_c11_source_release() -> accepted Parquet carrier -> full reopen -> direct DuckDB`

at bounded row prefixes under a hard resource tripwire.

P1 is execution-scale evidence only. It creates no reusable WVS7 semantic authority and performs no source certification.

## 3. Exact P1 source and runtime

Use only ChatGPT Library transport:

`WVS Wave 7.sav.zip`

Extract only `WVS Wave 7.sav` and verify exact SHA-256:

`2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Use the accepted control-line runtime unmodified.

Required decoder invocation:

`decode_sav(source_path)`

No encoding override.

No production runtime changes are authorized in P1.

## 4. P1 execution-only projection law

The P1 harness may construct the minimum lawful source-bound C11 candidate necessary to exercise the existing I02 path at scale.

Any authority snapshots created by the harness must be explicitly scoped and named as:

`P1_EXECUTION_ONLY__NO_SOURCE_SEMANTIC_CERTIFICATION`

They may authorize only the mechanics needed to validate the bounded test candidate. They may not be reused as WVS7 source authority or cited as certification evidence for respondent identity, country meaning, routing, weight role, semantic missingness or label/document semantics.

Required preservation in each bounded candidate:

- exact source SHA;
- source row ordinal as hard replay identity;
- exact source variable ordinal/name;
- exact raw storage value;
- exact physical missing state;
- exact source missing declaration where present;
- raw value-label material where the existing C11 raw-value representation can lawfully retain it;
- no canonical question/value mapping unless already mechanically identity-preserving and explicitly non-semantic;
- no native-ID hard-key claim;
- no default weight selection;
- no routing inference from missingness;
- no country-local code semantic mapping;
- Q152/153, Q154/155 and Q156/157 remain distinct ordered source variables;
- W_WEIGHT and S018 remain distinct raw candidates;
- I_PSU source-declared physical state is not converted to row absence.

Where the accepted C11 object model requires a semantic response state but no source semantic authority exists, use only an existing explicitly unresolved state such as `INVALID_UNRESOLVED`; do not invent meaning.

If the existing I02 contract cannot lawfully represent the required physical distinctions without semantic invention, stop with:

`P1_BLOCKED__FROZEN_C11_PHYSICAL_PRESERVATION_CONTRADICTION`

Do not redesign I01-I07 in this worker.

## 5. Hostile physical-state microproof

Before scale escalation, locate at least one actually observed SPSS user-missing cell among Q152-Q157 using the accepted decoder path.

Pass that exact physical cell through the same execution-only projection used by the bounded candidate and prove its representation retains enough exact material to distinguish:

- the raw source value;
- `FORMAT_USER_MISSING_VALUE` or `FORMAT_USER_MISSING_RANGE` as actually emitted;
- the source-native declaration/range;
- row ordinal;
- variable ordinal/name.

Do not infer semantic DK/refusal/not-applicable meaning.

If the projection collapses the physical missing class/declaration into generic null/missing or loses the raw value, terminate with:

`P1_BLOCKED__FROZEN_C11_PHYSICAL_PRESERVATION_CONTRADICTION`

## 6. Bounded prefix stages

All stages use **all 613 source variables** for the exact first N physical source rows.

The stage sizes are chosen to be approximately event-frontier comparable to SR08-P1.

Required stages:

| stage | rows | expected cell/event frontier |
|---|---:|---:|
| S1 | 32 | 19,616 |
| S2 | 128 | 78,464 |
| S3 | 512 | 313,856 |

Optional S4:

| stage | rows | expected cell/event frontier |
|---|---:|---:|
| S4 | 1024 | 627,712 |

S4 may run only if S3 completes below all tripwires and measured scaling remains stable enough that S4 is useful.

Do **not** run a 2048-row I02 materialization merely because physical P0 used 2048 rows.

Do **not** run the full 97,220-row candidate.

## 7. Hard resource tripwire

Run each stage in a fresh child process supervised by a parent or equivalent external monitor.

The supervisor must sample child RSS and terminate the stage before uncontrolled growth if RSS reaches:

`4 GiB`

A killed stage is evidence, not a harness failure.

After every completed stage record:

- baseline RSS after decoder open;
- peak RSS during candidate construction;
- peak RSS during I02 validation;
- peak RSS during Parquet persistence;
- peak RSS during full reopen;
- final RSS after disposal + GC;
- wall time for each phase;
- exact object-family counts;
- canonical Parquet disk bytes;
- semantic release hash;
- relation digests;
- direct-DuckDB count checks.

Before advancing to the next stage, stop if either:

1. the 4 GiB tripwire was reached; or
2. linear/measured extrapolation indicates full-source materialization would plainly require unsafe memory for this machine.

Do not hide a memory wall by swapping, disabling the tripwire, or silently changing the C11 representation.

## 8. Determinism proof

Repeat S2 from a fresh decoder/process and require:

- identical exact source SHA;
- identical bounded row/cell frontier;
- identical semantic release hash;
- identical logical relation digests;
- identical public/internal object-ref inventories.

Parquet byte identity should be reported if deterministic, but semantic/logical identity is the dispositive P1 requirement.

## 9. Same-path requirement

P1 must use the actual accepted production functions for:

- physical decoding;
- physical-to-I02 bridge where applicable;
- `validate_c11_source_release()`;
- `ParquetC11Carrier.persist()`;
- `ParquetC11Carrier.reopen()`;
- `VerifiedDuckDBSession` or `open_direct_session()`.

A fake sizing loop that allocates arbitrary Python objects is insufficient.

P1 may use a worker-private scratch driver to orchestrate these functions. The driver must not modify `rawlsing_next/**`; its exact SHA-256 must be recorded in the receipt.

## 10. Direct DuckDB checks

For each completed stage, after persistence open the accepted verified in-memory DuckDB session and prove at minimum:

- respondent-event row count equals the bounded event frontier represented by the candidate;
- release identity is exact;
- no persistent `.duckdb` file exists;
- no PostgreSQL/SQLite/DATABASE_URL path is used.

## 11. Full-source projection

Using measured stage data, produce clearly labeled projections for full WVS7 (`97,220 x 613 = 59,595,860` cells) covering:

- candidate-build peak RSS;
- I02 validation peak RSS;
- full reopen peak RSS;
- persistent Parquet disk;
- candidate-build wall time;
- validation wall time;
- persistence wall time;
- reopen wall time.

Every extrapolation must be labelled `PROJECTION_ONLY` and show the basis/stage used.

## 12. Allowed P1 dispositions

Exactly one:

- `P1_PASS__FULL_CERTIFICATION_EXECUTION_SCALE_ACCEPTABLE`
- `P1_BLOCKED__I02_MATERIALIZATION_SCALE`
- `P1_BLOCKED__PARQUET_ROUNDTRIP_SCALE`
- `P1_BLOCKED__RESOURCE_TRIPWIRE`
- `P1_BLOCKED__FROZEN_C11_PHYSICAL_PRESERVATION_CONTRADICTION`
- `P1_BLOCKED__RUNTIME_CONTRACT_MISMATCH`
- `P1_BLOCKED__SOURCE_OR_LIBRARY_IDENTITY`

A P1 block is fail-closed evidence for HQ. It does not authorize representation redesign by the worker.

## 13. Outputs

Write only small evidence artifacts under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR07_P1_WVS7_C11_SCALE_PREFLIGHT/`

Required:

- `P1_RECEIPT.json`
- `STAGE_MEASUREMENTS.json`
- `PROJECTION_ONLY.json`
- `P1_RESULT.md`

Do not commit raw source bytes, Parquet carriers, scratch drivers, giant logs or extracted SAV files.

## 14. Required return token

`PRE553_SR07_P1_WVS7_C11_SCALE_PREFLIGHT_RETURNED`

## 15. Gate state

`G-SR07 = P1_C11_SCALE_PREFLIGHT_AUTHORIZED`

Full WVS7 certification remains blocked pending HQ adjudication of P1.
