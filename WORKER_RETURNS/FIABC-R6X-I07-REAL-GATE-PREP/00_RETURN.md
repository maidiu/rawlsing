# FIABC R6X / I07 / Real-Gate Browser Preparation

## Terminal

`FIABC_R6X_I07_REAL_GATE_PREP_COMPLETE__BROWSER_WORK_EXHAUSTED__MINIMAL_LOCAL_CONTROL_SEQUENCE_FROZEN__NO_MEASUREMENT_PERFORMED`

## Exact lane

- repository: `maidiu/rawlsing`
- exact common base: `357cc2ac6952a478fa2e38f9adbe45ebb3671081`
- branch: `agent/rabochii-premain-fiabc-r6x-i07-real-gate-prep-r1`
- execution surface: GitHub/browser only
- raw LiTS/WVS carriers opened: **0**
- Candidate A/B/C executed: **0**
- I03/I05 executed: **0**
- measured P2X executed: **0**

This return prepares control mechanics only. It does not certify a source, mint a physical-equivalence PASS, issue I07 PASS, or authorize measured P2X.

## 1. R6X holding — historical ledger is not the current court ledger

The old R6X protocol was written against the historical continuation map and the stopped local ledger whose pre-reconciliation SHA-256 was:

`7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671`.

A divergent historical LM3 branch records that one local work root had already been reconciled to:

- post-ledger SHA-256 `4d0c412df4844906df78a94fbd0b3f6dff40412ca695e76137d3309cf1aaedd6`;
- R6X receipt SHA-256 `cd346db0623ce1f138bd0f14d9a81f8edf45b62c576c4f35910241b98edc7b26`;
- status `AUDIT_ONLY__ALREADY_RECONCILED`.

That branch is **not** in the sealed current lineage, so its local-state observation is archaeological evidence, not a current-lineage receipt.

More importantly, the current live driver no longer consumes the historical continuation map. Its CLI loads `WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json` through `load_current_execution_manifest(...)`. The current manifest:

- admits exactly all six LiTS-I/WVS7 × A/B/C cells;
- explicitly makes the historical continuation map immutable history only;
- rejects historical Candidate-C failures as current capability law;
- requires LiTS-C and WVS-C current execution;
- has first unfinished stage `LITS_I/A/S02_C11_REACHABILITY`.

The current `StageLedger` also requires its embedded manifest identity to equal the current machine identity exactly. An old historical/R6X ledger therefore cannot be silently resumed under the current T2 machine: it fails closed as ledger-authority drift.

### R6X final disposition

**Do not mutate the historical ledger again and do not import it as the current court ledger.**

The minimum current-court action is:

1. preserve the old ledger/R6X receipt as historical evidence if the files still exist;
2. choose a **new, absent/empty current court work root**;
3. initialize the current T2-manifest ledger there;
4. let the current driver bind the lawful preserved prefixes from immutable repository evidence;
5. if the preserved LiTS-A R5 carrier physically resides under an old root, reference only that governed derivative through the dedicated R5 root + R35 parentage inputs after Worker 3 closes them; do not copy the old stage ledger or backend state.

Thus the remaining R6X burden is control-state reconciliation by **current-manifest supersession**, not another destructive old-ledger rewrite.

## 2. I07 holding

The accepted I07 implementation remains:

- `rawlsing_next/fiabc_succession_preflight.py`
- blob `e9591b3f4beba3a5aa35039edc85163635582959`.

Its schema/profile remain:

- manifest schema blob `484678375abcdd94151b72b425629ccb535be5eb`;
- governing profile blob `57effa49428f8274cf7ca73e8442f75cca1b8267`.

A real PASS requires all P00–P10 checks, exact immutable evidence refs, all required F001–F036 function-chain dispositions, six production capabilities, candidate-neutral oracle closure, accounting closure, and a separate lifecycle/failure-scope context.

The live T5 wrapper further requires:

- the manifest was frozen before candidate execution;
- `generated_from_commit_sha` equals the **actual final execution HEAD**;
- current court contract validates against the current execution manifest;
- all evidence refs resolve at exact commits;
- lifecycle context is present;
- the emitted T5 I07 receipt binds final HEAD, manifest digest, lifecycle digest, and court-contract digest.

This worker deliberately does **not** guess future R1K/Worker-2/Worker-3 identities. `02_I07_FINAL_HEAD_BINDING_TEMPLATE.json` freezes all presently knowable law and names exact unresolved slots.

## 3. Source/oracle live binding

Before candidate start the T3 freeze receipt must satisfy:

- schema `RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0`;
- candidate-neutral = true;
- frozen-before-candidate-execution = true;
- candidate outputs seen = 0;
- candidate-owned roots consulted = [];
- candidate-owned state reused = false;
- state = `FROZEN_READ_ONLY`;
- exact source freezes for LiTS-I and WVS7;
- exact authority/workload identities;
- exact source-local oracle identities and freeze-authority refs;
- strict order source identity → authority/workload → oracle.

The WVS oracle identity is intentionally pending R1K. The final live runtime identity/court-contract pins are intentionally pending Worker 2. LiTS-A parentage is pending Worker 3.

No candidate process may begin until the complete final T3 freeze and real I07 receipt both validate.

## 4. R35 physical-equivalence holding

### WVS7

A candidate-neutral canonical expectation already exists in the sealed lineage:

- path `WORKER_RETURNS/FIABC-LM2/04_WVS7_CANONICAL_PHYSICAL_EXPECTATION.json`;
- Git blob `94d28db4fe031db03210303fd9f7b197a5b84c26`;
- expectation identity `9845c24da0c03adb4dfd65118b7c8c39a60a30337f33cc4177ffc6c848d02390`;
- source SHA `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- reader: pyreadstat 1.3.6, native SAV, `apply_value_formats=false`, `user_missing=true`;
- edge classes EC01, EC05, EC07, EC09, EC10, EC12, EC13.

R1J's minimal representation repair does not invalidate that physical expectation.

No A/B/C WVS physical realization receipt is presently persisted in the current tree.

### LiTS-I

No candidate-neutral LiTS-I R35-I03 canonical expectation was found in the sealed common-base tree. T6 itself states that real candidate-neutral expectations/realizations remain a controlled local qualification materialization step.

LiTS exact edge classes are:

`EC01, EC02, EC05, EC06, EC09, EC12`.

Therefore one local, candidate-neutral LiTS physical evidence materialization remains irreducible unless a later accepted return recovers an existing expectation. It must not be confused with Candidate-A's preserved R5 build.

### Nonduplication law

R35 is external to the P2 driver. Do not prebuild an expensive candidate solely to obtain an R35 receipt and then rebuild it during measured execution.

For candidate-specific realizations:

- use an already-current preserved realization when one exists and passes parentage/currentness;
- otherwise assemble the R35 realization descriptor from the same governed physical state produced at the cell's S01 boundary;
- hold its performance telemetry **inadmissible** until R35 physical equivalence and independent semantic parity both pass;
- if required physical evidence cannot be extracted from the current S01 realization without rebuilding/rereading, STOP and return the exact missing evidence dimension instead of duplicating work.

Physical PASS never substitutes for I05 semantic parity, source certification, population authority, or I08.

## 5. Lock1 host preflight

Frozen host law:

- CPython 3.11.3;
- Darwin;
- x86_64;
- pyreadstat 1.3.6;
- pyarrow 25.0.1;
- Darwin `ru_maxrss` interpreted as bytes;
- LiTS-I SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- WVS7 SHA `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- exact accepted P2X branch and P2R1 seam;
- isolated fresh current work root;
- one live driver instance;
- no concurrent benchmark workload.

The current driver proves only a single-driver lock; it explicitly makes no process-name idle heuristic claim. Therefore “no concurrent benchmark workload” must be established by exclusive-host reservation/operator observation, not fabricated by a brittle process-name scan.

The preflight itself hashes both source files. That is non-measured source verification and is allowed only in the eventual local control lane—not in this browser worker.

## 6. Remaining local mechanics after sibling fan-in

If Worker 1, Worker 2, and Worker 3 all close successfully, the irreducible pre-candidate local sequence is reduced to:

1. create a fresh current-court work root; retain old stopped/R6X root as history only;
2. verify Lock1 host/repo/source gates;
3. materialize/recover only the missing LiTS candidate-neutral R35 expectation if still absent;
4. assemble the final T3 source/oracle freeze from exact final LiTS/WVS source and oracle refs;
5. assemble and seal the final I07 manifest/lifecycle context using the exact final HEAD, final live court contract, Worker-3 LiTS parentage and source-local R35 gate inputs;
6. run `--preflight` only and require exact I07/T5 PASS;
7. only after those controls pass may the separately governed six-cell execution begin.

No measured result was created here.
