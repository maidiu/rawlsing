# INDEPENDENT TEST AND FAULT RECEIPTS

## Environment

- Host: macOS, Intel x86_64.
- Python: 3.11.3 at `/usr/local/bin/python3`.
- pytest: 9.1.1. E5's receipt used pytest 9.0.2; the candidate results were re-run here under 9.1.1.
- E5 detached test checkout: exact `96e6d49ac18274332751c5fbb87c6ed370e8fd9c`.
- PRE-MAIN baseline checkout: exact `8e44ca9c751049d65e6def47600b5c073ee04b29`.
- Every run used `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.`, `-p no:cacheprovider`.
- No real source, native survey, actor, API, network or model execution.

## E5 court results

All commands below were run from the E5 checkout.

### Unfiltered claim to falsify

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py \
  rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py \
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  <S06FR-overlay>/test_hq284_s06fr_native_review.py
```

Result: **179 passed, 14 failed, exit 1, 0 skipped, 0 errors.** The claim was reproduced exactly. Log: `test_receipts/e6_unfiltered_e5.log`.

The 14 failures are exactly:

- `test_17_binding_cannot_resolve_different_release`
- `test_18_endpoint_failover_only_among_same_release`
- 12 unmodified S06FR `OBSERVED` historical defect-presence tests:
  - `test_OBSERVED_direct_b5_append_bypasses_native_preflight[RECERTIFIES]`
  - `test_OBSERVED_direct_b5_append_bypasses_native_preflight[CURRENT_SELECTED]`
  - `test_OBSERVED_direct_b5_append_bypasses_native_preflight[PRODUCT_PUBLISHED]`
  - `test_OBSERVED_direct_m2_insert_bypasses_type_and_preflight`
  - `test_OBSERVED_publication_payload_not_bound_to_subject_on_cold_replay[replay_root_ref]`
  - `test_OBSERVED_publication_payload_not_bound_to_subject_on_cold_replay[determinant_set_hash]`
  - `test_OBSERVED_publication_payload_not_bound_to_subject_on_cold_replay[producer_permission_ceiling]`
  - `test_OBSERVED_publication_torn_after_event_append`
  - `test_OBSERVED_m2_check_then_insert_race_overwrites_collision`
  - `test_OBSERVED_concurrent_b5_selection_accepts_two_stale_predecessors`
  - `test_OBSERVED_public_event_payload_changes_internal_identity`
  - `test_OBSERVED_rebuild_receipt_can_link_event_for_different_release`

### Filtered selection

```sh
... -k 'not OBSERVED and not test_17_binding_cannot_resolve_different_release and not test_18_endpoint_failover_only_among_same_release'
```

Result: **179 passed, 14 deselected, exit 0.** This is a selection, not a green full court. Log: `test_receipts/e6_filtered_e5.log`.

### Per-court

| Court | Command | Result | Log |
|---|---|---|---|
| Accepted B5 | `pytest -q rawlsing_next/tests/test_pre553_learned_product_lifecycle.py` | 39 passed, exit 0 | `e6_court_b5.log` |
| Accepted M2 | `pytest -q rawlsing_next/tests/test_pre553_learned_product_release.py` | 26 passed, 2 failed, exit 1 | `e6_court_m2.log` |
| S06G repair | `pytest -q rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py` | 42 passed, exit 0; 6/6 consecutive runs | `e6_court_s06g.log` |
| E2 independent | `pytest -q rawlsing_next/tests/test_pre553_e5_s06g_independent_hostile.py` | 10 passed, exit 0; 12/12 consecutive runs | `e6_court_e2.log` |
| Adjacent | `pytest -q test_pre553_ee14_selected_current_asof_hq260.py test_pre553_learned_world_composition.py` | 45 passed, exit 0 | `e6_court_adjacent.log` |
| S06FR overlay | `pytest -q <exact overlay blob a25cf5a...>` | 17 passed, 12 `OBSERVED` failed, exit 1 | `e6_court_s06fr.log` |

The S06FR overlay was extracted from `1b5b6072` blob `a25cf5a5ecec4b473ccceaec8a032747d804da7d`, SHA-256 `fea7cb29f6056996fd999cf50ddc227671024946e32af313f7954b1d30eecf30`, and was not edited.

## PRE-MAIN baseline comparison

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py
```

Result: **67 passed** = accepted B5 39/39 + accepted M2 28/28. Baseline M2 is green; the E5 cost is exactly the two accepted-fixture failures. Log: `test_receipts/e6_baseline_b5_m2.log`.

E2 court on unpatched PRE-MAIN:

- First run: **9 failed, 1 passed**.
- 12-run sample: **6 runs at 9 failed/1 passed; 6 runs at 10 failed**. An earlier 12-run sample split 7/5 the same way.
- The nondeterministic case is `test_concurrent_selection_one_winner_one_conflict_and_cold_restore`; the unpatched race does not lose on every schedule.
- On E5 the same E2 court was **10 passed in 12/12 runs**.

This is an honest evidence limitation on E2's "baseline 10/10 failed" claim, not a candidate failure. The S06G 42-case court contains its own 12-trial race and is stable on E5. Logs: `test_receipts/e6_baseline_e2.log` and `test_receipts/e6_baseline_e2_12run.log`; candidate stability is in `test_receipts/e6_candidate_e2_12run.log`.

## Reviewer-owned adversarial court

File: `reviewer_tests/test_e6_independent_review.py`, SHA-256 `eb3037cd1612ca17792e802bdcd76c0f5268d87a82f0fc05d3f78c2d6412839e`. It was run against the E5 checkout, not against a modified reviewer tree.

Result: **11 passed, exit 0.** Log: `test_receipts/e6_independent_review.log`.

Covered behaviors:

1. M2-17 independent early `RELEASE_UNAVAILABLE`, atomic store refusal, lawful foreign subject/closure/release import, then `PUBLICATION_BINDING_MISMATCH`.
2. M2-18 independent early refusal, lawful import, preserved cross-release failover `PUBLICATION_BINDING_MISMATCH`, and same-release failover success.
3. Direct `register_release` of a foreign release requires local subject and closures; stores unchanged on refusal.
4. Direct `register_binding` refuses a wrong publication contract without mutation and accepts the correct contract.
5. Nested event payload mutation raises `TypeError`; event ref stays stable; `as_dict` export is detached.
6. Cold restore detaches the caller's checkpoint; later deep mutation and clearing of the caller's containers do not change the restored checkpoint.
7. A rehashed publication event substituting `replay_root_ref` is refused on cold replay.
8. Two-writer selection race: one winner, one `LearnedProductLifecycleConflict`, cold replay equal, 8 independent trials.
9. Saved `_append_events`, `_commit_selection_transition_receipts`, M2 `_insert` and `B5.stage_release.__wrapped__` refuse outside an owner transaction.
10. `LOCAL_UNAUTHENTICATED` is honest; external/protected mode causes `EXTERNAL_ISSUER_HOLD`; saved alias does not elevate.
11. M2 competing subject preimages: one winner, one `SEMANTIC_REOWNERSHIP_ATTEMPT`, no overwrite.

## Fresh-process checkpoint replay

A checkpoint was exported, JSON-serialized, loaded in a fresh Python process, restored through `LearnedProductLifecycleExecutor.from_checkpoint`, and re-exported. Result:

```text
export_hash 3f7a7e074a2b94e099ea558560191f812c650fce9ad39d126d29b900840dca98
restored_hash 3f7a7e074a2b94e099ea558560191f812c650fce9ad39d126d29b900840dca98
hash_equal True
canonical_equal True
strict_container_equal False
```

The checkpoint hash and canonical semantics match. Strict Python equality is false only because six canonical pair rows return as tuples after JSON rather than the original lists. This is representational, not a semantic mismatch. Log: `test_receipts/e6_fresh_process_checkpoint.log`.

## Fault coverage summary

| Fault / boundary | Evidence | Result |
|---|---|---|
| Foreign M2 representation/binding injection | Independent M2-17/18; accepted tests | Early typed refusal; stores unchanged; downstream oracle preserved after lawful import |
| Post-append failure rollback | S06G 14 event + 3 non-event mutators; E2 torn publish | PASS |
| M2 post-insert failure rollback | S06G five M2 writers | PASS |
| Two-writer B5 selection | S06G 12-trial; reviewer 8-trial; E2 candidate 12 runs | One winner/one conflict; cold replay |
| Two-writer M2 subject collision | S06G; reviewer | One winner/no overwrite |
| Detached event mutation | S06G; E2; reviewer | TypeError; stable ref |
| Caller checkpoint detachment | Reviewer | Restored state unaffected by later caller mutation |
| Rehashed publication/receipt tamper | S06G; E2; reviewer | Typed conflict |
| Saved helper / unwrapped body misuse | S06G; E2; reviewer | Typed transaction refusal |
| Reader during interrupted transaction | S06G | Reader waits; sees pre-call checkpoint |
| External/protected mode | E2; reviewer; S06G | `EXTERNAL_ISSUER_HOLD`; LOCAL remains honest |

Captured pytest logs in `test_receipts/` were normalized by removing trailing spaces and blank-line padding for repository whitespace hygiene; pass/fail counts, test identities and exception text are otherwise verbatim.

No SKIP was observed in any E5 run. No error was observed. The only RED results are the two accepted M2 fixture conflicts and the 12 intentionally obsolete S06FR `OBSERVED` defect-presence assertions.
