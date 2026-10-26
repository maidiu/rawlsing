# SOROK S52 — qualified paid opportunity as a real actor alternative

**RESULT:** `S52_PAID_ACTIVITY_REPERTOIRE__ACTUAL_G18_CONTRACT_SOURCE__CURRENT_STATE_CONDITIONAL_PAID_CANDIDATE__S39_OPEN_WITH_OPTION_AND_REASON__CONTROLLED_PORT_EFFECTS__NATIVE_PURPOSE_AND_INDEPENDENT_COUNTERPART_STILL_MISSING`.

S52 is built on accepted S51 `2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65` and accepted S49 `6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43`. It adds the separately missing repertoire connection without fabricating a counterpart, a generated B attempt, a native motive, or a new psychological choice rule.

## Recovered contract and new callable function

- The actual G18 source is `lab_sgi1/joint.py`; `material_joint_opportunity` supplies the bounded owner-qualified schedule, `verify_material_source` authenticates its fixture receipt, and G18's participation arithmetic is `cash += payment_per_actor`, `free_hours -= task_hours`, `completed_units += material_units`.
- G18 `perform_participation(events, material)` replays old event history and therefore is not used as a current-B execution. S52 exposes `S52Session.perform_paid_participation(candidate, generation, counterpart_performed=...)`, a current-state port at `TEST_ONLY_S52_PAID_ACTIVITY_PORT_NOT_NATIVE` scope. It rechecks position, permit, task time, material, current actor state, generation/candidate identity and duplicate execution. It does not borrow a G18 action receipt or claim unilateral wages.
- The normal path is conditional: the contract requires an independent counterpart contribution, which the current journal does not establish. `counterpart_performed=True` is a controlled port test only.

## Normal consumer change

- S52 resolves the same accepted S51 object, consumed one-event hypothesis, actual world offer, B access and recomputed relevance from the same actor/root/branch/journal.
- It compiles a typed `PAID_PARTICIPATION` candidate/plan with exact offer, actor, participant role, task parameters, prospective payment, time/material/capability readset, counterpart prerequisite, source/rule references, and status `CONDITIONAL_ON_INDEPENDENT_PARTICIPATION` (or `BLOCKED`/`UNKNOWN`/`NOT_RECRUITED`).
- The existing S39 generation path is extended by a scoped repertoire parameter. The actual receipt contains the new option and a `CONDITIONAL_SUPPORTS` reason bound to the canonical S51 source and candidate hash. S39 `FULL_RULE` content is unchanged; no REPAIR_URGENT/PREFER_INDEPENDENT/PRIOR_B_REFUSAL relation was added and no new option has a comparison, weight, rank or default.
- The result remains `OPEN_CHOICE_SET` with no selected option or performer in the normal path. Source cut removes the paid option/reason; restoring the same source restores them. Inaccessible and obstructing offers do not add a positive paid reason; blocked/unknown current states are not recruited.

## Controlled versus generated effects

- **Generated:** only the candidate and conditional reason; no paid action, no C8, no B world event, no earned money. `earned_payment` remains `0`, prospective payment `2`.
- **Controlled denial:** without an independent counterpart the performer returns `CONDITIONAL_ON_INDEPENDENT_PARTICIPATION` with no actor/world effect.
- **Controlled performance:** with the explicit test-only counterpart flag, the current-state port records a real BP4 `REPAIR` event and `S52_PAID_ACTIVITY_RESULT`; B moved from cash 54/free 11/completed 5 to cash 56/free 10/completed 6 for payment 2/task 1/material 1. Duplicate denial is keyed to the canonical paid contract target/offer event, not a caller-mutable candidate hash. A forged cross-actor candidate is denied, and mutating the current B checkpoint away from the lawful result is detected by verification.
- This is not evidence that B chose the action, that A participated, or that payment was earned in the normal path.

## Evidence

- Focused S52 tests: **11 passed**, 0 failed/error/skipped; `junit/s52_full.xml`, `logs/s52_full.log`, `evidence/test_run.json`.
- Entrypoint: `run_s52.py` exits **0**; `evidence/entrypoint.json`, `logs/entrypoint.log`. The normal paid option/reason stays OPEN with no action; controlled denial and controlled effect remain distinct; cold replay verifies.
- Changed seams: S39 model (scoped repertoire option/reason, FULL_RULE unchanged), S49 `generate_b`/`produce_b_turn` optional repertoire forwarding, S51 `consume_generation` optional repertoire forwarding. Source manifest `evidence/source_manifest.json` records these and the accepted base cuts.
- Existing focused suites remained green after the seam changes: S39 **10**, S49 **13**, S51 **13**.
- Review53 oracle is captured at `logs/review53_probe_after.json`: raw repertoire is refused (`S52_CANONICAL_CANDIDATE_MISSING`), forged cross-actor performance is denied with one performed action, current-state divergence is rejected, and source cut/restore distinguishes actual source removal from repertoire omission.
- No provider call, package install, new agent, native A/T/source/Pyat/human/SCI05 grant, second psyche, or S50 runtime use.

## Remaining real gaps

The normal paid alternative is conditional because no actual independent counterpart contribution/willingness is observed. The current actor state supplies a capability readset (`completed_units`, practices, time/material), but no paid-history-specific source establishes paid capability; that remains a disclosed limitation rather than a role-title inference. There is still no actual current actor-owned purpose, no native object-formation/relevance law, no generated selected attempt/choice, and no native C8 permission. The controlled port demonstrates only the mechanical contract and denial/effect arithmetic at current state.

Untracked S50 runtime was left untouched and uncommitted.

**Terminal:** `S52_PAID_ACTIVITY_REPERTOIRE__REAL_CONTRACT_CONDITIONAL_OPTION__CONTROLLED_PORT_ONLY__NO_INDEPENDENT_COUNTERPART__OPEN_NO_WINNER__FULL_PURPOSE_CHOICE_NOT_DONE`.
