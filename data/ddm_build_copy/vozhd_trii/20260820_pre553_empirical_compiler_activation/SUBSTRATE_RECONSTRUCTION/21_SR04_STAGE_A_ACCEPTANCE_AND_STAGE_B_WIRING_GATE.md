# SR04 STAGE A ACCEPTANCE AND STAGE B WIRING GATE

Status: `STAGE_A_ACCEPTED__STAGE_B_NOT_AUTHORIZED__SHARED_PATH_WIRING_REQUIRED`

Accepted Stage-A harness HEAD: `a5874b3a8bc371ae3a2baebf31f3cce6fe9bb298`
Accepted harness SHA-256: `ee885a7256b0d2bf5f2efa81f8c503ed034c7d6e78f203cb1f99c3936f7d3a1d`
Required Stage-A token: `PRE553_SR04_SYNTHETIC_CONTRACT_TESTS_PASS`

## 1. HQ acceptance of Stage A

HQ accepts the returned Stage-A synthetic contract receipt as proving the following about the synthetic execution path:

- all Q00-Q15 synthetic query shapes executed and matched an independent synthetic oracle for all four candidates;
- all four candidates reproduced stored-candidate read-back digests;
- wrong-oracle detection fired;
- stored-data corruption detection fired;
- disposable PostgreSQL remained connected through query and replay and then stopped;
- `DATABASE_URL` was not used;
- no WVS7/LiTS I raw decode occurred;
- cleanup remained confined to the disposable work root.

Stage A is therefore `ACCEPTED` as a synthetic contract test.

## 2. Stage B remains blocked

Static HQ review of the committed harness proves that the real-source Stage-B dispatch still invokes the older pre-acceptance functions:

- `candidate_duck(...)`
- `candidate_pg(...)`
- `candidate_sqlite(...)`
- `query_specs()`

Those functions are not the same candidate/oracle/read-back implementation exercised by Stage A.

Therefore Stage A does **not** yet prove the real Stage-B execution path.

No raw-source Stage-B run is authorized from `a5874b3...`.

## 3. Specific remaining defects in the old Stage-B path

At minimum, the old real-source path still contains these defects:

1. `Q05_WVS_RISKSET_Q152` does not enforce the frozen `I_PSU physical_state='ORDINARY'` condition used by the accepted Stage-A SQL.
2. `Q06_WVS_WEIGHTED_Q152` uses a separate raw-text parsing implementation rather than the accepted typed numeric path.
3. `Q09_XOR_COORDINATE` returns only a scalar count instead of the frozen Q152 distribution over the XOR-qualified respondents.
4. candidate SQL results are timed but are not required to equal the independently computed real oracle.
5. DuckDB-native replay digest is computed from the neutral in-memory dataframe instead of reading the DuckDB store back.
6. SQLite replay digest is computed from the neutral in-memory dataframe instead of reading SQLite back.
7. PostgreSQL replay digest is computed from the neutral in-memory dataframe instead of reading PostgreSQL back.
8. the old PostgreSQL function closes its connection before the subsequent timed query path.
9. the old PostgreSQL schema materializes all fields as TEXT, diverging from the typed Stage-A PostgreSQL execution and risking engine-specific coercion differences.
10. required performance measurements are incomplete: cold open/connect, separate index-build time, measured peak RSS, and exact warm-up protocol are not uniformly implemented.
11. per-candidate disk and wall/query time budgets are not enforced as the frozen contract requires.
12. the old Stage-B SQL and Stage-A SQL are duplicated maps and can drift independently.

This list is a minimum audit, not permission to patch only these numbered symptoms.

## 4. Binding Stage A.1 design law — ONE EXECUTION PATH

The harness must be refactored so Stage A and Stage B invoke the **same**:

- frozen Q00-Q15 SQL definitions;
- candidate build functions;
- candidate query normalization;
- oracle comparison function;
- stored-candidate read-back digest function;
- timing protocol;
- disk/time safety enforcement;
- candidate-disposition logic;
- provisional selection logic.

The only lawful Stage-A/Stage-B difference is the fixture provider:

`tiny synthetic fixture -> shared carrier court`

versus

`exact WVS7/LiTS I neutral fixture -> shared carrier court`.

There must not be a separate `STAGE_A_SQL` truth map and `query_specs()` truth map after Stage A.1. One frozen map must serve both.

There must not be synthetic-only candidate implementations that are different from Stage B candidate implementations.

## 5. Stage A.1 acceptance burden

Before any raw-source decode, the updated harness must rerun the tiny synthetic suite through the exact shared code path that Stage B will later invoke.

The Stage A.1 receipt must additionally prove:

- `shared_query_map = true`;
- `shared_candidate_execution_path = true`;
- `shared_oracle_comparison_path = true`;
- `shared_stored_readback_path = true`;
- `shared_budget_enforcement_path = true`;
- candidate outputs cannot receive `MEASURED_CORRECT` unless oracle comparison AND stored read-back digest both pass;
- each candidate has actual non-placeholder measurements for every contract-required measurable field or an exact typed nonviability reason;
- deliberate oracle corruption and stored-data corruption still fail through the shared path.

Required Stage A.1 token:

`PRE553_SR04_SHARED_EXECUTION_PATH_CONTRACT_PASS`

## 6. Neutral fixture checkpoint law for later Stage B

After Stage A.1 is accepted, Stage B may decode the exact WVS7/LiTS I sources once and build the neutral Arrow fixture.

The neutral fixture becomes reusable within SR04 only when a checkpoint manifest records and verifies:

- exact WVS7 and LiTS I source SHA-256 identities;
- harness HEAD + harness SHA-256;
- fixture manifest hash;
- all four neutral relation digests;
- independent query-oracle digest;
- exact row counts;
- successful hostile-fixture preflight.

A later execution-only retry may reuse that checkpoint only if every recorded identity/digest still matches and no fixture-generation, oracle, raw-value, query-truth, decoder, source-byte, or benchmark-contract code changed.

Candidate-implementation-only retry does not require raw-source re-decoding if the checkpoint remains exact.

## 7. Governance consequence

G-SR04 state:

`STAGE_A_ACCEPTED__STAGE_A1_SHARED_PATH_RETURN_REQUIRED`

G-SR06 remains blocked.
