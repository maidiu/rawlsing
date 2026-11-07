# SOROK P3 final-runtime independent review — REVISE / conditional

**Reviewcut:** `d1a6817b3210880812f68090bcd2b1109ec68ef9` (parent `a04f9b0f…`).
**Protected start:** `c852d7516e23fcb6cf2215e9be7c5fa268503516` (ancestor unchanged).
**Branch:** `review/sorok-p3-final-runtime-20261106-r1`.
**Reviewer:** same distinct nonauthor reviewer, OpenCode DeepSeek V4.1-Flash `#max`. Effective model/variant verified from the OpenCode session record; quota **UNKNOWN**. This is the resumed same session after the provider DNS/transport failure; the prior partial work/logs and the HQ external snapshot were preserved, not restarted.
**Write scope:** `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/final-independent-review/` only. Runtime/tests/fixtures/production/accepted source/PROGRAMMA were not edited. No self-fix, merge, native or scientific issuance.

## Verdict

**FULL P3 GOAL — REVISE / conditional.** The actual valid P3→P2 owner chain is materially demonstrated at TEST_ONLY scope, but the complete frozen-cut A–H proof matrix is **not green**, the resource per-record metric is not valid, and two material custody gaps remain in the durable store/compression path. Full goal acceptance is withheld pending exact repairs and a focused changed-cut recheck.

- **Runtime valid chain:** conditionally demonstrated at TEST_ONLY: actual P2 root, formation of two V3MS records, later computed response and same-history contrast; owner suite 8P/1 inapplicable guard skip; store suite 51P; unit suites 36P.
- **Full13 A–H:** **REVISE** at the frozen cut. Multiple failures are demonstrably wrong test assertions/fixtures, not missing runtime psychology; the author lane must repair them within its lease and reexecute. The frozen startup contains no complete author full13 matrix/metrics; later lane claims are not this review's execution evidence.
- **Material store/compression issues:** **REVISE** (see below).
- **SCIENCE:** HOLD. **AUTHORITY:** HOLD. No native CAN/ADP, ADP016/017, original actor/B, human validity, production registry, CAS or protected merge is accepted.

## Independently executed at exact cut

All runtime/test execution used a `git archive` scratch copy of `d1a6817`; the scratch had **no runtime/test edits** (empty scratch diff). The reviewed branch remains the frozen source.

| Exact command/test | Result |
|---|---|
| `tests/test_p3_owner.py` | **8 passed, 1 skipped in 31.41s** (missing-store guard skip; actual P2/P3 owner, formation/later response/control, denial, replay, real child crash) |
| `tests/test_state_store.py` | **51 passed in 0.75s** (schema/migration/lossless V3MS, CAS, phases, cold/replay) |
| `tests/test_compression.py` + `test_projections.py` + `test_rules.py` | **36 passed in 8.89s** |
| `test_primary_actual_formation_read_later_and_no_mediator_control` | **failed in 448.23s at line 106**: `final["batch_id"] != second["batch_id"]` observed both `batch-000002`; all formation/recruit/control assertions before that passed |
| `test_e_stability_event_reveals_without_new_record` | **failed in 231.15s at line 271**: intermediate stability after-state compared to final owner snapshot after ordinary/terminal batches (`7104257d…` vs `1ea9c5a3…`) |
| `test_h_cold_reopen_idempotent_replay_and_source_restore` | **failed in 243.63s**: direct completed `owner.realize` after later batches raised `P3_REPLAY_STATE_MISMATCH` (`p3_owner.py:683`); engine-history replay was not used |
| `test_h_real_process_crash_after_base_before_psych_commit` | **failed in 3.57s**: child `EventProposal(**p["proposal"])` left `source_refs` as a JSON list; P2Owner raised `P2_ABSENT_OR_WRONG_SOURCE`; no crash occurred |
| `test_b` / `test_d` / `test_f` / `test_g` | **3 failed, 1 passed in 1115.83s**. D passed. B line 156: scheduled `objective_material_eligible=False`, expected True; F line 295: compression `HELD`, expected `BOUND`; G line 323: `STANDPOINT_IDENTITY_MISMATCH:clock` |
| `test_h_wrong_root_actor_branch_time_source_rule_version…` + `test_h_cross_root…` | **1 passed, 1 failed in 9.63s**. H identity/time passed. Cross-root failed: left/right `build_case` share the same default logical root hash, so `left.source` against right did not raise |
| `test_11_resource_receipts_are_actual_measurements` | **1 passed in 235.17s** with actual metrics, but `bytes_per_record=0.0` and `bytes_per_event=0.0` (see resource finding) |
| Same-history diagnostic (review probe) | FORMATION: head count 2, later `joint_check`/`private_check`; STABILITY: head count 0, later `inspect_alone`. This proves the persisted record effect that the official no-history control does not isolate |
| Compression four-event probe | SINGULAR `BOUND`, REPRESENTATIVE `BOUND`, ACCUMULATED `HELD` (`ACTUAL_INTERVAL_UNAVAILABLE`, interval `NOT_PERFORMED`, 0 perceptions), RETROSPECTIVE `BOUND` |
| Compression crash-gap probe | Bind failure after effect commit → phase `PSYCH_COMMITTED`; recovery completed `REALIZED`/`COMPLETE` **without** `test_only_compression_evidence` |
| Store result-link probe | `store.finish` accepted a result with omitted receipt link, `receipt_ref='P3:forged'`, arbitrary `accessible`; operation `COMPLETE`; `verify()` True |

Logs/receipts: `logs/`, `reproductions/`, `logs/source-pin-check.json`.

## Material findings (must fix)

### M1 — Store result is not linked to the effects receipt; `verify` accepts forged result

`p3/state_store.py:_validate_result` only checks `effects_receipt_hash`/`effects_receipt` when those keys are present in `result["consequences"]`. The actual `P3Owner._result` does **not** include an effects-receipt link. The independent probe omitted the link, set `receipt_ref='P3:forged'` and `accessible={'forged_actor_surface': True}`, and `store.finish` accepted it; `store.verify()` returned True. This breaks the promised immutable result/durable receipt linkage and lets a caller replace the actor-visible result after `PSYCH_COMMITTED`.

Minimal correction: include `effects_receipt_hash`/`effects_receipt` in the P3Owner result, require it in `PsycheStore.finish`, verify the receipt/response hash and `receipt_ref` against the stored effects receipt, and add an omitted-link negative test. No new gate or theory.

### M2 — Compression evidence is lost on recovery after `PSYCH_COMMITTED`

`p3/p3_owner.py:_effect` commits the durable effects receipt first and runs `compression.bind` afterwards. The receipt/response does not carry the compression envelope. In the independent probe, an injected `compression.bind` failure left the operation `PSYCH_COMMITTED`; retry through `_existing_effect` completed `REALIZED`/`COMPLETE` with **no** `test_only_compression_evidence`. A crash/exception at that boundary can therefore complete a compression-designated event without its evidence.

Minimal correction: compute the deterministic compression envelope before `store.commit_effects` and persist it in the receipt/response, or recompute it in the `PSYCH_COMMITTED` recovery path and verify its hash before `finish`; add that exact crash-boundary test. Do not fabricate an interval or fabricate participant access.

### M3 — Resource per-record/event bytes are not actual

The resource test passes, but the actual metrics report `db_bytes=4096`, `wal_bytes=1,413,192`, `bytes_per_record=0.0`, `bytes_per_event=0.0`. `measure_case` subtracts main-DB bytes only, so WAL-resident state is ignored; `test_11` asserts only `is not None`. The §11 storage requirement is therefore not met by the named metric.

Minimal correction: use actual DB+WAL/incremental bytes (or checkpoint the store before measurement), assert positive per-record/event bytes, and retain main/WAL separately. This is measurement repair, not a new performance gate.

## Fixture/assertion defects (not automatically runtime defect)

These are exact failures of the frozen test harness; the author lane is separately repairing them. They must not be weakened, renamed or silently skipped.

| Test | Exact defect | Minimal correction |
|---|---|---|
| Primary line 106 | `final["batch_id"] != second["batch_id"]` is false; `RecursionCycle.finish` returns the terminal retrospective for the same pending batch | Assert equality or validate terminal retrospective/history hash, not a different batch ID |
| Primary control line 61/118 | Control uses `history_outcomes=()`, so it is a no-history actor, not a same-history no-record control; positive/control difference is confounded | Hold history fixed and suppress formation (e.g. phase `STABILITY`) or sever exact records; the same-history probe demonstrates the correct contrast |
| E line 271 | Intermediate stability `after.state_hash` compared to final owner snapshot after later batches | Capture the post-bootstrap snapshot or compare the stability record/head only |
| Cold line 441 | Direct completed `owner.realize` after later batches demands current-head replay; runtime correctly refuses `P3_REPLAY_STATE_MISMATCH` | Use `engine.history`/exact #704 completed-replay semantics; do not demand a new historical-current-head contract |
| Crash child | `EventProposal(**p["proposal"])` leaves `source_refs`/`participants` as lists; P2Owner expects tuples | Normalize to tuples, as the passing `test_p3_owner` crash child already does |
| A line 131 | `recognized.owner.initial` attribute does not exist on `P3Owner`; source inspection; not independently executed | Use `VerticalCase.initial`; do not add a new owner attribute |
| B line 156 | `SCHEDULED_ONLY` after prior ACTUAL intervals has `material_eligible=False`; test assumes interval label controls material feasibility | Vary legitimate actual material opportunity with fixed psychological history; material feasibility stays P2-grounded |
| C/G line 323 | Standpoints built at initial clock are passed with a later event identity; projection correctly rejects stale clock | Update standpoint clock/hash to identity (as `P3Owner._standpoint` does) or build at that clock |
| F line 295 | Event-3 ACCUMULATED interval is `NOT_PERFORMED`; compression correctly returns `HELD`; test expects `BOUND` | Use an actual positive interval event with material/actor access; do not force BOUND |
| H cross-root line 419 | `build_case` left/right share the same default logical root hash; this is a replica, not a foreign root | Construct an actually foreign root or explicitly test the replica; do not invent a migrated positive fork |
| Resource test | Passes with zero per-record/event bytes | Use DB+WAL/checkpoint and assert positive values |

## Runtime disposition

The valid owner/store/later-reader chain is **conditionally demonstrated at TEST_ONLY scope**: the owner suite (8P/1skip), store suite (51P), primary core through recruit/control, same-history contrast, and resource two-batch chain all ran on the actual P2 root. The runtime correctly keeps `MISSING_RULE`/no native action, honors source/config/rule/root/clock denials, and preserves the E1/S1 scoped inputs. It is **not** full P3 A–H acceptance because the frozen full13 is not green and M1–M3 remain.

## Resource / counterfactual / holds disposition

- **Resource:** actual two-batch chain: 3 provider calls, 2 batches of 3 events, 2 retrospectives, 6 event latencies, batch latencies 36.705s / 168.553s / 17.271s, cold open 10.724s, 2 P3 records, DB 4,096 B + WAL 1,413,192 B, provider context 4,359 B, 6 targeted queries, 9 full-verify row reads. `bytes_per_record/event` are invalid (M3).
- **Counterfactual:** same-history FORMATION vs STABILITY produced 2 records → `joint_check/private_check` vs 0 records → `inspect_alone`; the official no-history control is weaker but the runtime difference is real. Material/context/contradiction and opacity unit paths pass; full13 B/C/D/F/G/primary assertions are not accepted as written due the fixture defects above.
- **Holds:** no native CAN/ADP, ADP016/017 memory/claim, original actor/B, human validity, production registry, CAS or protected merge. E1/S1 remain scoped design inputs. No full13 author matrix/metrics is present in the frozen startup; separate lane claims are not this review's execution evidence.

## Required fixes vs residual uncertainty

**Required before full acceptance:** M1 store result linkage; M2 compression recovery evidence; M3 resource metric; repair and reexecute the fixture/assertion defects above; provide the complete author full13 matrix/metrics at the corrected exact cut. **Not required/new:** no speculative performance gate, new psychological theory, native rule issuance, or new proposal grammar. **Residual uncertainty:** A/C were source-inspected only, not independently executed here; full13 author execution was delegated separately and is not accepted; corrected-cut recheck remains necessary.

Science and authority remain HOLD. This review grants no merge or native receiving.
