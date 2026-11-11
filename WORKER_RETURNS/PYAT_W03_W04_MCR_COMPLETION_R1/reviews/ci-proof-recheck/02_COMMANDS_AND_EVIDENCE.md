# CC-F03/CC-F04 CI/proof recheck — commands and evidence

**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1`
**Branch:** `review/pyat-w03-w04-ci-proof-focused-recheck-r1`
**Reviewed head:** `4ac862ef58d06266c7de8a7cc186c5c41dd0ad48`
**Verdict:** `REVISE` at CC-F03 scope solely for CCF3-R01 trigger paths. CC-F04 actual proof gate and both sidecars pass at this scope.

All commands used an explicit `cd` into this worktree. Production/test/workflow/contract/HQ were read-only except the existing proof checker's transient mutation, which it restored. Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/ci-proof-recheck/`.

## 1. Worktree and source identity

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1
git branch --show-current
git rev-parse HEAD
git status --short
git ls-tree -r --name-only HEAD rawlsing_next | wc -l
find rawlsing_next -type f | wc -l
```

Result:

```text
review/pyat-w03-w04-ci-proof-focused-recheck-r1
4ac862ef58d06266c7de8a7cc186c5c41dd0ad48
clean before this review lease
407
407
```

Reviewed blobs:

```text
5a7a7bcdf7aa1e65cad887374ea204ed8e4d8ed8  .github/workflows/pyat-w03-w04-physical-economy.yml
7735f23582aed585d4865f3a1a228fc11c68d355  rawlsing_next/tests/test_bench_w03_w04_physical.py
aa4aa078b9345b846f5d3622392a7028f714c107  rawlsing_next/tests/test_bench_w03_w04_physical.py.proof.json
d487c413507f2834a411351ae47d41abd7d6227f  WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py
38a388db1709044312c0b690957909ba681422ba  WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py.proof.json
9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920  rawlsing_next/_pre553_query_eval.py
```

Frozen commission SHA-256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`; TSV blob `b17c63cea9706f50a0d9c0f0ce064e967da4c8eb`.

## 2. Actual committed proof gate

```sh
TMPDIR="$PWD/$OUT/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B \
  CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  --head 4ac862ef58d06266c7de8a7cc186c5c41dd0ad48 --root .
```

Result: exit 0, `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION`,
`witness_contracts_run=2`.

Witness receipts:

```text
SNAPSHOT_BENCH_CELLS_ACTUAL_CONSUMER_SEVERANCE_R1
  positive_node = WORKER_RETURNS/.../BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py::test_cli_cells_and_hash_uses_same_actual_consumer
  fault = rawlsing_next/_pre553_query_eval.py typed_state=evaluation.fact_state -> typed_state="UNRESOLVED"
  baseline = PASS; fault_probe = TARGET_ASSERTION_FAILED; grade = BOUNDED_MUTATION_DETECTED

W03_W04_BENCH_CELLS_ACTUAL_CONSUMER_SEVERANCE_R1
  positive_node = rawlsing_next/tests/test_bench_w03_w04_physical.py::test_cli_cells_and_hash_uses_same_actual_consumer
  fault = same production path
  baseline = PASS; fault_probe = TARGET_ASSERTION_FAILED; grade = BOUNDED_MUTATION_DETECTED
```

Restoration:

```text
query_eval before/after = 9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920
snapshot test before/after = 01eb49d388ce29721a6658ccb1fb305683ba3a8a369c2a814c6701b5885be7e2
source status after gate: clean (only this review lease)
```

The snapshot test was not renamed, removed or edited; only its sidecar was added. The actual bench and snapshot sidecars both name real tests and use the actual production mutation; no checker bypass or dummy metadata loader.

Logs: `logs/proof_gate_changed_actual.json`, `logs/proof_gate_changed_actual.stderr`, `logs/source_identity_before_gate.log`, `logs/source_identity_after_gate.log`.

## 3. Workflow / CC-F03

Current workflow blob `5a7a7bcdf...`. The court includes the prior sourcefree selections plus cold/completion:

```text
test_pre553_c11_execution_view.py
test_pre553_c11_cold_reopen_i03.py
test_pre553_source_backed_c11_facade.py
test_pre553_carrier_execution.py
test_pre553_i03_grouping.py
test_bench_w03_w04_physical.py
test_pre553_w03_w04_cold.py
test_pre553_w03_w04_completion.py
```

Author receipt: **86 passed in 37.07s** (`logs/CI_PROOF_R1_workflow_tests_86.out` copied from read-only receipt); not rerun, no demonstrated need. The changed bench test only adds I05 receipt/fact assertions; no assertion removal/weakening.

Checkout: `actions/checkout` uses PR head (`github.event.pull_request.head.sha`) with `fetch-depth: 0`; the proof-gate step fetches exact `pull_request.base.sha`/`head.sha` and runs the existing checker. Correct.

Smoke: 256-row full-matrix is explicitly named non-100k/MCR acceptance; `smoke_summary.json` has `acceptance_pass=false`, `acceptance_status=NON_FINAL_DIAGNOSTIC__DO_NOT_REPORT_AS_FULL_MATRIX_PASS`, `final_matrix_eligible=false`. No full 256/100k rerun; no economic threshold claimed.

### CCF3-R01 — trigger omissions

`logs/workflow_path_audit.txt` confirms these exact paths are **MISSING** from `pull_request.paths`:

```text
WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py.proof.json
```

The original commission, TSV, checker, actual sidecar, proof gate and its self-test are present. The wrapper/checker test and preserved snapshot proof paths are not. A PR changing only those paths does not trigger the court; the author return's claim that wrapper/checker paths were added is incomplete. This is CCF3-R01.

## 4. Sidecar and snapshot proof details

Actual sidecar:

```text
rawlsing_next/tests/test_bench_w03_w04_physical.py.proof.json
claim_id W03_W04_BENCH_CELLS_ACTUAL_CONSUMER_SEVERANCE_R1
positive_node rawlsing_next/tests/test_bench_w03_w04_physical.py::test_cli_cells_and_hash_uses_same_actual_consumer
fault path rawlsing_next/_pre553_query_eval.py
```

Preserved snapshot sidecar:

```text
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py.proof.json
claim_id SNAPSHOT_BENCH_CELLS_ACTUAL_CONSUMER_SEVERANCE_R1
positive_node .../BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py::test_cli_cells_and_hash_uses_same_actual_consumer
snapshot test SHA-256 = 01eb49d388ce29721a6658ccb1fb305683ba3a8a369c2a814c6701b5885be7e2
```

`git diff --name-only 8c5ae1c5..4ac862ef -- .../BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py` is empty; no snapshot rename/remove/edit. Both witnesses baseline PASS and mutant assertion RED; source restored. This satisfies CC-F04 at this scope.

## 5. Boundary

No full 12-ID/economic/code acceptance, no 100k/final matrix, no 86/256 rerun, no original35/SAV/DTA/DB/source bytes, native/S3/science/actor effect, install, protected merge, CI waiver, new engine/worker, or model/provider/account/effort change. CC-F01 already accepted and not reopened; current CCF5-R01 remains unaccepted; CC-F02 economics method remains outside. Full final same-SHA code/economic/external MCR proof remains required.

`logs/review_hashes.log` records SHA-256 of this review, findings, workflow/sidecars/snapshot, gate logs and exact source blobs.

**Final:** `REVISE` at CC-F03 scope solely for CCF3-R01; CC-F04 actual proof gate and both sidecars pass at this scope; no whole MCR/economic acceptance.
