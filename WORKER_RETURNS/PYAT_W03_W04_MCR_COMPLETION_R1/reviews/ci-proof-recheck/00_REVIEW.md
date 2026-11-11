# CC-F03/CC-F04 CI and proof focused recheck

**Review:** independent focused CC-F03/CC-F04 recheck only.
**Exact worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1`
**Branch/head:** `review/pyat-w03-w04-ci-proof-focused-recheck-r1` at `4ac862ef58d06266c7de8a7cc186c5c41dd0ad48`; source tree 407 files, clean.
**Verdict:** **`REVISE` at CC-F03 scope**. CC-F04's proof gate and both sidecars pass at this scope; the CI workflow still does not trigger on the exact wrapper, verifier-checker test, or preserved-snapshot proof paths it claims to cover. No whole 12-ID, code or economic acceptance.

## 1. Exact reviewed sources

- Prior combined review: `07c172683c4a720b8d1c37599c3e09a5357e56d8` (CC-F03/CC-F04 findings).
- Frozen commission and 12-ID TSV were read; original review CC-F03/CC-F04 was read.
- Author candidate `df32985387da3da26f587ddbcd75ad031b837773`; CI/proof author commits `a77d1e052` / `be6548072` / `df6fa8aa2` / `8c5ae1c5`; integrated `7036e7358` / `c8ea91266` / `a35f0a2c6` / `5c79eb5ab`.
- Snapshot residual author commit `0d8988ee1`, integrated at `4ac862ef5`.
- Reviewed workflow blob `.github/workflows/pyat-w03-w04-physical-economy.yml`; actual sidecar `rawlsing_next/tests/test_bench_w03_w04_physical.py.proof.json`; preserved sidecar `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py.proof.json`.
- No author repair performed. All production/test/workflow/contract/HQ files are read-only after the existing checker's transient mutation restored.

## 2. CC-F04 actual proof gate — PASS

I ran the required existing checker on the actual committed checkout:

```sh
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  --head 4ac862ef58d06266c7de8a7cc186c5c41dd0ad48 --root .
```

Result: exit 0, `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION`,
`witness_contracts_run=2`. Both witnesses:

1. actual bench node:
   `rawlsing_next/tests/test_bench_w03_w04_physical.py::test_cli_cells_and_hash_uses_same_actual_consumer`;
2. preserved snapshot node:
   `WORKER_RETURNS/.../BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py::test_cli_cells_and_hash_uses_same_actual_consumer`.

Each receipt: baseline **PASS**, production mutation path
`rawlsing_next/_pre553_query_eval.py`, `typed_state=evaluation.fact_state` ->
`typed_state="UNRESOLVED"`, mutant **TARGET_ASSERTION_FAILED**, grade
`BOUNDED_MUTATION_DETECTED`.

Restoration:
```text
query_eval before/after = 9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920
snapshot test before/after = 01eb49d388ce29721a6658ccb1fb305683ba3a8a369c2a814c6701b5885be7e2
source status after gate: clean (only this review lease)
```

The preserved snapshot test was not renamed, removed, edited or weakened; only its sidecar was added. The actual sidecar names the exact real test and actual production dependency; no checker bypass or fabricated metadata.

## 3. CC-F03 — court and smoke PASS, trigger incomplete

- The workflow court now includes the cold lane and completion tests plus the prior sourcefree selections:
  `test_pre553_c11_execution_view.py`, `test_pre553_c11_cold_reopen_i03.py`, `test_pre553_source_backed_c11_facade.py`, `test_pre553_carrier_execution.py`, `test_pre553_i03_grouping.py`, `test_bench_w03_w04_physical.py`, `test_pre553_w03_w04_cold.py`, `test_pre553_w03_w04_completion.py`.
- Author receipt: **86 passed in 37.07s**; read, not independently rerun (no demonstrated need).
- Test diff adds two I05 assertions to the existing actual-consumer test; no assertion removal/weakening in the changed court.
- Checkout is PR head with `fetch-depth: 0`; proof gate step fetches exact PR base/head and runs the existing checker with real base/head. Correct.
- 256-row smoke is explicitly named non-100k/MCR acceptance; `acceptance_pass=false`,
  `final_matrix_eligible=false`, `NON_FINAL_DIAGNOSTIC__DO_NOT_REPORT_AS_FULL_MATRIX_PASS`. No economic threshold is claimed.
- Direct bench-helper paths are included (query common/eval/predicate, empirical query, carrier execution, repository, physical decoder, etc.).

### CCF3-R01 (P2) — CI trigger omits wrapper, verifier test, and preserved-snapshot proof paths

The `pull_request.paths` list in the committed workflow does **not** contain:

```text
WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/BENCH_LIVE_C44_SNAPSHOT/test_bench_w03_w04_physical.py.proof.json
```

The workflow does contain the original commission, TSV, checker, actual proof sidecar, proof gate and its self-test. But a PR changing only the wrapper, the verifier-checker test, or the preserved snapshot/test sidecar would not trigger this court; the claim that wrapper/checker and both proof sidecars are covered is therefore incomplete. The author return says wrapper/checker paths were added; current committed workflow has no wrapper path.

**Minimum exact repair:** add those exact paths (and any equivalent preserved snapshot proof path) to `pull_request.paths`; if the verifier-checker test should be exercised, add `CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py` to the workflow test command or a dedicated step. Do not weaken the existing 86 court, smoke boundary or proof gate; no new checker/engine.

## 4. Boundaries and remaining limits

- CC-F01 is already accepted and was not reopened.
- Current CCF5-R01 API binding remains unaccepted; this review does not reopen it. CC-F02 economics-method work and CC-F05 API-binding repair remain with their owners.
- No 100k/final matrix, no 86/256 rerun, no whole 12-ID/economic/code acceptance, no original35/SAV/DTA/DB/source bytes, native/S3/science/actor effect, install, protected merge, CI waiver, new engine/worker or model/provider/account/effort change.
- Full 12-ID/final same-SHA both-receiver code/economic/external MCR proof remains required.

## 5. Output and commit

Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/ci-proof-recheck/`. Actual model is the existing OpenCode Go DeepSeek V4.1 Flash MAX; no change.

**Final:** `REVISE` at CC-F03 scope solely for CCF3-R01; CC-F04 actual proof gate and both sidecars pass at this scope; no whole MCR or economic acceptance.
