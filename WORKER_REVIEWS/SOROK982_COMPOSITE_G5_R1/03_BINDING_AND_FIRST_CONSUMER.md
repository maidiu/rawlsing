# Binding, trust model and first-consumer proof

## 1. Defect and correction

The original hostile probe at `c597024bb` replays an authentic `APPROACH` receipt from clock 248 after a real `WAIT 4` has moved the world to clock 253, with a caller-chosen interval `{start: 247, end: 253}`. It returned `True` on `4cbf67398` before the composite change. It returns `False` at `ff30c13ee`.

The composite correction in `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py` introduces three owner checks:

1. `_owner_current_interval` (lines 136-162) reads the latest `S46_INTERVAL_STATE` from `session.read_interval_states()`, requires `currentness == CURRENT`, requires the caller interval to equal that owner state's start/end, requires its end to equal `world.clock`, and matches root, branch and actor from the live session.
2. `_bound_interval_receipt` (lines 165-182) requires the caller's `source_receipt["interval"]` to carry the same `state_id`, `receipt_hash`, `episode_id`, `domain_issuance_id`, start, end, root, branch and actor as that owner state.
3. `_current_operation_conduct` (lines 185-223) finds the unique `P6_HOUSE_CONDUCT` committed between the previous and current `S46_INTERVAL_STATE`, reads it through the actor-scoped `session.episodes(user)` reader, and requires its clock and `{event_id, operation}` body to match the authentic world event.

The outward-cue branch at lines 306-312 now calls `_current_operation_conduct`; it no longer accepts any historical conduct with a matching clock/body anywhere in the actor's episode list. The near-term self-action/speech paths use the owner state's `start`/`end` (line 252), so a widened caller interval cannot re-open a historical event.

## 2. Trust model: owner facts vs caller inputs

Owner-produced facts used for authority:

- `S46_INTERVAL_STATE` episode produced by the existing S46 producer, including `state_id`, `receipt_hash`, `episode_id`, `domain_issuance_id`, root, branch, actor, start and end. `read_interval_states` validates the state body and recomputes `CURRENT`/`SUPERSEDED` from actual episode order.
- The `P6_HOUSE_CONDUCT` episode committed by the existing P6 outward owner, read through the actor-scoped episode reader.
- The performed world event in the existing P2/BP4 store and its hash/clock.
- `session.read_root()`, `session.branch_id`, the live world actor, and the checkpointed sensory conditions used by `sensory_candidate`.

Caller-provided inputs:

- The helper arguments `interval`, `world`, `house`, `packet`, and `source_receipt`.
- `packet["cues"]`, `recent_self_actions` and `recent_speech` are caller-visible candidates; each admitted outward row must still match the authentic current event, the owner state, the current operation conduct and the source-derived sensory cue.

The caller interval is therefore **a request to be matched**, not authority. The authority is the owner state found in the episode store; the receipt must identify that exact state. The caller cannot widen time because the owner state's start/end are used for every bound. The caller cannot replay an old operation because the old receipt does not identify the latest owner state, and a copied latest interval identity on an old event fails the current-operation conduct/window or the world-event lookup.

Residual raw internal trust, explicitly retained:

- A caller that already controls the live session object can monkeypatch owner readers. The receiver's revocation probe deliberately simulates this by making `session.episodes(user)` return `[]`; the helper correctly refuses. This is not a protected public API boundary.
- `qualified_p3_read(actor_observed=True)` remains raw internal trust: the caller supplies the boolean. The receiver baseline test `test_explicit_internal_trust_boundary_not_mistaken_for_protected_source` confirms `actor_observed=False` yields no records, `actor_observed=True` yields sourcefree records, and no native memory/action is issued.
- `world` and `house` arguments are still caller-supplied. The normal first consumer reads them from `read_house(session)`; the helper does not independently re-open the store. This is a known direct-internal-caller limit, not a claim of a protected API.
- Full crash recovery is not claimed. P4 pending requires reconciliation; `_owner_current_interval` catches owner-reader exceptions and returns `None` (fail-closed). Same-request retry conservation and later-operation supersession are tested; S46 condition-revocation injection and crash-injection recovery are not independently re-proven here and remain held.

## 3. Same-clock/other-operation strength

The author's same-clock test uses two deterministic genesis states, then `APPROACH` in one and `ORIENT` in the other. The reviewer's independent exploratory probe (`evidence/inspect_same_clock.py`, output `evidence/same_clock_identity_probe.txt`) confirms those two receipts have **identical** root, branch, actor, start/end, `state_id`, `receipt_hash`, `episode_id` and `domain_issuance_id`; only the world event ID/kind differ. The test still refuses the substituted receipt and accepts the session's own receipt. Therefore the refusal is not an artifact of differing interval identities. The within-session conduct-binding path is exercised separately by the receiver revocation test (`test_real_current_cue_requires_issuer_parent_not_just_event_identity`), which passes.

The composite test group also covers: old authentic receipt after `WAIT`, old receipt with its unchanged interval, old event laundered through copied current interval fields, missing/forged/zeroed identity fields, widened caller interval, cold reopen/retry conservation, and later-operation supersession.

## 4. Actual first-consumer timing

Source path:

```text
run_p6.experience (run_p6.py:116-125)
  -> perform_outward (outward.py:37-87) commits world event + P6_HOUSE_CONDUCT
  -> PACE (run_p6.py:26-30) commits the S46 interval state
  -> reconsider (situated.py:339-474)
  -> current_p3_actor_access (situated.py:226-336)
run_p4.act (run_p4.py:248-326)
  -> pending saved before the conduct callback
  -> callback returns after reconsider
  -> outer turn appended and ledger saved after the callback
```

The owner state and conduct used by the check are already persisted when `reconsider` runs. The check never reads the outer turn being appended.

The reviewer's probe `test_first_consumer_checks_owner_interval_before_outer_turn_commit` proves this behavior in a real `run_p6.experience(..., sourcefree_p3_bridge=True)` call:

- Inside the interpret callback, `ledger["pending"]` is non-null and `ledger["turns"]` is still empty.
- The packet contains `actor_access_evidence` with basis `P6_OUTWARD_CURRENT_OPERATION_DERIVED`, grade `SOURCEFREE_TEST_ONLY`, disjoint world/P3 readsets and `stimulus_to_mediator_relevance == UNISSUED_NATIVE_RULE`.
- After return, the outer turn exists and its private `sourcefree_p3_receipt` exactly matches the packet's evidence/readsets.
- On reopen, the receipt's `state_id`, `receipt_hash`, `episode_id`, `domain_issuance_id`, root, branch and actor equal the latest `CURRENT` owner interval state; the unique conduct in that operation window matches the performed event; direct access is `True`.
- Cold reopen twice conserves the positive; a later `WAIT` supersedes it and the old receipt, including a widened interval, refuses.
- A current authentic receipt with a tampered `performed` body or forged sensory cue detail refuses without weakening the positive.

The probe needed two reviewer-side corrections before passing: the packet field is `readset` (the private receipt names it `p3_record_readset`), and `session.world()` returns a `WorldState` object rather than a mapping. Both corrections were to reviewer probe code only; the safety assertions were not weakened. All three runs are preserved in `evidence/`.

## 5. Native and authority holds retained

- `stimulus_to_mediator_relevance`: `UNISSUED_NATIVE_RULE` — present sensory contact does not establish relevance of a particular historic mediator.
- `native_memory`: `MISSING_RULE`; `native_action`: `NOT_ISSUED_BY_P3_RULE`.
- CAN-008 Rule A: `NOT_ISSUED`.
- CAN-011 Rule T: `NOT_ISSUED`.
- Memory/transfer/`NO_CHANGE`: `NOT_ISSUED`.
- Actor/human rights: `HELD`; production grant: `NOT_ISSUED`.
- No native psychology, scientific authority, protected integration or protected merge is claimed.
