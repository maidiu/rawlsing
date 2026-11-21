# J1 exact blocker — missing terminal child-event performer

**Final status:** `J1_PARTIAL_EXACT_BLOCKER`.

## What is proven at the composed cut

The executable upstream J1 chain passes:

```text
B03 objective feasibility
  -> C03 parent decision
  -> C03 performed B04 purchase or valid-empty/hold
  -> C04 committed public SPEECH
  -> C12 child speech receipt
  -> normal P6 child current-experience (situated.recent_speech)
  -> D03 immediate uptake over prior P3 organization
  -> actual later P3 response streams under the same organization
```

Cold reopen preserves one purchase, one debit, one utterance and the unchanged P3 head. The J1 test also proves that tight space, noise, unknown acoustics, insufficient parent cash and currency mismatch bind the parent's act; that household rent changes only household funds; and that unperceived/tampered/severed speech cannot recruit D03.

## Exact missing seam

D03 does not select or perform a child action. Its own output says:

```text
immediate_response.native_action = NOT_ISSUED_BY_D03_RULE
immediate_response.streams[*].native_action_performed = false
durable_formation.status = MISSING_RULE
durable_formation.target_candidate = null
durable_formation.records = []
```

The composed J1 output therefore reports:

```text
subsequent_event.status = SUBSEQUENT_CHILD_EVENT_HELD_NO_COMPETENT_PERFORMER
subsequent_event.performed = false
subsequent_event.admitted_event = null
subsequent_event.eligible_modes_are_candidates_not_actions = true
subsequent_event.missing_owner = D04_TARGET_RULE_OR_D05_PERFORMED_CONSUMER
```

`WORKER_RETURNS/SOROK-DUEL-D03-R1/D03_D04_SEAM.md` requires D04 to add an explicit sourcefree target rule and an authorized P3 target writer/owner, and D05 to provide a distinct later performed consumer. The frozen task packets mark D04 and D05 `QUEUED_UNLAUNCHED`. No existing module, function or rule in this checkout consumes D03 `eligible_modes` into a chosen, admitted, performed child event.

## Reproduction

```sh
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py
```

Observed: `10 passed`. The terminal assertion is in `test_j1_full_chain_and_cold_reopen`; it reads the actual D03 output and asserts the held subsequent-event fields above. No test promotes an eligible mode to an act.

## Smallest owner-specific next action

Commission **one** bounded successor packet at a new exact head:

1. **D04 owner:** an explicit sourcefree target/recruiter rule and the smallest authorized existing-store writer, consuming D03 `speech_scope`, `prior_organization_scope`, `activation_context` and `immediate_response`; no new choice engine; explicit `NO_CHANGE`/`MISSING_RULE`/held outcomes.
2. **D05 owner:** one distinct later performed child event consumer that uses the D04-qualified target and actual access, with a severance negative proving the outcome changes when the target is removed.
3. Only if the product needs a single combined seam instead of D04+D05, name an explicit sourcefree child-event performer with its own source/authority; it must not relabel D03 modes as actions.

Until that owner exists, J1 remains a partial exact blocker. No downstream E02/J2, no automatic repair, no G5 and no protected merge follows from this return.
