# SOROK developmental recursion — focused repair-boundary review

**Subject:** `7c4907d0b5c42eaf0f6eb92a538516453a922933`
**Protected base:** `33c40a315d3c231cb2021bd8e60f3261547efa62`
**Branch:** `review/sorok-recursion-repair-boundaries-20261106-r1`
**Reviewer:** distinct focused repair-boundary reviewer, not the implementation author
**Mode:** local S2 sourcefree review; no production/native/human issuance

## Verdict

**`ENGINEERING_ACCEPT_SCOPED__REPAIRED_ACTOR_ACCESS_AND_PRE_EFFECT_BOUNDARIES_PASS_AT_7C__WHOLE_ENGINE_AND_NATIVE_HELD`**

The two required repairs execute and the focused negative boundaries reproduce cleanly at exact `7c`:

1. `P2Owner.actor_experience` uses the developing actor's action-hash binding and that actor alias's native perception rows, not the user's `public_opportunity` view.
2. `BatchEngine._check_new_batch` and `P2Owner.validate_proposal` reject bad chronology and explicit history grounding before any interval/operation effect; valid ID/hash forms and dynamic default history remain usable.

This is **not** acceptance of the unchanged whole engine, original historical V3, native psychology, independent B, or protected receiving. The separate full review of `41863919210021eced174ad5abdf49cb2df2042a` remains outside this scope.

## Exact inspected source

```text
developmental_recursion/p2_owner.py   sha256 1e22648822e99e245275b7f1160311a489b725169eba923578c8f1f588f710ba
developmental_recursion/engine.py     sha256 ba6caa74b2c57e567dbefa57571bc931bac8e4e5108bf844efe2966754ae9586
tests/test_engine.py                  sha256 e3478519a5b098162dd70d62c02ea69343448e56651922ba11fc75e50268b4ea
tests/test_p2_owner.py                sha256 1096fb62d4abf789e17b299a2f01daac19c2c029944365787dbe2c9ec95e7a85
tests/test_recursion_integration.py   sha256 7b6c32ec4fa2790d4c3b5c7211ee31aa9f59f61a59185587a066756274b64928
```

The reviewed code was read directly at `7c`; no source/test edits were made in this review.

## 1. Actor-access boundary

### Implementation observations

- `P2Owner.actor_experience(event, after_clock=...)`:
  - checks `event["actor_id"] == self.actor`;
  - resolves the actual action event by `event["action_event_id"]`;
  - requires `action["hash"] == event["action_event_hash"]`;
  - derives the store actor alias from `action["actor_id"]`, rejecting absent or user alias;
  - reads `store.perceptions(branch_id, actor_id=alias)`, filters the actor's own receipts in `(after_clock, action.clock]`;
  - requires the action event itself to be among those native receipts;
  - projects only the accepted `project_event` public surface and removes `perceived_by_user`;
  - returns `HELD` for absent actor/action/perception paths and `OBSERVED` only with actual receipts;
  - always returns `memory_formation = MISSING_RULE` (no native memory claim).

### Independent evidence

- `test_actual_material_effect_reaches_c9_and_owner_receipt_survives_reopen` passed: actual material interval reaches C9, `result.accessible["status"] == "OBSERVED"`, `actor_ref == owner.actor`, action event present, `perceived_by_user` absent.
- The same test severs the actor alias's perception list, observes `HELD` with `P2_ACTOR_PERCEPTION_UNAVAILABLE`, then restores the store and observes equality with the original `OBSERVED` receipt. This is the exact actor-perception severance/restore witness.
- Cold CLI receipt: `retrospective_uses_developing_actor_perceptions=true`; default output contains only event IDs and experience status, no `actor_ref`, `body_public`, or objective state.
- `MISSING_RULE` remains in the durable-transition field; no native memory formation was claimed.

## 2. Pre-effect chronology and native grounding

### Implementation observations

- `BatchEngine._check_new_batch` now rejects `event_time <= previous_clock` in caller order before `_claim_batch`/`_validate_all`/realization. It never sorts or rewrites proposals or historical journals.
- `P2Owner.validate_proposal` checks every explicit `history_refs` entry:
  - list/tuple schema and nonempty string;
  - actual native event ID or hash resolution;
  - duplicate removal by native event ID;
  - actor and branch equality;
  - native ordinal/clock strictly increasing;
  - history clock strictly before the proposed event time;
  - future event time and interval non-crossing check.
- `_validate_all` runs all owner proposal validations before the batch is claimed; a bad later proposal cannot commit the earlier interval.
- Empty `history_refs` retains the dynamic default realized-history path in `_realize`; native ID and hash forms remain accepted.

### Independent evidence

- `test_invalid_batch_chronology_is_refused_before_effects` passed for inverted `(3,1,4)`, equal `(1,1,2)`, and nonfuture `(0,1,2)` sequences. The owner snapshot was unchanged, `realize_calls=0`, `effect_count=0`, and the journal had zero batches.
- `test_bad_history_in_later_proposal_is_refused_before_first_interval` passed with actual P2 owner:
  - inverted and equal native times left interval states empty and operation rows zero;
  - missing, malformed, duplicate, and duplicate mixed ID/hash references were refused;
  - valid native IDs and valid native hashes were accepted;
  - owner snapshot unchanged and `engine.verify()` passed.
- Integration `test_two_real_batches_retrospection_and_cold_root` passed with actual material→C9, carry-forward, two-batch order, actor-bound retrospective input, terminal nonmutation and cold reopen.
- `test_material_antecedent_changes_later_native_c9_result` passed: ACTUAL material yields `[False, False, False]`; SCHEDULED_ONLY yields `[True, True, True]`.

## 3. Regression and cold CLI

Independent local execution at exact `7c`:

```text
tests/test_engine.py + tests/test_model_cycle.py
64 passed in 1.03s

tests/test_p2_owner.py + tests/test_recursion_integration.py
6 passed in 267.61s

combined focused/core suite
70 passed
```

Cold CLI `run_cold_cli_witness.py` passed:

```text
bootstrap / advance / finish
batch_event_counts = [3, 3, 0]
retrospective_count = 2
same_root = true
before_clock = 222
after_clock = 258
provider_calls_between_events = 0
cold_verified = true
retrospective_uses_developing_actor_perceptions = true
default_output_omits_actor_private_experience = true
native_psychological_transitions = MISSING_RULE
```

The model transport was the explicit local file fixture permitted as TEST_ONLY proof. No provider/model call, respondent read, or native participant action occurred.

## 4. Source and CI context

- Frozen architecture read: `fbfc529230d8b3c13f824cfac31741a5dfaa57e5:SOROK_PRODUCT_CONTROL_ROOM/USER_DIRECTED_ARCHITECTURE/20261026_USER_SETTLED_BATCH_RECURSION_IMPRESSION_MEMORY_R1.md`.
- Prior `b9f7f306` report is banked; it is **not** used as independent implementation proof.
- Existing proof contracts `77321a907` and receipts remain context, not acceptance of this repair.
- Remote Pyat later court: `3 failed, 144 passed`; the three failed nodes are inherited unchanged from protected base, with exact unchanged source blobs recorded in subject `evidence/receiving_ci.json`. This review does not re-pin or repair them; RED is preserved.
- No full review of `41863919210021eced174ad5abdf49cb2df2042a` is duplicated or accepted here.

## 5. Science and authority

- **Science:** HOLD; no native CAN/ADP memory, psychological propagation, independent B or human validity.
- **Authority:** HOLD; no protected CAS/native/Pyat/source/human grant, merge or production issuance.
- **Engineering:** scoped accept only for the two repaired boundaries and their actual regression/cold proofs.
- Raw final `MISSING_RULE` is preserved; it was not converted to evaluated NO_CHANGE or native psychology.

## 6. Remaining owner dependencies

1. Native CAN/ADP memory/psychological propagation and independently owned B remain unissued.
2. The original V3 source archive/dependency closure remains unavailable; no historical V3 reuse is accepted here.
3. The three inherited Pyat hash-pin CI failures remain owned by their existing authority; no unrelated repair.
4. Full engine review remains separate.

**No source/test changes, merge, new science, new source issuance or human validation.**
