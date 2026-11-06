# Developmental batch engine receipt

Status: **ENGINEERING PASS AT THE SPECIFIED ABI SCOPE**. HQ still decides after independent review. This is not a protected merge, native/source issuance, scientific acceptance or human-validity claim.

## Delivered

- `developmental_recursion/engine.py` — `BatchEngine(owner, journal_path)` with `run_batch`, `history`, `verify`, and the actual owner exposed as `engine.owner`.
- `tests/test_engine.py` — 42 core tests using a stateful software owner fixture with durable operation receipts.
- `batch_evidence/` — commands, source pins, sanitized passport and reproduction receipts.

Not implemented here, as commissioned: P2 adapter, `model_cycle.py` coordinator, or any production file. ABI, `contracts.py`, accepted P2 code and other workers' files were not changed.

## Mechanism

- SQLite journal with atomic `BEGIN IMMEDIATE` writes, WAL, `synchronous=FULL`, stable operation IDs and a per-event hash chain plus `history_hash = digest(records)`.
- Root/actor/branch binding is recorded on first open and checked against the actual owner, journal metadata, every batch and every owner result.
- Exactly 3–5 detached proposals are structurally validated, then all are owner-validated before any reservation or effect. Owner mutation during validation is refused before effects.
- Before each owner call the next state is snapshotted and checked against the preceding realized `after`; the reservation (operation ID, proposal hash, before state) is committed first.
- Owner results are checked for type, operation ID, proposal hash, exact before identity, current after identity, root/actor/branch, nondecreasing clock, core status, JSON-safe detached content, readset and nonempty receipt.
- Completed same-input replay returns the stored result without another owner realization. Different material under the same batch or event ID is refused.
- Interrupted reservations are durable. A retry offers the **same** operation ID. A receipt-bearing owner resolves it; an owner without a receipt may refuse as ambiguous. The engine preserves the reservation and never invents a replacement operation or repeats an unknown effect.
- Partial history is available from the valid completed prefix. `verify` checks metadata, batch identity, proposal material, ordering, before-state chaining, record/result/readset/receipt copies, chain hashes, history hashes, completion state and orphan events.

## Acceptance mapping

| Commission requirement | Evidence |
|---|---|
| SQLite durable journal, exclusive execution | `test_exclusive_concurrent_same_batch_realizes_effects_once`; `CROSS_PROCESS_EXCLUSIVE.log` |
| Root binding | `test_journal_binds_the_actual_owner_identity`, `test_invalid_root_branch_or_rolling_clock_is_refused_before_new_effects` |
| Hash chain | `test_journal_hash_chain_tamper_fails_history_and_verify`, `test_journal_meta_tamper_and_missing_event_fail_verify` |
| Strict 3–5 validation before effects | `test_batch_requires_exactly_three_to_five_valid_proposals_before_effects`, `test_all_five_proposals_are_validated_before_any_realization` |
| Current state between steps | `test_each_step_receives_the_actual_post_event_state_and_persists_readset` |
| Source readset | same test; hard-crash and cross-process evidence |
| Reservation before owner call | `test_interrupted_after_receipt_recovers_the_same_operation_without_duplication`; `HARD_CRASH_RECOVERY.log` |
| Idempotent completed replay | `test_completed_replay_is_identical_and_does_not_call_the_owner_again` |
| Safe ambiguous recovery | `test_ambiguous_retry_is_held_and_never_silently_reissued` |
| Malformed/non-finite data | `test_batch_requires_exactly_three_to_five_valid_proposals_before_effects` |
| Forged owner results | ten parameterized cases plus `test_a_forged_result_can_be_recovered_through_the_same_owner_operation` |
| Operation/proposal/before/after/clock/status/receipt checks | forged-result parameterization and `test_invalid_root_branch_or_rolling_clock_is_refused_before_new_effects` |
| Interrupted progress not dropped | `test_interrupted_progress_is_visible_and_resumable_without_replay`; `HARD_CRASH_RECOVERY.log` |
| Order matters through owner state | `test_order_matters_through_actual_owner_state` |
| Scientific hold explicit | `test_held_and_missing_rule_are_preserved_and_never_become_no_change` |
| No fixed story/actor/workshop in runtime | `test_generic_identifiers_round_trip_and_engine_has_no_fixed_story_tokens` |

## Observed execution

```text
python3 -m pytest -q tests/test_engine.py
42 passed in 0.60s

hard crash:
  child exit                         17
  batch after crash                  RUNNING
  event 0 after crash                RESERVED, result_json=null
  recovery event_ids                 e1,e2,e3
  recovery statuses                  REALIZED,REALIZED,REALIZED
  scientific consequences            MISSING_RULE x3
  verification                       true

cross-process exclusivity:
  owner order                        a1,a2,a3,b1,b2,b3
  duplicate effects                  0
  final clock                        6
  verify                             true
```

## Source and authority

- Startup/ABI commit: `0d4edae634b3ef19643a7d0eb7752081013e5d83`.
- Code commit: `27645b56cddf361403609c5c6cc22b35757ccad5`.
- Branch: `agent/sorok-recursion-batch-20261106-r1`.
- Architecture pin: `fbfc529230d8b3c13f824cfac31741a5dfaa57e5:SOROK_PRODUCT_CONTROL_ROOM/USER_DIRECTED_ARCHITECTURE/20261026_USER_SETTLED_BATCH_RECURSION_IMPRESSION_MEMORY_R1.md`.
- Model/runtime: `opencode-go/deepseek-v4.1-flash#max` in OpenCode. Quota was not observed: **UNKNOWN**.
- Authority: local source-free implementation only. No merge, native issuance, source issuance, protected receiving or human-validity claim.
- Scientific holds remain exact: unavailable propagation/coupling, impression/memory formation, developmental transition rules, native source issuance, independently owned B behavior and protected receiving.

The evidence packet commit is the branch head after this file is committed. HQ decides after independent review.
