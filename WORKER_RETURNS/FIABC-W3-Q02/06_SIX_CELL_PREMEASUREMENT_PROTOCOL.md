# FIABC-W3-Q02 — six-cell premeasurement qualification and lawful-measurement gate

This phase occurs **after** R6X historical reconciliation and **after** both independent oracles are frozen, but **before** measured P2X candidate execution.

## 1. Fresh qualification/measurement roots

Do not use a candidate root containing prior candidate scratch/session/RSS history as a fresh Wave-3 measurement lifecycle.

```bash
export MEASURE_ROOT=/absolute/path/to/new/wave3/measured-court-root
test ! -e "$MEASURE_ROOT" || test -z "$(find "$MEASURE_ROOT" -mindepth 1 -print -quit)"
mkdir -p "$MEASURE_ROOT"
```

The historical `OLD_WORK_ROOT` remains evidence for R6X/history only. The integrated execution code may consume preserved immutable LiTS-A first-build evidence and other permitted historical telemetry credit only where the B03 constitution explicitly allows it; it must not inherit mutable candidate session/scratch state.

## 2. Mechanized succession preflight comes before any candidate start

Run the exact I07 command from:

`WORKER_RETURNS/FIABC-W3-I07/00_RETURN.md`

against the fully integrated execution tree and the two frozen I05 oracle receipts. The I07 command must produce a machine receipt that proves every comparison-required obligation through the chain:

`obligation -> authority -> current authoritative owner -> executable binding -> live consumer -> invariant class -> cost owner`

and must prove all six current source×candidate capabilities.

If I07's final return does not provide a deterministic invocation, or if its receipt is anything other than PASS, stop. Do not proceed to a candidate process.

## 3. Six-cell capability matrix that I07/current execution binding must prove

### LiTS-I × A

Required before measurement:

- exact LiTS source identity;
- frozen Candidate-A owner blob `d4915e7e6755ba1850756aebff72f982f73a332b`;
- preserved qualifying R5 carrier bound without repeating the forbidden first build;
- stable I04 LiTS runtime package/materializer and exact runtime identities;
- current carrier-neutral C11/I03/I05 executable binding;
- independent LiTS oracle already frozen;
- no mutable state from another candidate lifecycle.

### LiTS-I × B

Required:

- exact LiTS source identity;
- frozen Candidate-B owner blob `7c509c2098d0030f253344eb3f682471378812a8`;
- source-backed virtual C11 binding;
- preserved standalone cacheless-C11 historical milestone used only as allowed evidence, not as current result substitution;
- stable runtime authority closure;
- independent LiTS oracle already frozen.

### LiTS-I × C

Required:

- exact Candidate-C owner blob `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`;
- Candidate-C identity remains C even when source-backed realization is used;
- existing CACC1/CACC2 are optional and used only inside exact frozen scope;
- q310/q311 and any other required material outside accelerator scope use exact-source-backed fallback;
- no CACC3;
- no workload truncation;
- same governed C11/I03/I05 semantic core as A/B;
- accelerator deletion/nonavailability leaves semantic result identity unchanged;
- independent LiTS oracle already frozen.

### WVS7 × A

Required:

- exact WVS source identity and Lock2 closure;
- frozen Candidate-A owner blob;
- stable WVS runtime package/projection materializer;
- exact source-backed projection and current R5 execution binding;
- independent WVS oracle already frozen.

### WVS7 × B

Required:

- exact WVS source identity and Lock2 closure;
- frozen Candidate-B owner blob;
- stable WVS runtime package/projection materializer;
- exact source-backed virtual C11 current binding;
- independent WVS oracle already frozen.

### WVS7 × C

Required:

- frozen Candidate-C owner blob;
- **zero applicable accelerators**;
- no WVS-specific accelerator and no CACC3;
- exact-source-backed reconstruction feeding the same governed C11/I03/I05 core;
- Candidate C must remain Candidate C even though physical realization degenerates to source-backed execution;
- the old preserved WVS-C portability failure must be classified as historical evidence, not current execution law;
- independent WVS oracle already frozen.

Any unproved cell is a hard court stop. Five proven cells plus one preserved historical failure is not six-cell qualification.

## 4. Equal-work premeasurement gate

Before the first candidate process, verify that the integrated I06 implementation enforces all of the following:

1. fresh isolated process per `source × candidate` cell;
2. oracle/source/authority/workload freeze occurs before candidate-local measurement start;
3. candidate-local measurement stop occurs only after required lifecycle/replay work for that cell;
4. no `_SESSIONS`, RSS history, scratch, or unpermitted durable state leaks between candidates;
5. CPU outer-total and phase deltas cannot nested-double-count;
6. RSS is candidate-process-local under Darwin's `ru_maxrss` bytes law;
7. bytes read/written/rewritten are observed operations, not endpoint directory size;
8. scratch is high-water, not final size;
9. cold and warm fields are distinct and write-once;
10. delete/rebuild, source invalidation, semantic invalidation, stale, corrupt, interruption, and fresh replay are real actions;
11. uncaptured/unreached telemetry is typed null, never synthetic zero;
12. permitted historical telemetry is explicitly typed as historical/preserved and never represented as a fresh measurement.

The I06 focused hostile tests and Q01 accounting tests must be PASS on the exact execution tree.

## 5. Current execution manifest/continuation contract gate

Before measured execution there must be one current machine-readable execution contract consumed by the driver. It must:

- list exactly sources `LITS_I`, `WVS7` and candidates `A`, `B`, `C`;
- admit all six cells as current executable/capability-proved cells;
- preserve historical reducer/receipt references without reusing historical Candidate-C failures as current terminal states;
- place candidate-neutral oracle freeze before candidate process start;
- bind exact source hashes, workload/frontier identities, frozen owner blobs, I04 runtime package identities, and I07 preflight receipt;
- bind I08 final terminal verifier;
- never authorize a weight/default estimand for the RAW/unweighted workloads.

The historical continuation map SHA-256 `ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422` does not satisfy this requirement because it encodes the superseded current WVS-C portability failure.

If no new/current contract exists after fan-in, stop. Do not edit the historical map in place.

## 6. Terminal-verifier premeasurement contract check

Run I08's focused/source-independent verifier tests before measurement. The final verifier must require inputs for:

- I07 succession-preflight PASS;
- I05 independent-oracle PASS for each source;
- all six admitted cells;
- mandatory C11 and I03 intermediate receipts;
- complete fixed I05 frontier;
- I05 coverage and constituent-I03 closure;
- exact semantic identity;
- exact replay identity;
- exact output/product identity;
- lifecycle replay reproducing the same terminal identities.

It must not fabricate those receipts itself.

## 7. Lawful-measurement predicate

Measured P2X becomes lawful **only** when all terms below are true:

```text
WAVE3_BROWSER_TESTS_PASS
AND PACKAGING_IDENTITIES_PASS
AND FROZEN_OWNER_IDENTITIES_PASS
AND R6X_HISTORICAL_RECONCILIATION_PASS
AND LITS_ORACLE_FROZEN_INDEPENDENTLY_BEFORE_CANDIDATES
AND WVS_ORACLE_FROZEN_INDEPENDENTLY_BEFORE_CANDIDATES
AND SIX_CURRENT_SOURCE_X_CANDIDATE_CAPABILITIES_PROVED
AND I06_EQUAL_WORK_INSTRUMENTATION_PASS
AND I07_SUCCESSION_PREFLIGHT_PASS
AND I08_TERMINAL_CONTRACT_PASS
AND CURRENT_SIX_CELL_EXECUTION_MANIFEST_VALID
AND EXACT_DARWIN_RUNTIME_PASS
AND BOTH_SOURCE_HASHES_PASS
AND NO_UNRESOLVED_COMMON_SOURCE_OR_COURT_BLOCKER
```

If any term is false or unknown, measured P2X is not authorized.

## 8. Mechanical execution sequence once lawful

The final I03/I05/I06 integration may retain the existing driver CLI or return a successor CLI. Use the exact final command recorded by I06/I07/I08 returns. If it retains the current driver contract, the mechanical pattern is:

```bash
python rawlsing_next/ee_p2x_darwin_court_driver.py \
  --preflight \
  --continuation-map "$CURRENT_WAVE3_EXECUTION_MANIFEST" \
  --work-root "$MEASURE_ROOT" \
  --repo-root "$REPO" \
  --lits-path "$LITS_PATH" \
  --wvs-path "$WVS_PATH"

python rawlsing_next/ee_p2x_darwin_court_driver.py \
  --run \
  --continuation-map "$CURRENT_WAVE3_EXECUTION_MANIFEST" \
  --work-root "$MEASURE_ROOT" \
  --repo-root "$REPO" \
  --lits-path "$LITS_PATH" \
  --wvs-path "$WVS_PATH" \
  --backend-module rawlsing_next.ee_p2x_darwin_stage_backend
```

If interrupted after a terminal stage receipt is durably sealed, use the final driver's governed `--resume` mode; never hand-edit stage order. After complete execution, run the exact I08 verifier command and the final driver's `--verify-only` mode if retained.

**Do not run the pattern above against the old reducer merely by substituting its path.** The current manifest must be the Wave-3 six-cell contract proved in Section 5.

## 9. Expected successful terminal

Only the I08 terminal defined by Wave-3 is admissible:

`GOVERNED I05 LEARNED EMPIRICAL PRODUCT + EXACT SEMANTIC / REPLAY / OUTPUT IDENTITY + COVERAGE + CONSTITUENT I03 FACT CLOSURE`

Later lifecycle stages may continue for accounting/replay purposes, but they must reproduce the same terminal identities. No ranking, winner, or cross-source metric pooling is produced by this court.
