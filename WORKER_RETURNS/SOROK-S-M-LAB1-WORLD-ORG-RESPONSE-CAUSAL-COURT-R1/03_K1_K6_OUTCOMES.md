# 03 — K1–K6 executed outcomes (machine-first)

Preregistration: `02_FROZEN_PREREGISTRATION.json` (sha256 `f36d2d31289a6f1544444193689778e352e2e903162f63a578185868e89f4981`). Run set: `outputs/primary_results.json`; every receipt: `outputs/runs/<K>__<contrast>__<arm>__<seed>.json` (576 files). Run order executed: K1, K3, K5 → integrity gate `phase1_integrity: True` → K2, K4, K6.

## K1 — same world, different admitted developmental histories

- World: `W_PORT_TOWN_1998_TEST` (hash `W_SYNTH_001`), same position `POS_SYNTH_01`, same relationship `REL_SUP_APP`, same opportunity `OPP_FEEDBACK_WINDOW`, same present occurrence `EV21_FEEDBACK_REQUEST_ENCOUNTER`.
- Contrast: `H_RESPONSIVE` (EV7_FEEDBACK_RESPECTED + EV13_FEEDBACK_COLLABORATIVE → CAN010 `SCOPE_HELP_POSSIBLE`, CAN011 `ASK_CLARIFICATION` practice, CAN010 `VERIFY_TOGETHER` striving) vs `H_PUNITIVE` (EV7_QUESTION_PUNISHED + EV13_REQUEST_SANCTIONED → CAN010 `SCOPE_SPEAKING_COSTLY`, CAN011 `APPROACH_WITHDRAW` tension, ADP016 nondeclarative trace).
- Machine result (all 12 seeds × 3 arms): `H_RESPONSIVE`→`REQUEST_FEEDBACK` (recruited by practice+expectation+striving; parents EV7_FEEDBACK_RESPECTED/EV13_FEEDBACK_COLLABORATIVE); `H_PUNITIVE`→`SILENCE` (recruited by expectation+tension; `REQUEST_FEEDBACK` route-gate refused for lack of practice/help expectation). Causal parent receipts differ; identical-history replay identical.
- Kill checks: category/profile-driven response without owner ancestry — absent (selection always references parent events); paraphrase-driven machine mutation — absent (`K1_ADJECTIVE_ONLY_CHANGE` null).
- Negative controls run: identical history replay (pass), adjective-only change (pass), noise event (pass).

## K2 — same nodes, different admitted temporal relational topology

- Same nodes `EV1_APPROVAL`, `EV2_CRITICISM` and same present `EV3_REQUEST`; distinct admitted formation ancestry: `EV_RELFORM_A` (content `COMPENSATION_READING_FORMED`, parents EV1→EV2) vs `EV_RELFORM_B` (`CONDITIONAL_RECOGNITION_READING_FORMED`).
- Machine result: relation views formed correctly in all arms (`COMPENSATES_FOR` / `CONDITIONS_RECOGNITION` with exact formation refs; A source `RECONSTRUCTED_FROM_ADMITTED_ANCESTRY`, C source `C_TYPED_RELATION_INDEX`). A routes correctly (`REQUEST_WITH_REPAIR` / `REQUEST_WITH_CONDITIONAL_CAUTION`) = 1.0. B and C route both topologies to `REQUEST_WITH_REPAIR` = 0.0 (diagnosis below).
- **Diagnosis (retained in `outputs/liveness_controls.json`):** the frozen B/C score adds `+goal_match`; `SCOPE_APPROVAL_CONDITIONAL` matches `REQUEST_WITH_REPAIR` in both topologies, tying it with the relation-supported `REQUEST_WITH_CONDITIONAL_CAUTION` at score 2 in `T_CONDITION`; the frozen B/C tie-break prefers goal-match and picks `REQUEST_WITH_REPAIR`, collapsing the distinction A preserves. This is an outcome of the preregistered B mechanism, not a scoring change (frozen scoring untouched).
- Cache test: `a_reconstruction_equivalent_to_c_edge: True`; `c_unique_gain_over_a: False`; C scans 0 formation events vs A 1.88. → C earns **DERIVED_CACHE** only.
- Negative controls run: free-edge mutation refused (`K2_FREE_EDGE_MUTATION`), event-order shuffle (pass, elsewhere).

## K3 — inaccessible early residue, wrong/absent self-explanation

- `TRACE_ACTIVE` (EV7_PUBLIC_SHAMING → ADP016 nondeclarative trace `RETAINED_NOT_ACCESSIBLE`, episodic `UNAVAILABLE`, ADP017 origin claim DENIED) vs `TRACE_ABSENT` (EV7_NEUTRAL_COUNTERFACT, no trace) vs `RETAINED_INACCESSIBLE`.
- Machine result: `TRACE_ACTIVE`/`RETAINED_INACCESSIBLE` → `HEIGHTENED_GUARD` with trace support keyed to `TRACE_PUBLIC_SHAMING`; `TRACE_ABSENT` → `NEUTRAL_RESPONSE` with zero trace support. Actor-safe projection grants **no recall** and exposes only `NON_DISCLOSABLE_ORIGIN` markers; the seven-year-old origin never appears in actor-visible content.
- Hidden-origin injection into evaluator-only metadata: actor-safe payload byte-identical in 6/6 arm×contrast runs.
- Kill checks: actor reciting origin without recall grant — impossible by construction (projection never carries origin); ledger copied to actor context — absent.

## K4 — corrective recurrence without obligatory healing

- Prior `EV7_QUESTION_PUNISHED` (identical hash in all contrasts); later admitted event varies: peer-respected (relationship `REL_PEER_APP`), supervisor-punished (same authority), unrelated kindness.
- Machine result: `CORRECTIVE_CONTEXT` → TENSION_REVISED `APPROACH_WITHDRAW` status `NARROWED` scope `FEEDBACK_SUPERVISOR_ONLY` (parents EV7 + EV17_PEER) and route `NARROWED_CONSULT`; `RECURRENCE_SAME_AUTHORITY` → status `REINFORCED` and route `REPEATED_QUESTION`; `WEAK_COUNTEREXAMPLE` → `NO_CHANGE` and route `NO_ACTION`. Prior event hashes unchanged in every receipt (`NO_REWRITE_PRIOR_EVENTS`).
- Kill checks: fixed global wound-counter — absent (no scalar exists; status changes only with exact new parent); forced recovery/revelation — absent.
- Negative control: paraphrase-only "revision" refused (`K4_PARAPHRASE_ONLY_NO_REVISION`, one-parent revision → `NO_REWRITE_PRIOR_EVENTS`).

## K5 — recognition / social reality conflict

- Same actor history `EV_PRIVATE_SELF_DOUBT` (ADP017 belief `BELIEF_OWN_WORK_UNCERTAIN`, actor-testimony warrant); witness event varies: registrar (kind `INSTITUTIONAL_RATIFICATION`, power `CAN_RATIFY`), supervisor (`CAN_SIGN_SHIFT_NOT_RATIFY`), peer (`NONE`).
- Machine result: `objective_public_standing_effects` nonempty **only** for registrar (WORLD_PUBLIC_RECORD `CERTIFIED`); supervisor/peer arms leave standing unchanged (`NO_OBJECTIVE_PUBLIC_STANDING_FROM_UNEMPOWERED_WITNESS` gate would refuse any attempt — exercised in nulls). `BELIEF_OWN_WORK_UNCERTAIN` is byte-identical across all three arms ("belief not automatic"). `ACCEPT_CERTIFICATE` route is permitted only when standing is certified. Supervisor praise produces only an actor-side reception record; peer praise produces none (no forced uptake).
- Private resistance/mistaken belief: recorded as ADP017 testimony, never adjudicated as truth.
- Negative controls: powerless witness (pass), official-sounding badge utterance (`K5_OFFICIAL_SOUNDING_UTTERANCE`).

## K6 — internalization → outward discipline

- Later world/position: `W_PORT_TOWN_1999_POSITION_VARIANT` at `1999-06-10T10:00:00Z`; capacity bound via position receipt (`POS_SYNTH_02F` `VALID_SMALL_SCHEDULE_POWER` / `POS_SYNTH_02A` `NONE` / `POS_SYNTH_02C` category-only).
- Machine result: `POLICING_CANDIDATE` permitted only in `PRACTICE_AND_CAPACITY` (practice `PROCEDURE_ENFORCEMENT` earned + valid capacity + admitted route); the action effect is recorded `CANDIDATE_NOT_MANDATORY` (`selected_not_mandatory: True`) — never inevitable. `PRACTICE_NO_CAPACITY` and `CATEGORY_ONLY` produce `NO_SANCTION` with zero action effects (`NO_CATEGORY_TO_BEHAVIOR_DIRECT_EDGE`, `NO_SANCTION_ROUTE_OR_CAPACITY` gate codes on candidates).
- Kill checks: demographic/category→behavior direct edge — absent; event-local wish creating capacity — absent (capacity comes only from the dated position receipt).

## Integrity summary

`hard_invariants_pass: True` — zero unadmitted-event commits, zero hidden-origin leaks, zero category-only sanctions, zero public-standing changes from unempowered witnesses, zero prior rewrites, zero unauthorized C edges, zero worldless commits, `REPLAY_SAME_SEED_SAME_STATE` (576/576).
