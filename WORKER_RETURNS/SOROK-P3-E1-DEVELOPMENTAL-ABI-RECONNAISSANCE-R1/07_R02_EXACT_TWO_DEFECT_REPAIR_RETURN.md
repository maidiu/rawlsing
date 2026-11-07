# Sorok P3-E1 — R02 exact-two-defect bounded repair return

**Status:** IMPLEMENTED / S0–S1 GITHUB SOURCE; **S2 LOCAL TARGETED TESTS PASS AT `992779441`** (see [08 — S2 local execution addendum](08_S2_LOCAL_EXECUTION_ADDENDUM.md)). This is an implementation and executor record, **not independent R02 reacceptance**.

**PR:** #735 / existing branch `research/sorok-p3-e1-developmental-capital-abi-recovery-20261106-r1`.
**Original reviewed head:** `ee1ff298fe7e57277c34a5af16df33165743d84f`.
**Protected start/current at repair:** `c852d7516e23fcb6cf2215e9be7c5fa268503516`.
**Receiving defect commission:** https://github.com/maidiu/rawlsing/pull/735#issuecomment-6697602420
**Repair code commits:** `616115e11b753c22ed4d143bdf8302734b043a42` (adapter), `5593eed6e0aa98f63d360a3af7856222f8e0fd3a` (new tests), `938367e927eed97b007809f5139c96f888e47d95` (probe cold reopen), `a22f32e47c95e7941610e6a74e5e571a1d95afe7` (probe documentation). Final commit containing this return is recorded by the GitHub PR branch HEAD, not inferred from this self-referential document.

## D1 — per-event committed psychological transition, not inherited state

In `probe/b1_owner_adapter.py`, after the B1 transaction returns `COMMITTED`:
- Compare pre/post arrays of `state["middle"]` and `state["transitions"]`, preserving exact prefixes.
- Derive `committed_middle` and `committed_transitions` from newly appended entries only.
- Require cardinality agreement with the B1 transaction's `receipt["owner_decisions"]` and refuse an impossible journal-only committed mediator.
- Set `durable_psychological_transition` to `TEST_ONLY_B1_V3MS_MEDIATOR` **only when** the operation committed new mediator(s) with corresponding decisions; set `TEST_ONLY_VALID_EMPTY_NO_NEW_MEDIATOR` when none were committed in the normal mode; and `TEST_ONLY_JOURNAL_ONLY_NO_DURABLE_EFFECT` for the controlled no-commit mode.
- Preserve existing `middle_state_ids` / `middle_state_record_hashes` as cumulative inventory; add `new_middle_state_ids` / `new_middle_state_record_hashes` as exact per-operation delta.

Thus event 1's positive writer remains positive, the dormant event 2 is not credited with a new mediator, event 3 recruits the old mediator but creates no new one, and all journal-only events have an explicit zero-durable-effect grade. No production code or scientific registry was modified.

## D2 — immutable owner mode binding across cold reopen

The adapter now persists `journal_only` as an integer-constrained metadata column of `b1_owner_meta`, checks type at construction, and verifies it in `_verify_source()` every snapshot and operation. Reopening with a different mode raises `B1_OWNER_EXECUTION_MODE_MISMATCH`; legacy unbound table schema fails closed as `B1_OWNER_MODE_BINDING_MISSING`. Constructor validation failure closes the store connection. The TEST_ONLY `source_ref` remains based on the same B1 fixture and rule identities, maintaining identical positive/control proposal/event hashes; operating mode is separately immutably bound to that DB/root and cannot silently drift. The new mode bit is not presented as original science or newly added to `StateIdentity`.

`run_probe.py` reopens in the same `journal_only` mode as the initial DB. The old cold control's implicit `False` reopen was a mode-drift assumption that had to be removed under the new custody rule.

## Newly added regression tests

`test_b1_owner_adapter.py` now contains **12 test functions, 13 pytest cases** (the cold mode test has two parameter values), compared with 9 on original reviewed SHA:
- `test_per_event_mediator_grade_counts_only_new_committed_targets`: event1 positive delta, event2 NO_CHANGE/no delta, event3 stored-mediator recruitment without new delta, journal-only three zero-durable cases, exact state-vs-delta distinction.
- `test_cold_reopen_mode_binding_refuses_flip_and_preserves_future_writes` in both regular and journal-only modes: wrong-mode reopening rejects; original-mode reopening retains snapshot and can perform new event1, close again, then event2/event3 with expected later action and count.
- `test_mode_metadata_tamper_refused_and_exactly_restored`: tampered persistent execution mode refuses snapshot; restoring metadata restores original identity.

Existing nine original tests plus the four R02 cases pass (13/13), including source/response severance and restore, idempotency, production `DENY_ZERO_EFFECT` and cold replay.

## Executed vs not executed / custody truth

**Performed:** S0–S1 private GitHub PR/current-ref checks; exact source reads, deterministic bounded text substitutions, sequential GitHub contents-API commits, exact SHA readback, static inspection of mode bindings/per-operation fields/new tests/probe reopen. PR remained on the same branch; no protected writes/merges.

**NOW RUN at `992779441`:** the corrected vendored-B1 command executed locally. Adapter **13/13**, vendored B1 **39/39**, engine core **45/45**, engine coordinator **19/19**, and `run_probe.py` **exit 0**; positive `joint_check:caretaker`, control `inspect_alone:caretaker`, same later event hash, production guard `DENY_ZERO_EFFECT`. `probe/receipts/PROBE_RECEIPT.json`, `junit.xml` and `source_pin.json` were regenerated for the new head. This is executor evidence, not independent R02 reacceptance.

## Exact next S2 verification

Use an isolated clean worktree at final PR #735 HEAD, matching protected source pins; do not reset another worker's local branch. From the repository root and the indicated directories:

```bash
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_engine.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_model_cycle.py

cd WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1
python3 -B -m pytest -q -p no:cacheprovider test_bfirst.py

cd ../..
python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py
python3 -B run_probe.py
```

The B1 author test and fixture are vendored byte-identically under `probe/vendor/B1/`, so the command works from a clean protected checkout. Preserve exact source SHA pins and inspect the regenerated receipt: `middle_state_count`, `durable_psychological_transition`, per-event `new_middle_state_*`, identical later event/proposal hashes, actor action difference, journal-only cold read, two-way mode refusal, and the production empty registry.

Test direct mode-flip negative -> RED/typed refusal -> same-mode cold continuation PASS. Check source/probe mutation restoration and unchanged worktree. If the new test fails, repair on this PR branch and rerun at actual new HEAD; do not claim accepted S2 from this document.

## Required receiving holds

Independent **different** R02 re-review of actual new test-run SHA; native CAN-008/011 and ADP-016/017 rules, scientific issuer/actor/B, P2 actor-root psychological store and transaction, real later P2 actor-action/response consumer, original V3 archive, memory formation, C8/C9/C12/ADP-019 and protected PRE-MAIN merge all **HELD**. Inherited Pyat FIABC/LiTS 144/3 court pin drift is separate: no repinning, waiver or hidden green.

**Verdict:** `IMPLEMENTED_SOURCE_ONLY__S2_REPLAY_REQUIRED`. No production psychological authority, protected merge or self-acceptance.
