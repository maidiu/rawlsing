# Combined W03/W04 code review — commands, hashes and results

**Review worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-combined-code-review-r1`
**Branch:** `review/pyat-w03-w04-mcr-combined-code-r1`
**Reviewed head:** `2959dda3c95b05db40a399d6d746401f434f5a38`
**Verdict:** `REVISE` / `INCOMPLETE_AT_THIS_HEAD` for combined code; no whole 12-ID or economic acceptance.

All commands were run with an explicit `cd` into the required worktree. Source/runtime/existing tests/HQ/author/peer/protected terrain were read-only. Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/combined-code/`.

## 1. Worktree, branch, source completeness

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
review/pyat-w03-w04-mcr-combined-code-r1
2959dda3c95b05db40a399d6d746401f434f5a38
clean (only this review lease untracked before commit)
406
406
```

The `rawlsing_next` tree is complete; this is not a partial/bad anchor. Current head includes W04 repair `558f4169`/`c2f4737e2`, cold lane `6d3e7439`/`f213e15b`, bench lane `c44cf09f`, and integration head `2959dda3c`. Prior W04 review `b5f919e6` is present. PR895/frozen source remains `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; protected baseline `4f3413fc5c37b589be3412f826bf8f68ee617d4a`.

## 2. Exact changed source/test/CI blobs and SHA-256

```sh
git rev-parse HEAD:<path>
shasum -a 256 <path>
```

Result:

```text
ec5c055e6d15527af08e5a29f67f430a5896c94f  dac85324a0d90c0126ca880fcf6d849181296329a74a3420a01d96ba26f66447  rawlsing_next/_pre553_c11_execution_view.py
e7b483d451ac674cf84c84a67a6147e5cdc41d64  39ef1adfb7537a5e43168aedfda80cd72a20aab94e2074fdfb4af7556f5d8e96  rawlsing_next/_pre553_w03_cold_compact.py
4bb7e933f0a5c3f34366ee9e9013b3714a3e4341  47ddca58d432d40010c593e0faec80966bc11889af7d021303e547d00aed7ade  rawlsing_next/_pre553_w04_cache.py
eeb60c1a46db3ed072ec333dfd5d075fda3f71c0  b00cf3245ac4305ed527b38f9e899d2dc3c0edcc6410aeaae084aaaaecc8eb37  rawlsing_next/bench_w03_w04_physical.py
96d2715858281cbece4288bb7c4ba05128d81f1c  e3793af386808039f11b84e65ba1c8d265ea2f0313b47dac9be810c26cc4aa9b  rawlsing_next/pre553_c11_ingest.py
2c09deeb9b85051cb9d4c36fc12b0a193095e085  6cbb07a755fa910154ebbe7e97435f46a4a9fabe29eac468d816ddc10d2a3d51  rawlsing_next/pre553_parquet_carrier.py
f8c5707f4f4982b233a95239037d66bcf2bac6a0  e659384f9d997fd264963acfa20c398a43ab2f12f17aa8510f87da1fcb36c5e7  rawlsing_next/pre553_source_backed_c11_facade.py
d487c413507f2834a411351ae47d41abd7d6227f  01eb49d388ce29721a6658ccb1fb305683ba3a8a369c2a814c6701b5885be7e2  rawlsing_next/tests/test_bench_w03_w04_physical.py
7e8bc4e92daecffa72b1fbc740a77b8ef1a6569b  d596a01cd1ca71ccd09ba7b13ae234e779f500dec1fac8a7d719f7d9ccc90b50  rawlsing_next/tests/test_pre553_c11_execution_view.py
8ee3f1668da0a57068a7403c7e8a2c8500f15b43  e6f3729ea1093ea0faa5f61ff62ade677a14d91c6e0861972d3b7acb6640b160  rawlsing_next/tests/test_pre553_w03_w04_cold.py
7cd62ffc36091f6e36847f1498d1dc428ebda157  f62cbd2263487ee2a8c8c395434d84b100b0c0cbc7548458282ddafa32a1fa07  rawlsing_next/tests/test_pre553_w03_w04_completion.py
a12f5dcde35f4d89ff281f1ec2f02200c4ac2e36  a277f84b374ae211a2fc69afaceb293f6d958b00a94c8a28f6faa32f262c47e2  .github/workflows/pyat-w03-w04-physical-economy.yml
```

Prior accepted compact production/test blobs: `986f327aa18053edc61bd837cdded02bbf8388d9` / `8e8effa58579af0c3326ecd4af7e159947abe4ec` (bounded prior capital; test blob unchanged at prior review; W04 repair explicitly changes its own helper). Frozen contract source TSV at `5a891a311c70f4cb8c09864008b33405362f7c7c` has blob `b17c63cea9706f50a0d9c0f0ce064e967da4c8eb`; HEAD TSV blob matches; 12 unique IDs.

## 3. W04 F01/F02/F03 verification against prior counterexamples

```sh
TMPDIR="$PWD/$OUT/tmp" PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B "$OUT/probes/prior_w04_adversarial_probe.py"
```

Result (`logs/prior_w04_adversarial_probe.stdout.json`):

```text
legacy_with_pytest_env_only = null
legacy_actual_cache_writes = 0
dir_fsync_failure_swallowed = {raised: true, destination_exists: false}
hidden_staging_orphan_remains = false
retention_files_after_prune = 1
authorization_id_missing_rejected = true
retention_budget_missing_rejected = true
policy root/file symlink, 0755, missing/relative, owner-mismatch, outside-temp legacy root all rejected
invalid configured policy no legacy fallback
```

Specific current repair tests:

```sh
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py::test_w04_cache_policy_spoofed_test_marker_and_legacy_dir_no_write \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py::test_w04_recovery_retention_prunes_hidden_orphans_without_active_or_canonical_loss \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py::test_w04_recovery_carrier_parent_fsync_failure_cleans_only_new_publication
```

Result: `3 passed in 2.88s` (`logs/w04_f01_f02_f03_specific.log`). The current W04 blobs equal repair `558f4169`/`c2f4737e2`.

Known combined default context (not re-investigated): `COMBINED_COLD_POLICY_RED.json` normal default cache files 0 vs cold=False 1; `COMBINED_R3_POLICY_RECOVERY_RED.json` known 5 failed/5 passed. A broader review selection through that known path produced `7 failed, 20 passed` (`logs/w04_cold_bench_focused.log`); this is not counted as a new F01/F02/F03 finding.

## 4. Cold/benchmark focused tests

```sh
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py \
  rawlsing_next/tests/test_bench_w03_w04_physical.py
```

Result: `15 passed in 8.20s` (`logs/cold_bench_focused.log`). These are small sourcefree S2 tests; the benchmark test uses real `CarrierNeutralResearchExecutor` I03/I05 and persisted/reopened children, not a hand-built statistic.

## 5. Cold parity probe — event sequence gap

```sh
TMPDIR="$PWD/$OUT/tmp" PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B "$OUT/probes/cold_parity_probe.py"
```

Result (`probes/cold_parity_probe.json`):

```text
fixture {} : release=true, replay=true, public material=true, consumer material=true, event_sequence=false, differences=3
fixture missing_weight : release=true, replay=true, public material=true, consumer material=true, event_sequence=false, differences=3
fixture valid_empty : release=true, replay=true, public material=true, consumer material=true, event_sequence=false, differences=3
event_sequence_parity=false
selector_yield_parity=false
selector_yield_differences=3
consumer_material_parity=true
```

The real `_ReleaseIndex.events_by_respondent` ref sequence and `_select_respondent_events` yield order differ from eager for matching R/O/missing targets. Current query facts are equal because the evaluator sorts supported multi/ordered/repeated topologies and predicates are OR/order-insensitive; the exact selector sequence is still not parity (`CC-F01`).

## 6. Direct forged-body negative — no forged seal

```sh
TMPDIR="$PWD/$OUT/tmp" PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B "$OUT/probes/cold_forged_body_probe.py"
```

Result (`probes/cold_forged_body_probe.json`):

```text
forged_materialization_refused = true
error_type = CarrierExecutionBindingError
```

The probe bypassed the facade pre-hash and mutated the semantic projection passed to `ColdCompactBuilder.add_event`; the real `C11Repository` refused materialization by deterministic object identity. The facade also checks `sha256(event_body) == event.content_hash` before builder insertion. No forged seal observed (`CC-P02`).

## 7. Benchmark harness / CI audit

- `bench_w03_w04_physical.py:327-394` builds `project_c11_candidate_from_physical_cells` then `validate_c11_source_release`; it never calls `build_cold_source_backed_c11_release`/`ColdCompactBuilder`. The `cold` scenario is process-cold, not cold streaming.
- Bench receipt 100k narrow (preintegration/eager): current_46b 777.53 s / 5,923,426,304 B vs protected_4f3413 997.04 s / 5,240,467,456 B; RSS ratio 1.1303 (+13.0% regression; target not met). 100k wide/repeat and final three-repeat candidate matrix are NOT_RUN. No economic PASS; separate economics receiver.
- CI `.github/workflows/pyat-w03-w04-physical-economy.yml:5-12` triggers on only `_pre553_c11_execution_view.py`, its test, `test_pre553_c11_cold_reopen_i03.py`, `bench_w03_w04_physical.py`, `test_bench_w03_w04_physical.py`, workflow. It omits `_pre553_w03_cold_compact.py`, `pre553_source_backed_c11_facade.py`, `pre553_c11_ingest.py`, `pre553_parquet_carrier.py`, `test_pre553_w03_w04_cold.py`, `test_pre553_w03_w04_completion.py`, and contract/TSV. The test command (`:30-38`) excludes cold/completion tests. The 256-row smoke is explicitly non-100k.
- `logs/w04_cold_bench_focused.log` is the known combined default red; no bypass investigation or patch was created.

## 8. Existing proof-integrity and MCR validators

Proof gate self-test:

```sh
python3 CROSS_HQ_CONTROL_ROOM/test_proof_integrity_gate_r1.py
```

Result: `Ran 9 tests ... OK` (`logs/proof_gate_selftest.log`).

Proof gate changed:

```sh
python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  --head 2959dda3c95b05db40a399d6d746401f434f5a38 --root .
```

Result (`logs/proof_gate_changed.log`):

```text
PROOF_INTEGRITY_GATE_RED: rawlsing_next/tests/test_bench_w03_w04_physical.py:
material integration-claim test requires test_bench_w03_w04_physical.py.proof.json
with executable severance witness
```

MCR validator self-test:

```sh
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --self-test
```

Result: `PASS_SELF_TEST`; 5 positive kinds; 32 negative mutations rejected (`logs/mcr_validator_selftest.json`).

MCR contract validation:

```sh
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py PYAT_W03_W04_MCR_C_Commission.md
```

Result (`logs/mcr_contract_validate.json`, exit 2):

```text
RED_INVALID_FOR_DISPATCH: REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK
```

The contract text has zero Markdown fences; the exact no-drop command cannot validate the contract artifact as written. The 12 IDs/source blob are otherwise consistent (12 MCR_OBLIGATION records, source TSV blob `b17c63...`, HEAD TSV match). No `RECEIVING_EVIDENCE.md`, `delivered_ids.txt`, final postcommit block or 12 same-head PASS records exist; `OBLIGATION_STATUS.candidate_sha=null`, `goal_complete=false`. The validator's `verify_return` reads the evidence text but does not enforce that the block is external/untracked at candidate.

## 9. Prior capital and boundary

- PR895/source `46b7325637e68f78ccc7487d4b1abc7009c5ac0b` and original 43-pass sourcefree run retained as bounded prior capital, not final proof.
- Accepted compact production/test blobs `986f...`/`8e8e...` retained; no silent change.
- No original35/SAV/DTA/DB/source-byte read, native/S3/science/actor effect, environment install, new engine/worker, protected merge or CI waiver.
- No 100k wide/repeat or final three-repeat matrix; no economic PASS; resource adequacy belongs to the separate economics receiver.
- No whole 12-ID MCR acceptance; final code and economic receiving must resume at the same frozen final SHA with all 12 proof records.

## 10. Review output hashes

`logs/review_hashes.log` retains SHA-256 of this review, the findings, commands/evidence, probes, logs, and exact source/test blobs. The `15 passed` / `3 passed` figures are sourcefree test results, not economic or whole-contract acceptance.

**Final:** `REVISE` at `2959dda3c95b05db40a399d6d746401f434f5a38`; CC-F01 through CC-F05 require the minimum repairs above; W04 F01/F02/F03 and cold materialization/consumer material pass at tested scope; no whole MCR or economic acceptance.
