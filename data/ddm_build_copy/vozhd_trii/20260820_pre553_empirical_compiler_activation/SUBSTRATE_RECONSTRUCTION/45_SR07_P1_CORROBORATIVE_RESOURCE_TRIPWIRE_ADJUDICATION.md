# SR07 P1 CORROBORATIVE RESOURCE-TRIPWIRE ADJUDICATION

Status: `ACCEPTED_CORROBORATIVE_SCALE_FAILURE__SR07_BLOCKED_ON_G_SR06_RELATIONAL_SCALE_CORRECTION`

Repository: `maidiu/rawlsing`

Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

Accepted SR07-P1 branch: `agent/vozhd-trii-sr07-p1-wvs7-c11-scale`

Accepted return commit: `19bae3eff94dbfd39aeeff9ca2ea0720d8a8682a`

Frozen starting HEAD: `e41850512d8b7cb6265067f57a5c4a8e6c6bd4d9`

Required token observed: `PRE553_SR07_P1_WVS7_C11_SCALE_PREFLIGHT_RETURNED`

## 1. Publication holding

HQ accepts the SR07-P1 return as valid corroborative fail-closed scale evidence.

The return is exactly one commit ahead of the frozen starting HEAD and changes exactly four files under the authorized `SR07_P1_WVS7_C11_SCALE_PREFLIGHT/` directory.

Exact source remained:

- SHA-256 `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- 97,220 rows;
- 613 variables;
- 59,595,860 physical cells;
- decoder `decode_sav(source_path)`;
- no encoding override.

No runtime/source modification or forbidden database path was used.

## 2. Hostile physical preservation proof accepted

The bounded execution-only projection found an actually observed source cell:

- source row ordinal `49`;
- variable `Q152`;
- variable ordinal `224`;
- raw storage value `-2.0`;
- physical state `FORMAT_USER_MISSING_RANGE`;
- source declaration range `-5.0..-1.0`.

The execution-only projection retained raw value, physical state, declaration, row identity and variable identity without semantic interpretation.

This establishes that the accepted pre-scale semantic path can preserve the WVS hostile physical distinction at bounded size.

## 3. Scale measurements accepted

S1, 32 rows / 19,616 events, completed:

- peak RSS `969,048,064` bytes;
- Parquet `7,086,206` bytes;
- direct DuckDB checks passed.

S2, 128 rows / 78,464 events, completed:

- candidate peak RSS `803,733,504` bytes;
- I02 validation peak RSS `848,945,152` bytes;
- Parquet persistence peak RSS `3,248,009,216` bytes;
- full reopen peak RSS `3,302,440,960` bytes;
- Parquet `26,944,776` bytes;
- direct DuckDB checks passed.

Fresh S2 repeat reproduced semantic release hash, relation digests, public/internal inventory hashes, object counts and Parquet byte count.

S3, 512 rows / 313,856 events, did not complete:

- external 4 GiB tripwire fired at `4,296,179,712` bytes;
- child terminated by SIGKILL;
- S4 correctly not run.

The worker disposition `P1_BLOCKED__RESOURCE_TRIPWIRE` is accepted.

## 4. Cross-format diagnosis

SR08 LiTS I and SR07 WVS7 now independently demonstrate the same failure scale at approximately 307k-314k events.

WVS7 uses the ordinary metadata-first/chunked SAV decoder rather than the LiTS compatibility full-frame exception.

Therefore the shared failure cannot reasonably be attributed to the LiTS compatibility DataFrame path.

The combined evidence confirms the diagnosis already frozen by Authority 42:

`CURRENT_FULL_PYTHON_OBJECT_C11_EXECUTION_REPRESENTATION = NOT_SOURCE_SCALE_VIABLE`

This is a shared execution-representation contradiction, not a SAV/DTA decoder-class contradiction.

## 5. Storage projection treatment

The worker's very large full-WVS storage and memory numbers are linear `PROJECTION_ONLY` outputs from the rejected wide/materialized P1 representation.

They are not accepted as corrected architecture capacity targets.

Authority 44 now separately governs corrected persistent-storage acceptance and requires canonical steady-state versus transient byte accounting.

## 6. Gate state

`G-SR07 = BLOCKED__P1_RESOURCE_TRIPWIRE__ON_G_SR06_RELATIONAL_SCALE_CORRECTION`

`G-SR08 = BLOCKED__P1_RESOURCE_TRIPWIRE__ON_G_SR06_RELATIONAL_SCALE_CORRECTION`

`G-SR06 = REOPENED__RELATIONAL_SCALE_CORRECTION_ACTIVE`

`G-SR09 = BLOCKED`

No full WVS7 or LiTS I certification may begin until G-SR06 scale correction is accepted and the proving-source scale courts are rerun against the corrected path.

## 7. Next execution

The sole critical-path implementation job is the Authority-43/44 SR06 relational scale correction on branch:

`agent/vozhd-trii-sr06-relational-scale-correction`

The WVS7 and LiTS I old-path P1 courts are now complete historical contradiction evidence and should not be rerun on the rejected representation.
