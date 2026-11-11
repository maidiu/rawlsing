# Combined W03/W04 MCR code receiving — independent review

**Review:** independent nonauthor W03/W04 code/MCR receiver review at exact candidate `2959dda3c95b05db40a399d6d746401f434f5a38`.
**Branch/worktree:** `review/pyat-w03-w04-mcr-combined-code-r1` in the required worktree; reviewed head clean, full `rawlsing_next` source tree (406 files), not a bad/partial anchor.
**Reviewer:** existing qualified nonauthor W04 reviewer, now independent code/MCR receiver for this integrated source; previous other engineering reviewer terminated twice with provider 429/no verdict, not accepted. Same OpenCode Go DeepSeek V4.1 Flash MAX; actual turn model in `logs/actual-model.json`; no model/provider/account/effort change, no subworker.
**Verdict:** **`REVISE` / `INCOMPLETE_AT_THIS_HEAD` for the combined code and evidence.** W04 F01/F02/F03 source-level repairs pass their prior counterexamples; cold release/public-object/consumer material is exact for the tested fixtures; but cold event-sequence parity is not exact, the benchmark does not exercise the new cold streaming path, CI does not automatically run the new cold/W04 files, the existing proof gate is red on the new benchmark integration-claim test, and the frozen MCR no-drop/evidence validator cannot validate the contract artifact as written. No whole 12-ID MCR or economic acceptance is issued.

## 1. Identity, contract and prior capital

- Current combined head: `2959dda3c95b05db40a399d6d746401f434f5a38`; branch `review/pyat-w03-w04-mcr-combined-code-r1`; source tree 406/406 files; clean before this review lease.
- Frozen source/PR895: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; protected baseline `4f3413fc5c37b589be3412f826bf8f68ee617d4a`.
- Prior W04 independent review: `b5f919e65cd2dcc3df46818026a5dc9581566955`; W04 repair: `558f4169386975630f59bbb487b3fc99aee83acb`, integrated as `c2f4737e2`; current W04 blobs equal the repair.
- Cold lane: `6d3e7439d9001e0b87cd3dbd2450ce811fa41469` + `f213e15b2969b2dcf1df0955572a6c76560dd24a`; bench lane: `c44cf09fb9ca5cbc235763d8bd5df9b0074de289`; current integration includes all three.
- Frozen 12-ID contract: `PYAT_W03_W04_MCR_C_Commission.md`; source TSV at `5a891a311c70f4cb8c09864008b33405362f7c7c`, blob `b17c63cea9706f50a0d9c0f0ce064e967da4c8eb`; current TSV blob matches; 12 unique expected IDs.
- Current `OBLIGATION_STATUS.json`: `candidate_sha=null`, `goal_complete=false`, all obligations `INCOMPLETE_PENDING_SAME_HEAD_PROOF_AND_INDEPENDENT_RECEIVING`. No `RECEIVING_EVIDENCE.md`, `delivered_ids.txt`, final postcommit block, or final 12-ID PASS package exists at this head.
- Original 43-pass sourcefree run and accepted compact blobs `986f327aa18053edc61bd837cdded02bbf8388d9` / `8e8effa58579af0c3326ecd4af7e159947abe4ec` remain bounded prior capital, not current final proof. PR895 was not edited.

## 2. What independently passed

### 2.1 W04 F01/F02/F03 repairs against the prior reviewer counterexamples

The current `load_policy()` has no `PYTEST_CURRENT_TEST`/`RAWLSING_C11_ACCELERATOR_DIR` authorization fallback. Re-running the prior adversarial probe in an ordinary process:

```text
legacy_with_pytest_env_only = null
legacy_actual_cache_writes = 0
dir_fsync_failure_swallowed = {raised: true, destination_exists: false}
hidden_staging_orphan_remains = false
retention_files_after_prune = 1
```

The specific current tests `test_w04_cache_policy_spoofed_test_marker_and_legacy_dir_no_write`, `test_w04_recovery_retention_prunes_hidden_orphans_without_active_or_canonical_loss`, and `test_w04_recovery_carrier_parent_fsync_failure_cleans_only_new_publication` pass (3 passed). The current W04 test blobs equal repair `558f4169`/`c2f4737e2`. Thus:
- **F01 fixed:** ordinary env spoof cannot obtain policy or write cache;
- **F02 fixed:** directory fsync now raises, direct probe leaves no destination, carrier cleanup path passes;
- **F03 fixed:** hidden stale `.c11-events-*` staging is pruned under grace/retention, active staging survives.

The known combined cold/policy default red remains: HQ `COMBINED_COLD_POLICY_RED.json` shows normal default cache files 0 versus cold=False 1, and `COMBINED_R3_POLICY_RECOVERY_RED.json` shows the known 5 failed/5 passed selection. This review did **not** re-investigate that known composition bypass or create another patch; the coupled-default repair remains owned by the author. The W04 completion selection run in this review therefore also has known red tests; it is not evidence of a new F01/F02/F03 defect.

### 2.2 Cold release identity, public objects, materialization and consumer facts

For the sourcefree Route B fixtures `routed-ordered-repeated`, `missing-optional-weight`, and `valid-empty`, eager versus cold releases have equal release/replay identities, equal public-object `as_dict` material, and equal actual `CarrierNeutralResearchExecutor` I03/I05 consumer material. The cold helper stores only selectors/compressed bodies/non-events; no second C11 store, query engine, or hand-built statistical oracle is introduced. The cold and benchmark focused tests pass: **15 passed** (`test_pre553_w03_w04_cold.py` + `test_bench_w03_w04_physical.py`).

A direct forged-body negative was attempted by bypassing the facade pre-hash and mutating the semantic projection passed to `ColdCompactBuilder.add_event`. Resolving the event through the real `C11Repository` refused materialization with `CarrierExecutionBindingError`; the deterministic object identity check prevents a forged seal. The facade also pre-checks `sha256(event_body) == event.content_hash`. This is a **pass** for the current production path; the public/internal refs and exact material are not forged.

### 2.3 Existing validator health

- `CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --self-test`: PASS; 5 positive kinds, 32 negative mutations rejected. It checks source tuples, 12-ID no-drop, candidate SHA, grades, evidence/output paths and digests, but its full return mode was not run because no final `RECEIVING_EVIDENCE.md`/delivered IDs exist.
- `CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py` self-test: 9 tests pass, including assertion-weakening and executable severance witnesses.
- The 12-ID source TSV and expected IDs resolve: 12 unique IDs; source blob `b17c63...` matches HEAD.

## 3. Findings and minimum owner repairs

### CC-F01 (P2) — cold/eager event sequence parity is not exact

**Location:** `rawlsing_next/_pre553_w03_cold_compact.py:88-92` groups rows in physical stream insertion order; `:132-135` emits `_RespondentEvents(lane, tuple(rows))` without sorting. The eager compact view groups rows in `release.public_objects` order (`_pre553_c11_execution_view.py:439-441`), which is ref-key sorted. The real I03 selector uses `public.by_respondent` directly (`_pre553_query_predicate.py:113-115`; `_RespondentEvents.select` iterates those rows).

**Proof:** `probes/cold_parity_probe.py` / `probes/cold_parity_probe.json` shows for all three sourcefree fixtures:
```text
release_equal=true, consumer_material_equal=true, event_sequence_parity=false
selector_yield_parity=false, selector_yield_differences=3
sequence differences: 3 per fixture
```
The exact `events_by_respondent` ref sequence and `_select_respondent_events` yield order differ from eager for matching R/O/missing targets. The current query facts happen to be equal because the evaluator sorts supported multi/ordered/repeated topologies and predicates are OR/order-insensitive; this is therefore a parity/contract gap, not a false SUPPORTED fact. It is beyond the new author cold tests, which compare release/public-object refs/material but not the real selector sequence.

**Minimum exact repair:** in `ColdCompactBuilder.finish`, construct each `_RespondentEvents` from rows sorted by `self.event_keys[row]` (matching eager ref-key order), or build groups from the ordered entries. Add a parity assertion comparing `events_by_respondent` ref sequences and `_select_respondent_events` yield order against eager for the cold fixtures. Re-run the cold and real-consumer courts.

### CC-F02 (P2) — benchmark harness does not exercise the new cold streaming path; final 3-repeat matrix is NOT_RUN

**Location:** `rawlsing_next/bench_w03_w04_physical.py:327-394` `_build_release` calls `project_c11_candidate_from_physical_cells` and `validate_c11_source_release` (the eager candidate path), then compacts. It never calls `build_cold_source_backed_c11_release` or `ColdCompactBuilder`. The `cold` scenario name means process-cold, not the new cold streaming builder.

**Evidence:** the bench lane's 100k narrow numbers are preintegration/eager (`current_46b` vs protected `4f3413`): 777.53 s / 5,923,426,304 B versus 997.04 s / 5,240,467,456 B, RSS ratio 1.1303 (+13.0%; target not met). 100k wide/repeat and the final three-repetition candidate matrix are NOT_RUN. The cold lane's 10k development 16.3% RSS result is development-only. No economic PASS is issued and resource adequacy remains with the separate economics receiver.

**Minimum exact repair:** add a scenario/profile that calls the actual cold release builder (or `build_source_backed_c11_repository(..., cold=True)`) through the real I03/I05 consumer and records the same full typed/oracle material; run it at the frozen final candidate. If not added now, explicitly mark cold-streaming resource adequacy NOT_RUN rather than using eager numbers as its proof.

### CC-F03 (P2) — committed CI path/test selection misses the new cold/W04 code

**Location:** `.github/workflows/pyat-w03-w04-physical-economy.yml:5-12` triggers on only `_pre553_c11_execution_view.py`, its test, `test_pre553_c11_cold_reopen_i03.py`, `bench_w03_w04_physical.py`, `test_bench_w03_w04_physical.py`, and the workflow itself. It omits `_pre553_w03_cold_compact.py`, `pre553_source_backed_c11_facade.py`, `pre553_c11_ingest.py`, `pre553_parquet_carrier.py`, `test_pre553_w03_w04_cold.py`, `test_pre553_w03_w04_completion.py`, and the contract/TSV. The test command (`:30-38`) also excludes the cold builder and W04 completion tests. A PR changing the actual cold/facade/ingest/W04 files would not trigger this court.

**Minimum exact repair:** add the changed cold/W04 source and test paths and the contract/TSV to the trigger, and include `test_pre553_w03_w04_cold.py` and `test_pre553_w03_w04_completion.py` in the exact court. Keep the 256-row smoke explicitly non-100k. Use the existing workflow/checker; no new engine.

### CC-F04 (P2) — existing proof-integrity gate is red on the new benchmark integration-claim test

**Evidence:** `python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed --base 46b73256... --head 2959dda3... --root .` returns:
```text
PROOF_INTEGRITY_GATE_RED: rawlsing_next/tests/test_bench_w03_w04_physical.py:
material integration-claim test requires test_bench_w03_w04_physical.py.proof.json
with executable severance witness
```
The flagged test is `test_cli_cells_and_hash_uses_same_actual_consumer` (the filename/test name matches the integration/consumer claim). The gate self-test passes; the new test file has no `.proof.json`. The CI workflow does not run this existing gate.

**Minimum exact repair:** add `test_bench_w03_w04_physical.py.proof.json` with a real implementation mutation (not a test mutation) that makes the named actual-consumer test fail by assertion, and pass the existing `proof_integrity_gate_r1.py changed` command; add that gate to CI. Do not weaken assertions or add a new checker.

### CC-F05 (P1) — frozen MCR no-drop validator cannot validate the contract artifact; external postcommit evidence is not enforced

**Evidence:** the existing MCR launch/validator self-test passes, but the contract's own required command
```text
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py PYAT_W03_W04_MCR_C_Commission.md
```
returns `RED_INVALID_FOR_DISPATCH: REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK`. The frozen contract file has zero Markdown fences and is not the single fenced copy-paste prompt the validator expects. Its 12 IDs/source blob are otherwise consistent (source TSV blob `b17c63...`, 12 IDs), but the exact no-drop invocation is not runnable as written. In addition, `verify_return` reads `RECEIVING_EVIDENCE.md` text and checks committed per-ID output/evidence, but never checks that the evidence block was emitted after the candidate or is outside the defining candidate commit; the "external postcommit block" intent is procedural, not enforced. Final `RECEIVING_EVIDENCE.md`, `delivered_ids.txt`, 12 per-ID same-head PASS outputs and the final postcommit block are absent, so no whole-MCR acceptance is possible now.

**Minimum exact repair:** make the contract artifact include the expected single fenced copy-paste launch prompt (or change the contract's `no_drop_check` command to the actual fenced launch artifact), then run the existing validator with `--verify-return` at the final candidate; add an explicit existing-validator check that the evidence file/block is external/untracked at the candidate (or accept a PR/CI comment artifact with equivalent provenance). Do not create a new checker. The final code/economics receiver must resume at the same frozen final SHA with all 12 proof records.

## 4. Known excluded noise and limits

- Known normal cold/governed-cache default composition is red: `COMBINED_COLD_POLICY_RED.json` (normal 0 cache files; cold=False 1) and `COMBINED_R3_POLICY_RECOVERY_RED.json` (known 5 failed/5 passed). This review did not create another bypass investigation or patch; the author's coupled-default repair remains required.
- The full W04 completion selection in this review produced 7 failed/20 passed because it runs through the known cold default bypass; this is **not** counted as a new F01/F02/F03 finding. The specific F01/F02/F03 tests and direct probes pass.
- **100k/economics UNPROVEN:** no 100k wide/repeat or final three-repeat candidate matrix; no economic PASS from code; memory/resource utility remains with the separate economics receiver.
- **No whole 12-ID acceptance:** `goal_complete=false`, candidate SHA null, no final delivered IDs/evidence. Original 43-pass and accepted compact blobs remain bounded prior capital; PR895 is untouched.
- **No source/native/science/actor/merge:** no original35/SAV/DTA/DB/source bytes, native/S3/science/actor effect, environment install, new engine/worker, protected merge or CI waiver. Sourcefree S2 only.

## 5. Next exact action

1. Fix CC-F01 cold group ordering and add the real selector-sequence parity test.
2. Fix CC-F02 by adding an actual cold-streaming benchmark scenario/profile and marking final 100k/3-repeat NOT_RUN until run; no economic acceptance now.
3. Fix CC-F03 CI paths/tests; fix CC-F04 proof witness and run the existing gate; fix CC-F05 contract/evidence invocation and external postcommit enforcement.
4. Re-submit at a new exact integrated head; the whole code and economic receiving must then resume at the same frozen final SHA with all 12 proof records. Keep PR895 and protected terrain untouched.

## 6. Review boundary and preservation

Writes are confined to `WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/combined-code/`. All runtime/existing tests/HQ/author/peer/protected terrain were read-only. Source tree full; prior accepted compact blobs/source ceiling preserved; no source or protected merge. The actual turn model is `deepseek-v4.1-flash` / `opencode-go` / `max`, no change. Quota UNKNOWN.

**Final:** `REVISE` / `INCOMPLETE_AT_THIS_HEAD` for combined code; W04 F01/F02/F03 repairs and cold materialization/consumer material pass at tested S2 scope; CC-F01 through CC-F05 require the exact repairs above; no whole MCR or economic acceptance.
