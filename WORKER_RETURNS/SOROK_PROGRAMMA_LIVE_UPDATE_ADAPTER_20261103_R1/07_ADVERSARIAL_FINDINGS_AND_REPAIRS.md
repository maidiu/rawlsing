# SOROK-LIVE-02-R1 — adversarial findings and repairs

**Status: `EXECUTION_VERIFIED__MATERIAL_DEFECTS_REPAIRED` at execution content SHA `bbcc46bf3b7aadfc582e284daea61f99060e0fc3`. Independent review and HQ adoption remain NOT ISSUED.**

## 1. Starting condition

The starting branch `fe7b7c32bfe8aa508f556af649628930c12d9210` contained authored code, fixtures, and tests with an explicit `S2 NOT RUN` boundary. Execution at that SHA produced **25 passed** for `test_live_update_adapter.py` and **62 passed** for the P0/P1 regression suite. The authored suite therefore did not expose the defects below. The defects were found by direct source-substitution probes and by adding tests that the authored suite lacked.

No authored test was weakened, skipped, or reclassified. The repair added source binding and one view projection; it did not change grading, guide semantics, or the existing P0/P1 engine.

## 2. Material defects

| ID | Defect | Reproduction at starting SHA | Root cause | Exact correction at C1 | Regression test |
|---|---|---|---|---|---|
| D1 | `SCOPED_REVIEW` accepted a real but foreign source commit while claiming the 7bf subject | JOIN-E fixture with `source` replaced by the S35 `b65c75a9...` file and `return_sha=b65c...`; `subject_sha` remained `7bf2da30...`; intake returned `SCOPED_SOURCEFREE_ACCEPTED` | `validate_delta` checked `return_sha == source.commit` and `coordinate.source_cut == subject_sha` but never `source.commit == subject_sha` | `SOURCE_COMMIT_SUBJECT_MISMATCH` at `live_update_adapter.py:196-198` | `test_scoped_review_source_cut_must_equal_reviewed_subject` |
| D2 | `SCOPED_REVIEW` accepted a different file at the same 7bf cut instead of the exact JOIN-E return record | Source replaced by `joined/session.py` blob at commit `7bf2da30...` with quote `class JoinedSession`; intake returned `SCOPED_SOURCEFREE_ACCEPTED` | No exact source-path binding for the scoped review | `SCOPED_ACCEPTANCE_SOURCE_PATH_MISMATCH` at `live_update_adapter.py:130-131`; `JOIN_E_SOURCE_PATH` constant | `test_scoped_review_source_path_must_be_exact_join_e_return` |
| D3 | `REVIEW_REVISE` accepted the review document itself as its return source | RRIF fixture with `source` replaced by the `8090a1ea...` review file and `return_sha=8090...`; `subject_sha` remained `598d9e9e...`; intake returned `EXACT_NEGATIVE_REVIEWED` | No exact source-path binding and no source/subject equality check for negatives | Same `SOURCE_COMMIT_SUBJECT_MISMATCH` plus `REVISE_SOURCE_PATH_MISMATCH` at `live_update_adapter.py:153-154`; `REVIEW_RRIF_SOURCE_PATH` constant | `test_negative_review_source_cut_and_node_are_exact` |
| D4 | `REVIEW_REVISE` could attach the RRIF negative to an unrelated existing node | Node changed to `JOIN_E_7BF` with its known owner `JOIN_E_OWNER`; intake returned `EXACT_NEGATIVE_REVIEWED` and wrote `scoped_transition_states.JOIN_E_7BF[598d...]` | `_negative_review` checked subject and guide ref but not the exact node | `REVISE_NODE_NOT_JOIN_C12_HOLD` at `live_update_adapter.py:149`; `REVIEW_RRIF_NODE` constant | `test_negative_review_source_cut_and_node_are_exact` |
| D5 | `work-now` omitted the reconstructed `programma_live` section promised by the state and by `00_IMPLEMENTATION.md` | `ad.query(state, "work-now")` returned no `programma_live` key even when `state["work_now"]["programma_live"]` existed; new test raised `KeyError` on the starting SHA | `query()` built a fresh result dictionary and omitted the nested section | `"programma_live": state["work_now"].get("programma_live")` at `live_update_adapter.py:472` | `test_seven_views_share_one_cold_reconstructed_state`; assertion in `test_real_join_e_then_s35_cold_replay_and_one_entry_work_now` |

D3 and D4 share one validation cluster; D1 and D2 share the exact-source-binding cluster. The five concrete acceptance paths are listed separately because each had a distinct bypass.

Baseline evidence:

- `cold_replay/17_baseline_defect_repro.txt` — the first six new tests against `fe7b7c32...`: 4 failed, 2 passed.
- `cold_replay/18_baseline_defect_probe.json` — direct probes against `fe7b7c32...`: `same_cut_wrong_path`, `negative_review_as_source`, and `negative_on_unrelated_node` all returned `ACCEPTED`.

## 3. Adversarial matrix

| # | Required property | Evidence at C1 | Result |
|---:|---|---|---|
| 1 | Valid JOIN-E scoped sourcefree return and exact matching independent review | `test_real_join_e_then_s35_cold_replay_and_one_entry_work_now`; `cold_replay/03_intake_join_e.json`; review `4387dc81...`, subject `7bf2da30...`, source path exact | PASS |
| 2 | S35 authored sourcefree candidate with first consumer `NONE` | Same test; `cold_replay/04_intake_s35.json`; `code_reader=NONE`, status `SOURCE_PRESENT_CANDIDATE` | PASS |
| 3 | RRIF-R2 negative remains negative and does not revoke unrelated JOIN-E acceptance | `test_independent_negative_exact_cut_preserves_unrelated_join_acceptance`; `test_three_event_order_permutation_preserves_scoped_semantics`; `cold_replay/05_intake_rrif.json` | PASS |
| 4 | Duplicate delivery of the same transition without duplicate journal mutation | `test_duplicate_event_idempotent_no_new_journal_or_state_revision`; no write, no revision change | PASS |
| 5 | Same transition identity with changed payload rejected | `test_duplicate_transition_id_different_body_is_refused`; `test_direct_duplicate_transition_with_changed_payload_fails_closed` | PASS |
| 6 | Stale expected journal-head CAS rejected | `test_strict_cas_rejects_concurrent_writer_but_preserves_original_append_path` | PASS |
| 7 | Cold replay from the committed journal reproduces derived state | `test_real_join_e_then_s35_cold_replay_and_one_entry_work_now`; `test_seven_views_share_one_cold_reconstructed_state`; warm/cold digest `a3f84a2a...` in `06` | PASS |
| 8 | Event-order permutation preserves valid state semantics | `test_exact_order_inversion_same_claims_not_different_science`; `test_three_event_order_permutation_preserves_scoped_semantics` | PASS |
| 9 | Omitted predecessor or unsupported review does not manufacture qualification | `test_missing_transition_is_not_inferred`; `test_unsupported_negative_review_cut_is_refused`; `focus`/`goal` gates remain blocked or held | PASS |
| 10 | Fabricated source SHA, blob, owner, reviewer, source quote, or code symbol rejected | `test_forgery_and_cross_cut_refusals_do_not_append` (11 cases); `test_forged_source_commit_and_quote_are_refused_before_append`; `test_real_foreign_reviewer_commit_is_not_transferable` | PASS |
| 11 | Prior reviewer not transferable to unrelated new source cut | `test_real_foreign_reviewer_commit_is_not_transferable`; `test_forgery_and_cross_cut_refusals_do_not_append[CROSS_REVIEW]`; `test_unsupported_negative_review_cut_is_refused` | PASS |
| 12 | No sourcefree result promoted to native, human, product, or first-consumer acceptance | `test_source_free_author_fixture_never_implies_positive_acquisition`; `test_real_join_e...`; `whole.no_new_native_claim=true`; `goal` and `focus` show `target_stage_issued=false` | PASS |
| 13 | Typed source withdrawal/restoration retains original P0/P1 semantics | `test_existing_p0_p1_withdrawal_engine_is_reused_not_replaced`; `test_original_qualified_withdraw_restore_and_negative_independence`; `test_qualified_join_source_withdrawal_and_restoration_regrades_exact_delta` | PASS |
| 14 | `PROGRAMMA_DELTA` history cannot be silently erased through a forged text-only event | `test_unverified_event_erasure_of_delta_refused_and_replay_fail_closed`; `test_direct_forged_delta_event_fails_closed_on_replay` | PASS |
| 15 | Unselected C9 rule mode remains held; `ANY` is not satisfied vacuously | Assertions in the JOIN/S35, missing-transition, and S35-only tests; `cold_replay/view_4_goal_c9.json` shows `MODE_UNSELECTED_HOLD` | PASS |
| 16 | Seven entering-agent queries operate against the same reconstructed engine state | `test_seven_views_share_one_cold_reconstructed_state`; `cold_replay/` views all read digest `a3f84a2a...` at head `57a46767...` | PASS |

Matrix result: **16/16 properties exercised and passing**. This is a test/probe result, not independent acceptance.

## 4. Code corrections at C1

The repair is limited to `live_update_adapter.py` and `test_live_update_adapter.py`:

- `JOIN_E_SOURCE_PATH`, `JOIN_V_REVIEW_PATH`, `REVIEW_RRIF_NODE`, `REVIEW_RRIF_SOURCE_PATH`, and `REVIEW_RRIF_REVIEW_PATH` are exact source identities, not deployment tunables.
- `validate_delta` rejects `source.commit != subject_sha` before any append.
- `_positive_join_e` rejects a source path other than the exact JOIN-E return and a review path other than the exact JOIN-V record.
- `_negative_review` rejects any node other than `JOIN_C12_HOLD`, a source other than the exact RRIF return, and a review other than the exact `8090a1ea...` record.
- `query("work-now")` exposes the same `programma_live` section that `_recompute` already stores in `state["work_now"]`.

No assertion was weakened. The new tests assert more refusal paths, not fewer.

## 5. Residual limitations

- The adapter remains sourcefree. It does not issue native C9/C12, human A5, owner adoption, or product acceptance.
- The W8-R guide is read at `a9ebf71e...` and is not modified. `candidate-patch` remains advisory.
- The journal hash chain detects local truncation or mutation; it is not an external monotone anchor or a remote custody service.
- A filesystem actor who rewrites the entire journal and all derived state consistently is outside this adapter's threat model; replay validates the declared event types and exact Git objects, not external notarization.
- The P0/P1 regression suite is the existing engine's suite; it is not a new independent test of the adapter's science.
- No actual Sorok/Pyat production state, journal, snapshot, or protected PRE-MAIN file was read or written.
- Independent review and HQ adoption remain unissued regardless of the 16/16 matrix.

## 6. Report on `NONE FOUND`

Not applicable: five concrete acceptance-path defects were found and repaired. No material defect remains known from the executed matrix. Unknown defects outside the exercised sourcefree paths are not claimed absent.
