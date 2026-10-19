# 02 — Candidate transaction path (T1)

**Status:** `EXECUTED_GREEN__TEST_ONLY_SOURCEFREE_TECHNICAL__NONINSTALLING`. One complete fail-closed candidate transaction/consumer path implements all eight commissioned stages. The path is noninstalling: it writes only to its own SQLite store and never to production state.

## Path architecture (a) through (h)

```
(a) actor identity/currentness/standing-state ingress
    candidate/identity.py :: ingress_actor
    Fail-closed on: missing id, inactive, stale standing state, psychology claim, unsealed record.
        ↓
(b) ADP010/019 precipitating event witness
    candidate/events.py :: ingress_event
    Typed missing witnesses: MISSING_ADP019_OWNER_RECEIPT, MISSING_ADP010_ENCOUNTER_RECEIPT.
    Never fabricates an occurrence from an offer, label or narrative.
        ↓
(c) received person/world READ-ONLY conditioning
    candidate/conditioning.py :: bind_conditioning
    Native zero-positive guard consulted per source class; DENY_ZERO_EFFECT preserved.
    Forbidden conversions refused: structural→trait, observer→belief, demographic→propensity,
    source_text→affect, world_fact→actor_knowledge, other_private_motive→actor_state.
        ↓
(d) CAN008 response-rule registry lookup/refusal
    candidate/response_rules.py :: lookup_rule + evaluate_response
    Production registry EMPTY → RULE_ABSENT → REFUSED.
    Unverified issuer → RULE_ISSUER_UNVERIFIED → HELD.
    Found + insufficient history → RESPONSE_EFFECTS_VALID_EMPTY.
    Found + full inputs → exactly one V3MS_PRACTICE proposal.
        ↓
(e) separately authenticated CAN011 target rule/currentness/permission
    candidate/target_rules.py :: evaluate_target
    Branches: CREATE / NO_CHANGE / DENY with 14 typed reasons.
    Self-issued → DENY. Foreign owner → DENY. Missing rule → DENY.
    Revoked/expired/stale-prestate → DENY. Insufficient history → NO_CHANGE.
        ↓
(f) atomic occurrence/effect/no-ghost rollback + readset
    candidate/transaction.py :: CandidateStore.commit
    BEGIN IMMEDIATE; readset bound in receipt; injected fault → rollback + no-ghost verification.
    Occurrence admission is a separate prior commit and survives response rollback.
        ↓
(g) later E2 target READ by named action consumer
    candidate/later_action.py :: read_target_for_later_action
    No consumer → typed MISSING_CONSUMER. Consumer read cross-checked against committed state.
    As-of before commit → refused. State absent → typed STATE_ABSENT.
        ↓
(h) genuine performed-action owner admission or typed HOLD
    candidate/action_admission.py :: admit_performed_action
    Missing owner receipt → typed HOLD naming exact missing owner form.
    Hand-authored action → always refused.
```

## What is reused from accepted native modules

- **`rawlsing_next/v3_psepf_zero_positive_guard.py`** — imported directly; its production registry is confirmed empty; every conditioning source is routed through `evaluate_psepf_zero_positive_guard`. This is the real native fail-closed control.
- **B3AS SQLite atomicity** (`1a25b19dd…`, `ACCEPT_SCOPED`) — reused as technical reference for the transaction pattern: `BEGIN IMMEDIATE`, readset comparison at publication, rollback integrity, no-ghost verification. The candidate implements its own store; it does not import B3AS code.
- **B1 transaction shape** (`c0f4588c…`) — reused as technical reference for the propose→validate→commit sequence and the separate owner-permission court. B1's `recognized_plan→joint_check` labels are NOT reused; the candidate derives no psychological content from response text.

## What is deliberately absent

- No hand-authored later actual action. The later-action consumer reads committed state and produces a candidate route; a performed action requires separate owner admission.
- No psychological state awarded from a candidate response. No memory, belief, affect, wound, trait or relationship mutation.
- No production positive from fixtures. The TEST_ONLY chain uses explicitly typed test-only rules and permissions with `permission_ceiling='COMMISSION_AUTHORIZED_TEST_ONLY'`; the release gate never reads them as native authority.
- No self-granted owner. `request_is_self_issued=True` is always denied.

## Two materially distinct trajectories

Two materially distinct admitted event/action trajectories were exercised at TEST_ONLY ceiling:

| Trajectory | Event id | Time | Content | Causal parents |
|---|---|---|---|---|
| E1 | `event-c9p-e1` | 15 | `shared_tool_offer` / wrench | none |
| E2 | `event-c9p-e2` | 16 | `second_shared_tool_offer` / spanner | none |

Both produce distinct event hashes and distinct responses. The lawful unchanged counterfactual is held: no rule/action issuer permits a binding no-change contrast. The NO_CHANGE branch of the target evaluator is implemented and tested (`INSUFFICIENT_ENACTED_HISTORY`, `NO_PROPOSAL`).

## Atomicity and no-ghost guarantees

| Guarantee | Test | Result |
|---|---|---|
| Committed receipt binds exact readset | `test_committed_transaction_binds_readset_and_event` | PASS |
| Denied decision leaves no target rows | `test_denied_decision_leaves_no_target_rows` | PASS |
| Injected fault → rollback + no-ghost | `test_no_ghost_under_injected_storage_fault` | PASS |
| Unadmitted event refused with rollback | `test_unadmitted_event_is_refused_with_rollback` | PASS |
| Response/event mismatch refused | `test_response_event_mismatch_is_refused` | PASS |
| CREATE requires matching prestate | `test_create_decision_requires_matching_prestate` | PASS |
| Occurrence survives response rollback | `test_occurrence_survives_response_rollback` | PASS |
| Cold reopen finds committed target | `test_test_only_create_chain_survives_cold_reopen` | PASS |
