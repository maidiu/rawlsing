# CC-F03 / CC-F04 CI and proof repair

**Scope:** exact queued CC-F03/CC-F04 only; no CC-F01/CC-F02/CC-F05 repair, no production benchmark/method change, no economic or whole-MCR acceptance.

- **Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2`
- **Branch:** `agent/pyat-w03-w04-ci-proof-repair-r1`
- **Start head:** `09f97a3a4c77ed7666ee95af586cfdfd91493f73`
- **Implementation head:** `a77d1e052ab5d5022cd88c274dde4d2146265231`
- **Author status:** `DELIVERED_PENDING_RECEIVING` for the scoped CC-F03/CC-F04 repair; whole MCR/economics remain `INCOMPLETE`.
- **Full frozen proof gate:** `RED` only on the preserved review snapshot path, outside the authorized write lease; exact residual is recorded below. Scoped changed gate for this repair is `PASS`.
- **No waiver:** the workflow runs the existing checker at real PR base/head; no new checker, engine or bypass.

## CC-F03 disposition

- Trigger now includes actual cold/facade/ingest/execution-view/cache/carrier and directly used benchmark helpers, the cold/completion tests, exact contract/TSV and existing wrapper/checker paths.
- Existing court retains the prior sourcefree selections and adds `test_pre553_w03_w04_cold.py` and `test_pre553_w03_w04_completion.py`.
- Exact affected court result: **86 passed in 37.07s**.
- The 256-row full-matrix smoke remains explicitly non-100k/no-MCR-acceptance: `final_matrix_eligible=false`, `acceptance_status=NON_FINAL_DIAGNOSTIC__DO_NOT_REPORT_AS_FULL_MATRIX_PASS`.

## CC-F04 disposition

- Added `rawlsing_next/tests/test_bench_w03_w04_physical.py.proof.json`.
- Named claim: `W03_W04_BENCH_CELLS_ACTUAL_CONSUMER_SEVERANCE_R1`.
- Positive node: `rawlsing_next/tests/test_bench_w03_w04_physical.py::test_cli_cells_and_hash_uses_same_actual_consumer`.
- Actual implementation mutation: `rawlsing_next/_pre553_query_eval.py`, `typed_state=evaluation.fact_state` -> `typed_state="UNRESOLVED"`.
- Existing gate result: baseline **PASS**, target **ASSERTION_FAILED**, grade `BOUNDED_MUTATION_DETECTED`, restored source blob matches HEAD.
- Added the existing checker to CI with `fetch-depth: 0`, PR head checkout, real `github.event.pull_request.base.sha/head.sha` and explicit `git fetch`.

## Exact full-gate residual

```text
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  --head a77d1e052ab5d5022cd88c274dde4d2146265231 --root .
exit 1
PROOF_INTEGRITY_GATE_RED:
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py:
material integration-claim test requires test_bench_w03_w04_physical.py.proof.json
with executable severance witness
```

This is the preserved independent-review snapshot, not a benchmark/source/test modified by this lease. Adding its sidecar would require a write outside the allowed lease. It is reported, not hidden. The new cold-selector test was not reported by the gate and did not require a separate sidecar.

No 100k/full final matrix, no production/cache/facade/validator edits, no new workflow/checker/engine, no original35/science/native/actor/protected-merge effect. Final same-SHA code/economic receiving, full 12 IDs and external MCR proof remain required.
