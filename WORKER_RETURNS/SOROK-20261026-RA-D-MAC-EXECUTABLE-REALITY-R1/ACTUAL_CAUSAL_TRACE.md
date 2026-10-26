# RA-D actual same-person causal trace

**Grade:** `TEST_ONLY_SOURCEFREE_S52_CUT_NOT_NATIVE`. No provider call, raw data, accepted-source edit or native grant.

## 1. Execution identity

- S52 cut: `c821b488b3a9a3f0fa01b1981989cc17af637dc1`
- Imported S39 `model.py`: `6afba4b77b71c40654986fed4eda40915c7a0cc454e07d8293e353f135f1c603` (the S52-cut modified blob, not accepted `41fe95c1…`)
- G18 `history.py`: `2d861d7a820168d443e23efb2403b7ed9c3e899a8a79aaa72fd859c46f47c1c1`
- JOIN-E `joined/session.py`: `ea820ec3e30a2825c3d0d8c5dc66e812afdda40b08f9cc0a8c868c8b3e0dd0da`
- Language mediation `session.py`: `d6a1628cbfdc1c601f68fb3d3b9adbe91f9464875996b543caf69e548ece25aa`
- Actor B: `TEST_ONLY_BP1_R26V_ACTOR_B`; Actor A: `TEST_ONLY_BP1_R26V_ACTOR_A`
- Root: `84687e6f…` (S44 sampled antecedent root; current B state is the sampled root state, not the G18 replay final state)
- Historical G18 B history: 21 events; `replay_history` valid; no errors.

## 2. Historical state and object

`S44Session.start` calls `generate_root` (`s44/root.py:96–282`), which:

1. draws A/B material, cash, hours, birth and joint parameters from the fixed bundle;
2. calls `build_actor_history` for both actors;
3. creates the joint material opportunity and objective event;
4. appends shared objective/performed/other-action/relation-view events to the A/B ledgers;
5. freezes `g18_history_refs`, `g18_history_hashes`, snapshot hashes and the root hash.

The G18 replay produces the historical B state:

- `skill=6`, `free_hours=15` before the later route/commission events; final historical state `cash=53`, `free_hours=13`, `completed_units=3`, `material_remaining=1`, `practices=["scheduled_finishing_ledger_discipline"]`, `attitudes=["reciprocity_in_work_obligations"]`.
- Unique `STRIVING` event: `sha256:198b568bc0747c50829b68866009a5c5627cef7dbc4b036cfcc03848386a2c60`, value `fund_finishing_equipment`.
- Causal parents: `WORK_POSITION` `sha256:4de01226…` and `PROJECT` `sha256:bc48470f…`.
- A `value_witness` records the readset and effect (`striving=fund_finishing_equipment`, budget from the work/project values).
- `ROUTE_AVAILABILITY` events have effects whose `goal` equals the striving; these are the route-usage witnesses.

`s51/session.py:108–135 recover_object` reads that history, validates replay, requires exactly one admitted STRIVING, requires the two parents, requires a value witness and route usage, and returns the object with `source_grade=SOURCEFREE_RESEARCH_INPUT`, `native:false`, `native_purpose_proof:false`.

**What this proves:** the historical object is a real, replay-validated G18 object with causal parents, not a hash-only label.

**What it does not prove:** that the object is a current actor-owned purpose.

## 3. Current event, access and relevance

The S52 probe used the explicit S51 flow:

1. `recover_object()` → object `sha256:198b568b…`.
2. `declare_hypothesis(obj)` (`s51/session.py:146–165`) appends `S51_RETAINED_OBJECT_HYPOTHESIS` with:
   - `scope="ONE_SUBSEQUENT_RECEIVED_EVENT"`;
   - `status="DECLARED_IMMUTABLE"`;
   - `actual_current_purpose_proved:false`;
   - `psychology_claim:false`, `actor_testimony:false`, `native:false`.
3. `issue_offer()` (`s51/session.py:224–243`) creates a world offer from `material_joint_opportunity`:
   - `payment_per_actor=2`, `task_hours=1`, `material_units=1`, `permit=true`, `place=INST_WORKSHOP_A`;
   - the world event is written, B perceives it, and the offer episode records the world event/hash.
4. `_offer_access(offer)` (`s51/session.py:269–281`) finds B's perception of that exact world event and creates an actor-local access witness:
   - `access_status=ACCESSIBLE`;
   - `source_ref=S51_ACCESS_…`;
   - content binds `received_offer_event_id`, `received_world_event_hash`, perception clock and channel.
5. `evaluate(obj, hyp, offer, access)` (`s51/session.py:309–359`) calls `_relation_for(offer, access, actor_free_hours)`.

The actual current B state at this point is:

- `cash=54`, `free_hours=11`, `completed_units=5`, `material_remaining=1`, `skill=6`, `practices=["scheduled_finishing_ledger_discipline"]`, `attitudes=["reciprocity_in_work_obligations"]`, `place=INST_WORKSHOP_A`.

`_relation_for` (`s51/session.py:361–375`) is:

```python
def _relation_for(self, offer, access, actor_free_hours):
    p = offer.get("offer") or {}
    if access is None or access.get("access_status") != "ACCESSIBLE":
        return "NOT_RECEIVED", "NOT_RECEIVED"
    if p.get("permit") is not True:
        return "OBSTRUCTS", "RELEVANCE_WARRANTED"
    if not isinstance(actor_free_hours, int):
        return "UNKNOWN", "RELEVANCE_WARRANTED"
    if p.get("payment_per_actor") is None or p.get("task_hours") is None:
        return "UNKNOWN", "RELEVANCE_WARRANTED"
    if int(p.get("payment_per_actor", 0)) <= 0:
        return "OBSTRUCTS", "RELEVANCE_WARRANTED"
    if int(p.get("task_hours", 0)) > int(actor_free_hours):
        return "OBSTRUCTS", "RELEVANCE_WARRANTED"
    return "FACILITATES", "RELEVANCE_WARRANTED"
```

It does **not** read `obj` or the hypothesis's object semantics. With `access=ACCESSIBLE`, `permit=true`, `payment=2`, `task_hours=1`, `free_hours=11`, it returns:

- `status=RELEVANCE_WARRANTED`
- `relation=FACILITATES`
- `actor_free_hours=11`
- `actual_current_purpose_proved=false`

The object identity is copied into the relevance episode/source content, but the relation is a function of the **current offer + current free hours**, not the historical `striving` value. A different canonical historical object with the same current offer/free hours would produce the same relation. The code rejects non-canonical/different-striving objects before evaluation (`recover_object` requires `fund_finishing_equipment`), so no lawful object-value contrast is implementable on this path.

## 4. Option generation and the actual stop

The standalone S51 entrypoint (`run_s51.py`) confirms the narrower fact without the S52 repertoire: it recovers the same G18 object, declares the same one-event hypothesis, computes `RELEVANCE_WARRANTED/FACILITATES` from `free_hours=11`, and then S49 returns `SOURCE_OWNER_HOLD` with `selection_status=OPEN_CHOICE_SET`, `selected_option=""`, `reasons=[]` because no existing S49 option expresses the paid finishing-equipment offer. The cold replay preserves the same relevance hash and verify true. S52's modified S39/S49/S51 plumbing later adds the conditional paid option; it still does not select it.

`consume_generation` (`s51/session.py:426–464`) creates a validated `make_source` with:

- `source_class=HISTORICAL_EPISODE`,
- `predicate=S51_OBJECT_RELEVANCE`,
- `value=1`,
- content containing `object_event_id`, `offer_event_id`, `relation`, `hypothesis_id`, `relevance_hash`, `access_ref`,
- `model_premise:true`, `native:false`, `psychology_claim:false`.

S52 `compile_candidate` (`s52/session.py:137–223`) reads:

- `offer.permit`, `offer.place`, `task_hours`, `material_units`, `payment_per_actor`;
- current actor `free_hours`, `material_remaining`, `completed_units`, `skill`, `practices`, `material_position`, `position`;
- `relevance.status` and `relation`.

It **does not read the object's `striving` value** to decide status. It copies `object_event_id` into source/reason content. With the observed current state and `FACILITATES`:

- `status=CONDITIONAL_ON_INDEPENDENT_PARTICIPATION`
- `reason=S52_INDEPENDENT_COUNTERPART_NOT_OBSERVED`
- `recruited=true`, `performed=false`, `earned_payment=0`, `prospective_payment=2`
- `capability_readset.grade=CURRENT_ACTOR_STATE_ONLY_NOT_PAID_HISTORY`

`consume_generation` then passes the repertoire to S49 `produce_b_turn` → `generate_b` → S39 `generate_choice`.

### S39 receipt

The S52-cut `s39/model.py:169–427` receives only the S51 source. It has no `REPAIR_URGENT`, `AVOID_DEBT`, `PREFER_INDEPENDENT`, `PRIOR_B_SHARE` or `PRIOR_B_REFUSAL` records, so no four-option comparison rule's `all_of` is satisfied. The receipt is:

- `options`: `ATTEND_OBJECT`, `REQUEST_TOOL`, `EXPLICIT_REFUSAL`, `PAID_PARTICIPATION`
- `eligible_options`: all four
- `defeated_pairs`: `[]`
- `undominated_options`: all four
- `selection_status=OPEN_CHOICE_SET`
- `unresolved_reason=MULTIPLE_SURVIVORS`
- `selected_option=""`, `attempt_request=null`
- paid reason: `CONDITIONAL_SUPPORTS`, predicate `S52_PAID_OBJECT_RELEVANCE`, source class `HISTORICAL_EPISODE`

The paid option is appended by the S52-cut repertoire plumbing, but **no comparison rule names it**. Even the three base options have no comparison because the S51 source is the only source. Therefore there is no actor-selected action. The "choice" is an open set.

### Source-cut controls

| Control | Eligible options | Paid present? |
|---|---|---|
| No source records | `ATTEND_OBJECT`, `REQUEST_TOOL`, `EXPLICIT_REFUSAL` | no |
| S51 source only, no repertoire | `ATTEND_OBJECT`, `REQUEST_TOOL`, `EXPLICIT_REFUSAL` | no |
| S51 source + canonical repertoire | `ATTEND_OBJECT`, `REQUEST_TOOL`, `EXPLICIT_REFUSAL`, `PAID_PARTICIPATION` | yes |

This is a real conditional-option consumer edge. It is not a motivation or selection edge.

## 5. Controlled state change and later material consumer

`perform_paid_participation(counterpart_performed=False)` returns `DENIED/ CONDITIONAL_ON_INDEPENDENT_PARTICIPATION` with no state change. `counterpart_performed=True` is an explicit **test-only** controlled port (`s52/performer.py:30–113`):

- Before: `cash=54`, `free_hours=11`, `completed_units=5`.
- After: `cash=56`, `free_hours=10`, `completed_units=6`.
- Appends a `REPAIR` world event for B and a `S52_PAID_ACTIVITY_RESULT` episode.
- The result is `status=PERFORMED`, `controlled_counterpart=true`, `counterpart_status=EXPLICIT_CONTROLLED_TEST_ONLY`.

This is not an independent actor's participation and not an actor-chosen option. It is a port contract test.

Repeating lawful controlled tasks through `run_experiment()` drives `free_hours` from 11 to 0. The next S52 experiment then:

- computes `relation=OBSTRUCTS` because `task_hours=1 > free_hours=0`;
- compiles `status=BLOCKED`, `reason=S52_INSUFFICIENT_FREE_HOURS`, `recruited=false`;
- S39 `eligible_options` no longer contains `PAID_PARTICIPATION`;
- `verify()` remains true.

**This is the deepest actual same-person later-event consumer:** a changed B material capability value changes a later typed option eligibility. It is objective/material, not psychological.

## 6. What the A-actor/CAN008–CAN011 path actually does

The S44/S45 path uses the vendored M35 producer and S36/S37/C9. The M35 test-only resources are:

- `TEST_ONLY_BP2_CAN008_RULE_A` with `TEST_ONLY_BP2_CAN008_RULE_A_ISSUER`;
- `TEST_ONLY_BP2_CAN011_RULE_T` with `TEST_ONLY_BP2_CAN011_TARGET_OWNER`;
- a separate `TEST_ONLY_BP2_CAN011_TARGET_GRANT`.

The S44 entrypoint executed a first event with `selected_option=REQUEST_TOOL`, the S45 entrypoint executed `say/do_help/attend`, and the C9 target branch was `NO_CHANGE` with reason `NO_PROPOSAL` and `target_proposals:[]`. This is a **test-only** CAN008/CAN011 receiving/commit path with no target creation. It is not a native CAN011 rule and it is not the B paid-activity path. It does not create a durable psychological mediator.

The S52 B path does not use the M35 CAN008/CAN011 ports at all; it uses S39/S49 finite option generation and the S52 conditional candidate.

## 7. First exact stoppage

From the actual executed chain:

`G18 history → historical STRIVING object` **executes**.
`historical object → one-event hypothesis` **executes as a declared TEST_ONLY premise**.
`hypothesis → current relevance` **executes, but reads current offer/free hours, not object semantics**.
`relevance → paid option` **executes as a conditional option**.
`paid option → actor-selected action` **does not execute: OPEN_CHOICE_SET**.
`actor action → actor-owned psychological state change` **does not execute**.
`state change → later psychological response` **does not execute**.

The first psychological edge is therefore not a rendering or transport problem. It is:

> **actual historical actor state + received encounter + attempted/assisted discrimination and feedback → a current, actor-owned, scoped interpretive/practical operation (or explicit NO_CHANGE) under a competent formation/retrieval rule, admitted with causal parents and memory/epistemic ownership, then read semantically by a later same-person event.**

The first **software** missing piece is the composer/admission that emits that operation (CAN011 CREATE/TRANSFORM/NO_CHANGE) and the actor-state consumer that admits it. The first **science** missing piece is the concrete CAN008/CAN011 formation/persistence/retrieval criterion. The first **actor-input** missing piece is an independently performed counterpart/feedback rather than the controlled boolean. The first **unwired historical** source is S50 V3/PFF (fixture-only; actual root missing). The first **integrity** defect is the S52 verifier postcondition skip.

## 8. S52 verifier defect

`S52Session.verify()` (`s52/session.py:299–311`) only compares current B cash/free_hours/completed_units with the last performed paid result when that result is the last canonical episode. The independent probe:

1. performed controlled paid action (cash 56);
2. appended `S52_UNRELATED_TEST_NOTE` (no B transition);
3. set B cash 999 and checkpointed;
4. warm `verify()` → `ok=true`, `s52.errors=[]`;
5. cold reopen `verify()` → `ok=true`, `s52.errors=[]`.

Control without the unrelated note → `ok=false`, error `S52_CURRENT_STATE_DIVERGES:cash`. This is a concrete integrity regression in an unaccepted component. It does not create psychology and does not explain the first unproven edge.

## 9. Conclusion

The actual engine currently computes and connects **historical identity, historical object presence, objective current material eligibility, a conditional option, and material state carry-forward**. It does not yet compute or connect **actor-owned psychological formation, actor-owned selection, CAN011 durable change, or later psychological consumption**. The deepest trace is real but narrower than the Astra/developmental claim; it must be reported at that grain, not promoted by analogy.
