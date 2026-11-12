# C02/C03/C04 Agent B ABI — periods, parent decision/action, utterance/uptake

**Status:** `SOURCEFREE_S2_ONLY`; parent-side C02/B02/C03/C04 mechanics. Full P3 batch interleave, B04 writer currency repair, B05 rent integration and native/science/authority remain held.
**B implementation:** `255fd4905990e3c0cab3e2d95ba91b851ea701a8`.
**Start composition:** `4724125721c646024bc2ef16b11510e4584991a8` (A `4528b68ad…` + Pair1 B02/B04/B05 `8de517bd…`, production `62292613…`).
**Contract:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`; protected baseline `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## C02 period context

`parent_activity._period_context(session)` uses the actual B02 incremental readers:

```text
historical_period.read_period_plan(session)
historical_period.period_progress(session, current_period_id)
historical_period.read_material_period(session, progress.current_date)
```

Requirements: the current S46 clock is inside a declared period; `logical_tick == session.clock()`; `material.period.period_id == period.period_id`. No manual anchor/ticks date inference and no full-plan `materialize_periods` call.

Qualified context carries:

```text
status = B02_PERIOD_CONTEXT_READ
period_qualification = B02_PERIOD_CONTEXT_READ
as_of_date, as_of_relation, logical_tick, period,
period_progress (BEFORE|PARTIAL|COMPLETE, clock/date/coverage/remaining),
calendar_basis, clock_basis, ticks_per_day,
interval_status, interval_status_detail, current_interval, current_interval_status,
plan_source, employment_source,
b02_employment_holder_actor_slot = "A",
b02_employment_applied_to_parent = false,
parent_employment_source = "PARENT_ACTOR_LOCAL",
full_dated_proof = B02_INCREMENTAL_PERIOD_API_QUALIFIED
```

`PARENT_B02_FULL_PROOF_HOLD` now means only a missing plan/unqualified context, not “API missing.” `PARENT_B02_HOLD` remains `B02_PERIOD_PLAN_ABSENT_ON_ROOT`.

`run_p4.PARENT_BACKGROUND_OPERATIONS` adds:

```text
period-materialize -> historical_period.materialize_to(session, as_of_date)
market-establish   -> material_operations.establish_market_inventory
parent-decide      -> parent_decision.admit_parent_decision
parent-perform     -> parent_decision.perform_parent_decision
parent-speak       -> parent_speech.perform_parent_utterance
```

All use the existing P4 foreground lock, source/boundary check, pending marker, owner API and `record_activity`; no arbitrary callback or new ledger.

## B04 purchase history acceptance

`parent_activity._parent_material_history` accepts exactly the B04 `P2_PARENT_PURCHASE` episode and no generic unknown kind. It validates:

- episode body/receipt schema, grade, root, branch, parent id/alias, status;
- before/after parent material sources are hashes; admitted purchase possession/effect fields and clock;
- ordered before/after source-chain continuity across antecedent/activity/circumstance/purchase;
- refused purchase has before == after and no possession;
- **admitted purchase currency must equal the current parent material currency**, else `PARENT_PURCHASE_CURRENCY_MISMATCH`.

`read_parent_history` includes typed purchase rows (`purchase_source`, object, owner, currency, period ref) and `purchase_episode_count`.

**B04 required writer ABI:** see `B04_CURRENCY_EXPECTED_ABI.md`. B04 must require parent/request/market currency equality before debit and must not declare equivalence. Until Pair1 B applies it, B04/B05 default tests fail; C03 refuses mismatch before B04.

## C03 decision/action

```text
parent_request_fixture(kind="junior"| "acoustic", owner_actor_id)
propose_parent_decision(session, parent_id, *, request, as_actor) -> PROPOSAL
admit_parent_decision(session, parent_id, *, operation_id, request,
                      as_actor, expected_clock=None) -> DECISION RECEIPT
perform_parent_decision(session, parent_id, *, decision_id, as_actor)
read_parent_decision(session, parent_id, decision_id, *, as_actor)
read_parent_action(session, parent_id, decision_id, *, as_actor)
```

Request is `SOROK_PARENT_REQUEST@1` with `request_id`, `objective_request` (exact B03 drum-kit request), `owner_actor_id`. It contains no child/Nadia outcome.

Explicit rule `SOROK_SOURCEFREE_PARENT_OBLIGATION_PURCHASE@1` (sourcefree hypothesis, `native_science=false`, `child_outcome=NOT_READ`, `nadia_state=NOT_READ`):

```text
PURCHASE when:
  parent/request/market currency equal;
  B03 material constraints other than REFUSED_AFFORDABILITY hold;
  actual market stock exists and kind/price match;
  owner is parent or focal household holder;
  parent cash >= price and free_hours >= 1;
  after purchase cash >= parent debt_units and free_hours >= care_hours_due;
  B02 current period qualified.
DECLINE for a refused material premise; HOLD for a missing/unknown premise.
```

Proposal is read-only and returns candidate action/status/reasons/unknowns, actual material source, period context, market/owned sources, B03 feasibility and obligation arithmetic.

`admit_parent_decision` writes one C12 `P2_PARENT_DECISION` (self-only proposal + admitted decision) with operation-id idempotence and stale replay when current material/market/period/B03 source changes. `perform_parent_decision` revalidates the decision source, then:

- PURCHASE → B04 `purchase_drum_kit` with `operation_id=<decision>:purchase`, owner from request; writes one C12 `P2_PARENT_ACTION` linking the purchase receipt; retry returns the stored receipt/REPLAY without a second debit.
- DECLINE → `VALID_EMPTY` action episode, no material/stock/ownership.
- HOLD → `HELD` action episode, no effect.
- B04 refusal → `REFUSED` action episode with the B04 receipt; no fabricated success.
- A later state that changes the proposal source makes perform `PARENT_DECISION_STALE`.

Normal P4 `parent-decide`/`parent-perform` route through this; `parent-decide` is a C12-only decision and does not change the world snapshot; a performed purchase changes the world and is recorded through `record_activity`.

## C04 utterance/uptake

```text
perform_parent_utterance(session, parent_id, *, decision_id, text,
                         hidden_reason, operation_id)
read_parent_utterance(session, parent_id, operation_id, *, as_actor)
read_child_uptake(session, child_actor_id, event_id)
```

The writer requires an admitted parent decision; validates nonempty text and a scalar-map hidden reason; commits one actual P2 `SPEECH` world event with body `{text, observable, utterance_source, decision_id}` and **no hidden reason**; records the parent `own_speech` perception; records the focal-child `speech` perception only when the child is co-present; stores hidden reason/hash in a separate self-only C12 `P2_PARENT_UTTERANCE`; checkpoints. Operation-id retry is idempotent.

`read_parent_utterance` (self-only) returns the public projected event and the hidden reason/hash to the parent. `read_child_uptake` requires the exact utterance episode, event hash/author, and the child's `speech` receipt; returns only the public speech projection with `hidden_reason=NOT_READ`. No child receipt → `NOT_PERCEIVED`; hidden/severed event → `CHILD_UPTAKE_EVENT_SEVERED`; co-presence alone is not a child percept. Normal P4 `parent-speak` records the actual event/boundary; P6 view and user say remain valid.

## Explicit limits

- Full C02 P3 `BatchEngine` 3–5 event cycle across periods; C03 consumes P2/B02/B04 mechanics, not a P3 actor decision cycle.
- B04 writer currency guard/default fixtures; B04/B05 default tests fail until Pair1 applies the expected ABI.
- B05 rent/household budget integration and shared currency/spending policy.
- E03 composite/crash/ownership exactly-once; no SIGKILL proof.
- Fork/cold parent lineage; C01 origin-branch registration refusal remains.
- P3 source closure does not pin `parent_activity.py`, `parent_decision.py`, `parent_speech.py`; no P3 edit or pin weakening.
- MI/P5/P6 `MATERIAL_ACTIVITY`/parent speech exposure; C04 does not alter P4 user speech or claim a user-visible parent utterance.
- C03 rule is an explicit sourcefree experimental hypothesis, not native/MIII mother science; no LLM backend or fixture-supplied decision.
- No native/source/actor/human/rights/protected authority; no independent acceptance.
