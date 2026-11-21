# E01/J1 composed ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; upstream chain proven, terminal child act held.
**Module:** `WORKER_RETURNS/SOROK-E01-J1-995-R1/j1_join.py`.
**Inputs:** actual P3 `owner`, actual P2/P3 `session`, focal child id, committed speech event id, actual C04 writer receipt, exact P3 plan, optional expected identity/closure/speaker.

## Output

```text
SOROK_E01_J1_THREE_HEAD_JOIN@1
status = UPSTREAM_CAUSAL_CHAIN_PROVEN_SUBSEQUENT_EVENT_HELD
       | HELD_NOT_PERCEIVED
grade = SOURCEFREE_S2_ONLY

child_experience:
  normal P6 child_speech_experience
  p6_experience_source = situated.recent_speech
  public event/text/speaker/occurrence/read clocks
  response_input = SOROK_CHILD_SPEECH_RESPONSE_INPUT@1
  hidden_reason = NOT_READ; durable_acquisition = MISSING_RULE

immediate_uptake:
  D03 SOROK_D03_IMMEDIATE_UPTAKE@1
  speech_scope public only
  prior_organization_scope = sourcefree P3 plan scope, not parent identity
  immediate_response = existing P3 test-only activation/rule
  native_action_performed = false on every stream
  durable_formation.status = MISSING_RULE
  store_head.before == store_head.after

parent_decision:
  parent self-read decision/action evidence
  action status, physical_admission, performed/valid_empty
  objective B03 feasibility status/reasons/unknowns
  child_request = NOT_EVALUATED; nadia_state = NOT_READ

subsequent_event:
  status = SUBSEQUENT_CHILD_EVENT_HELD_NO_COMPETENT_PERFORMER
  performed = false
  admitted_event = null
  eligible_modes_are_candidates_not_actions = true
  missing_owner = D04_TARGET_RULE_OR_D05_PERFORMED_CONSUMER
  durable_formation = MISSING_RULE
```

## Refusals

- changed J1 closure hash → `J1_SOURCE_CLOSURE_CHANGED`
- altered/mismatched C04 receipt identity/hash/text/actor → `J1_UTTERANCE_*` or D03 `D03_*` refusal
- severed speech event → `CHILD_UPTAKE_EVENT_SEVERED`
- unperceived child → held output, no text/event/modes, parent decision not child-facing
- private parent receipt → `D03_PRIVATE_INPUT`
- D03 store mutation → `D03_STORE_MUTATED`
- D03 eligible modes are never converted to an action by this module

## Explicit non-claims

No choice engine, no D04 target writer, no D05 performer, no durable child memory, no native CAN/ADP/PYAT rule, no language-generation owner, no actor/human/science acceptance, no protected merge.
