# FIABC FINAL CURRENT-HEAD SUCCESSION / P10 PRODUCERS — R1 RETURN

## Terminal

`FIABC_FINAL_SUCCESSION_PRODUCERS_R1_B07_IMPLEMENTED__EXACT_HEAD_I07_P10_PRODUCER_COMMITTED__EXISTING_EVALUATOR_PASS_ENFORCED_AT_RUNTIME__SOURCE_FREE_TESTS_AUTHORED_NOT_EXECUTED__NO_CANDIDATE_OR_P2X_EXECUTION`

## Scope

Closed exactly launch blocker **B07** by adding a deterministic pre-candidate producer CLI:

`rawlsing_next/fiabc_succession_producer.py`

The producer emits:

1. exact-current-head frozen I07 succession manifest;
2. governed external P10 lifecycle/failure-scope context;
3. optional producer receipt binding both products to the same checked-out commit and exact current implementation Git objects.

It calls the existing `rawlsing_next.fiabc_succession_preflight.evaluate_manifest` evaluator and refuses to emit a PASS receipt unless the generated manifest/context evaluate `PASS`. It then embeds that PASS evaluation and re-evaluates the sealed manifest before writing outputs.

## Exact-head law

The producer obtains the runtime head from:

`git rev-parse --verify HEAD^{commit}`

No commission/base/head SHA is baked into `generated_from_commit_sha`.

The CLI requires a clean working tree. Optional `--expected-head <40-hex SHA>` gives the launch pack an additional exact-head assertion. A mismatch blocks before outputs are produced.

Every current implementation prerequisite is resolved from that same HEAD to:

- exact commit;
- exact Git blob;
- exact content SHA-256.

Those identities are retained in the optional producer receipt.

## Existing law preserved

The producer consumes, rather than rewrites:

- `RAWLSING_FIABC_SUCCESSION_MANIFEST@1.0.0`;
- `RAWLSING_FIABC_SUCCESSION_GOVERNING_PROFILE@1.0.0`;
- `RAWLSING_FIABC_SUCCESSION_PREFLIGHT@1.0.0`;
- current T2 six-cell execution manifest;
- current T5 six-cell court contract;
- final HQ preflight/fan-in return;
- adopted L01 comparison boundary;
- adopted L02 claim-scoped authority closure;
- accepted Wave-1 F001-F036 succession genealogy.

The current-owner map covers exactly the governing profile's 29 preterminal functions. The seven profile-deferred functions remain deferred; no new semantic owner is invented.

## Six-cell / failure-scope holdings

The producer refuses current-manifest drift unless order is exactly:

1. `LITS_I/A`
2. `LITS_I/B`
3. `LITS_I/C`
4. `WVS7/A`
5. `WVS7/B`
6. `WVS7/C`

P10 records current candidate-local successor edges directly from T2. Candidate-local failure is scoped to the current cell and later lawful cells remain reachable.

Common-source scope remains:

`BLOCK_REMAINING_GOVERNED_STAGES_OF_CURRENT_SOURCE__THEN_ADVANCE_TO_NEXT_SOURCE_OR_FINAL_COURT_GATE`

with terminal disposition `BLOCKED_BY_COMMON_SOURCE_AUTHORITY`.

Common-court scope remains `BLOCK_COURT_UNTIL_RESUME` / `BLOCKED_BY_COMMON_COURT_AUTHORITY`.

Candidate-B S12/S13 must retain `PURE_B_NO_CACHE`. WVS7/C S12/S13 must retain `C_ZERO_ACCELERATOR_NO_CACHE`.

LiTS/A S01 must remain:

`READY__RUN_LOCALLY`, source-access required, physical-host measurement required,

and is recorded as:

`MEASURED_CURRENT_WORK__NOT_HISTORICAL_PRESERVATION`.

## Pre-candidate zero-state law

P10 is emitted only with:

- `candidate_processes_started = 0`;
- `candidate_outputs_seen = 0`;
- `candidate_owned_roots_consulted = []`;
- `ranking_or_selection = false`;
- `frozen_before_candidate_execution = true`.

The producer contains no source decode/read path and no Candidate A/B/C execution entrypoint.

## Current-head fail-closed integration behavior

This worker does not import sibling-owned implementation files into its branch. The producer explicitly requires every I07 current owner named by the adopted profile to exist on the **later actual launch HEAD**. For example, accepted F012/F018 diagnostic/effective-N successors must be present after HQ fan-in; if they are not, production fails before a manifest is written rather than downgrading or fabricating succession.

That is deliberate B07 behavior, not a new blocker invented by this worker.

## Tests authored

Added:

`rawlsing_next/tests/test_fiabc_succession_producer.py`

Thirteen source-free hostile tests cover:

- Git-derived current HEAD;
- expected/stale HEAD rejection;
- dirty-tree rejection;
- exact six-cell order and WVS7/C sixth;
- LiTS/A S01 measured law;
- exact candidate-local/common-source/common-court scopes;
- Candidate-B no-cache and WVS7/C zero-accelerator no-cache;
- existing evaluator PASS on generated synthetic/current-T2/T5 fixture;
- nonzero candidate process/output/root/ranking rejection;
- exact 29-function owner-map closure;
- hostile preserved LiTS/A S01 rejection;
- hostile WVS7/C cache escape rejection.

No runtime tests were executed in this browser/GitHub-only lane and no GitHub Actions workflow was triggered.

## Execution prohibition record

- user's Mac/local runtime: **NOT USED**
- raw LiTS bytes: **NOT OPENED**
- raw WVS bytes: **NOT OPENED**
- Candidate A/B/C: **NOT RUN**
- measured P2X: **NOT RUN**
- GitHub Actions: **NOT TRIGGERED**
- execution branch pointer: **NOT ADVANCED**
- sibling workers: **NOT WAITED ON**

B08 remains HQ-owned.
