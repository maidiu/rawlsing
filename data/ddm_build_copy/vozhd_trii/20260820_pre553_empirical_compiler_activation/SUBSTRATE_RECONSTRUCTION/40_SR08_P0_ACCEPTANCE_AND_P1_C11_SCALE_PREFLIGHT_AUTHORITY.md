# SR08 — P0 ACCEPTANCE AND P1 BOUNDED C11 SCALE PREFLIGHT AUTHORITY

Status: `SR08_P0_ACCEPTED__P1_C11_SCALE_PREFLIGHT_AUTHORIZED`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Accepted SR08-P0 branch: `agent/vozhd-trii-sr08-p0-lits1-scale`

Accepted SR08-P0 return commit: `0d55a8e4f8de83790df1bdca1889bd128677f381`

Exact P0 starting HEAD: `55d0a848f73faf2df8dfd07aefadf716671578d0`

## 1. P0 adjudication

HQ accepts the SR08-P0 LiTS I real-source physical scale preflight.

Publication is exactly one commit ahead of the mandated P0 starting HEAD and changes exactly four files, all under:

`SUBSTRATE_RECONSTRUCTION/SR08_P0_LITS1_SCALE_PREFLIGHT/`

Accepted exact source:

- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows: `29002`
- variables: `1198`
- physical cells: `34744396`
- decoder: `decode_dta(source_path, encoding="latin1")`
- authority state: `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

Accepted bounded replay facts:

- 2048-row cell count: `2453504`
- 8192 digest = `e4cde7d05884719c5ccdb93f025b0ee1cefa997c7ee5a6a4ea7165232f8a4f4c`
- 32768 digest = same
- restart digest = same
- batch-size equality = true
- restart equality = true
- compatibility full-read DataFrame shallow memory = about 265.08 MiB
- peak measured RSS = about 380232 KiB
- projected full physical traversal = about 328-343 seconds, explicitly projection only

P0 proves the accepted SR06 decoder can enter and deterministically replay bounded LiTS I physical incidence at acceptable resource cost.

P0 does **not** certify LiTS I and does not establish source-text encoding, respondent identity, country mapping, weight/design, routing/module or semantic response authority.

## 2. Why P1 is required before full certification

Authority 35 explicitly deferred one scale risk to the proving-source gates: existing `C11SourceReleaseCandidate` / `C11LogicalRelease` APIs use materialized tuple inventories and had only been exercised synthetically.

LiTS I contains `34,744,396` source cells. A naive one-Python-object-per-cell full candidate could create an uncontrolled memory wall even though the physical decoder itself is bounded.

Therefore full SR08 certification is **not yet authorized**.

P1 must measure the real accepted path:

`exact LiTS I bytes -> accepted physical decoder -> explicit execution-only source-bound projection -> existing validate_c11_source_release() -> accepted Parquet carrier -> full reopen -> direct DuckDB`

at bounded row prefixes under a hard resource tripwire.

P1 is execution-scale evidence only. It creates no reusable LiTS semantic authority and performs no source certification.

## 3. Exact P1 source and runtime

Use only ChatGPT Library transport:

`LiTS_I.dta.zip`

Extract only `LiTS_I.dta` and verify exact SHA-256:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Use the accepted control-line runtime unmodified.

Required decoder invocation:

`decode_dta(source_path, encoding="latin1")`

No production runtime changes are authorized in P1.

## 4. P1 execution-only projection law

The P1 harness may construct the minimum lawful source-bound C11 candidate necessary to exercise the existing I02 path at scale.

Any authority snapshots created by the harness must be explicitly scoped and named as:

`P1_EXECUTION_ONLY__NO_SOURCE_SEMANTIC_CERTIFICATION`

They may authorize only the mechanics needed to validate the bounded test candidate. They may not be reused as LiTS source authority or cited as certification evidence for respondent identity, country meaning, routing, weight role, semantic missingness or text encoding.

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
- no country-code semantic mapping;
- no promotion of latin1 compatibility execution into text authority.

Where the accepted C11 object model requires a semantic response state but no source semantic authority exists, use only an existing explicitly unresolved state such as `INVALID_UNRESOLVED`; do not invent meaning.

If the existing I02 contract cannot lawfully represent the required physical distinctions without semantic invention, stop with:

`P1_BLOCKED__FROZEN_C11_PHYSICAL_PRESERVATION_CONTRADICTION`

Do not redesign I01-I07 in this worker.

## 5. Bounded prefix stages

All stages use **all 1198 source variables** for the exact first N physical source rows.

Required stages:

| stage | rows | expected cell/event frontier |
|---|---:|---:|
| S1 | 16 | 19,168 |
| S2 | 64 | 76,672 |
| S3 | 256 | 306,688 |

Optional S4:

| stage | rows | expected cell/event frontier |
|---|---:|---:|
| S4 | 512 | 613,376 |

S4 may run only if S3 completes below all tripwires and measured scaling remains stable enough that S4 is useful.

Do **not** run 2048-row I02 materialization merely because the physical P0 used 2048 rows.

Do **not** run the full 29,002-row candidate.

## 6. Hard resource tripwire

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

## 7. Determinism proof

Repeat S2 from a fresh decoder/process and require:

- identical exact source SHA;
- identical bounded row/cell frontier;
- identical semantic release hash;
- identical logical relation digests;
- identical public/internal object-ref inventories.

Parquet byte identity should be reported if deterministic, but semantic/logical identity is the dispositive P1 requirement.

## 8. Same-path requirement

P1 must use the actual accepted production functions for:

- physical decoding;
- physical-to-I02 bridge where applicable;
- `validate_c11_source_release()`;
- `ParquetC11Carrier.persist()`;
- `ParquetC11Carrier.reopen()`;
- `VerifiedDuckDBSession` or `open_direct_session()`.

A fake sizing loop that allocates arbitrary Python objects is insufficient.

P1 may use a worker-private scratch driver to orchestrate these functions. The driver must not modify `rawlsing_next/**`; its exact SHA-256 must be recorded in the receipt.

## 9. Direct DuckDB checks

For each completed stage, after persistence open the accepted verified in-memory DuckDB session and prove at minimum:

- respondent-event row count equals the bounded event frontier represented by the candidate;
- release identity is exact;
- no persistent `.duckdb` file exists;
- no PostgreSQL/SQLite/DATABASE_URL path is used.

## 10. Full-source projection

Using measured stage data, produce clearly labeled projections for full LiTS I (`29,002 x 1,198 = 34,744,396` cells) covering:

- candidate-build peak RSS;
- I02 validation peak RSS;
- full reopen peak RSS;
- persistent Parquet disk;
- candidate-build wall time;
- validation wall time;
- persistence wall time;
- reopen wall time.

Every extrapolation must be labelled `PROJECTION_ONLY` and show the basis/stage used.

## 11. Allowed P1 dispositions

Exactly one:

- `P1_PASS__FULL_CERTIFICATION_EXECUTION_SCALE_ACCEPTABLE`
- `P1_BLOCKED__I02_MATERIALIZATION_SCALE`
- `P1_BLOCKED__PARQUET_ROUNDTRIP_SCALE`
- `P1_BLOCKED__RESOURCE_TRIPWIRE`
- `P1_BLOCKED__FROZEN_C11_PHYSICAL_PRESERVATION_CONTRADICTION`
- `P1_BLOCKED__RUNTIME_CONTRACT_MISMATCH`
- `P1_BLOCKED__SOURCE_OR_LIBRARY_IDENTITY`

A P1 block is fail-closed evidence for HQ. It does not authorize representation redesign by the worker.

## 12. Outputs

Write only small evidence artifacts under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR08_P1_LITS1_C11_SCALE_PREFLIGHT/`

Required:

- `P1_RECEIPT.json`
- `STAGE_MEASUREMENTS.json`
- `PROJECTION_ONLY.json`
- `P1_RESULT.md`

Do not commit raw source bytes, Parquet carriers, scratch drivers, giant logs or extracted DTA files.

## 13. Required return token

`PRE553_SR08_P1_LITS1_C11_SCALE_PREFLIGHT_RETURNED`

## 14. Gate state

`G-SR08 = P1_C11_SCALE_PREFLIGHT_AUTHORIZED`

Full LiTS I certification remains blocked pending HQ adjudication of P1.
