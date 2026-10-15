# HQ300 — adopted-interface derivation (positive owner signature, effect dimensions, registry permission, owner methods)

**Grain:** derivation from ADOPTED authority at exact pinned blobs. Nothing here is a new semantic law; every dimension below is transcribed from an adopted file, and every gap is named.

## 1. Registry permission — the decisive question

**The adopted production registry grants no positive-transition authority.** Machine evidence (preserved, re-executed this commission):

| Probe | Result |
|---|---|
| `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES` (imported `v3_psepf_zero_positive_guard.py`, blob `e0528d65215cb431196570c38bac4eae94217a1b`) | `mappingproxy({})` — EMPTY |
| well-typed positive request, no authority presented | `DENY_ZERO_EFFECT / ZERO_POSITIVE_REGISTRY` |
| `DELEGATE_TO_ACCEPTED_OWNER` | UNREACHABLE while registry empty |
| guard docstring | "A later separately accepted authority change must update the production registry/binder; a runtime caller cannot manufacture positive authority by passing a mapping" |

**Conclusion:** under accepted law the positive chain cannot run against the production registry. The commission anticipates this: *"Distinguish a worker candidate registry fixture from accepted zero-positive guard authorization; changing guard or granting real owner positive authority is forbidden."* Therefore the candidate chain runs against `candidate/candidate_registry_fixture.py` (`FIXTURE_GRAIN = SOURCEFREE_CANDIDATE_FIXTURE__NOT_ACCEPTED_AUTHORIZATION`), and the dual result is enforced by test: **the candidate chain completes AND the imported production guard still denies the identical transition** (`test_B_imported_production_guard_still_denies`, `test_H_no_production_registry_mutation`).

## 2. Positive owner signature — CAN-008 R2 adopted dimensions

From adopted blob `b80dd6925066510ecbbfec7b427bf9f688475663` (contract `V3_ACTOR_RESPONSE_PRESSURE_FLOW_TRANSACTION_RULESET@2.0.0-CANDIDATE.R1`):

| Dimension | Adopted content | Candidate implementation |
|---|---|---|
| §6 occurrence gate | no committed causal response without exact generated/admitted precipitating occurrence; `DRAFT_RESPONSE / REJECTED_RENDER / UNEMITTED_CANDIDATE -> NO_SELF_FEEDBACK`; static state may condition, never precipitate | `occurrence_gate()` — H1/H6 hostile coverage |
| §7–10 coupling | receivability → actor uptake/appraisal projection → situated recruitment; `machine reading != uptake`, `uptake != durable belief`, `recruitment != access` | `coupline_evaluate()` with all three noncollapses as typed fields |
| §11 handoff | coupling → **registered** response rule → working-view effects → target-owner validation → atomic commit OR rollback; effect grammar `BUFFER/AMPLIFY/DEFLECT/REROUTE/TRANSFORM/BLOCK` unchanged; durable target state remains destination-owner-owned | `response_rule_apply()`; target effects are `SEPARATELY_OWNED_EFFECT_REQUEST` with `committed: false` at the request boundary (`test_C_target_owner_effect_is_request_not_seizure`) |
| §14 valid-empty/nonpositive | 17 distinct nonpositive states; missing/ambiguous never silently converted | `NONPOSITIVE_DECISION_STATES` transcribed; fail-closed returns |
| §16 rule obligations | 23 items "at minimum where applicable"; omission **fails closed** | `CouplingRuleBinding.validate_complete()` over `R2_RULE_OBLIGATION_ITEMS` (23); default binding passes; empty modality-evidence is bound explicitly as `NONE_USED` (§5.3 modality evidence is optional) |
| §17 receipt | `V3ResponseEvaluationReceipt` content = event stream IDs/hashes/authorities/times, conditioning refs + causal-use roles, receivability/uptake/recruitment, effect records + target validation, valid-empty decisions, provenance/replay; **the receipt is audit evidence, NOT a durable actor uptake/memory/belief state** | `build_response_receipt()` with `is_durable_actor_state: false` |

## 3. Target-owner effect dimensions — ADP-016 (blob `c6619a286e115d060ab4830889e7fc23762167a5`)

| Adopted interface | Candidate implementation |
|---|---|
| `GeneratedMemoryState` 13 required fields | `adopted_contract.GeneratedMemoryState` + `validate_memory_state` |
| `representation_kind ∈ {EVENT_REFERENTIAL_MEMORY, CAUSAL_TRACE_MEMORY}` | trace commit uses `CAUSAL_TRACE_MEMORY` |
| `MemoryTransitionRecord` 20 required fields + deterministic transition identity | `adp016_form_causal_trace` emits full record; identity = SHA-256 over actor/memory/kind/parents/rule/pre-post |
| `formation_rule.all_gates_required` (7 gates) | all enforced in `adp016_form_causal_trace` (admitted basis, parent id+hash verify, experiencer relation or lawful trace, source-bound features, rule-authorized effect, pre-state integrity, stochastic authority if used) |
| `formation_rule.ineligible_direct_sources` | H7 hostile: persona prose / rendered dialogue / V2 transcript / structural object / analyst annotation → `INELIGIBLE_NONCAUSAL_SOURCE`, no mutation |
| `fail_closed_states` (16) | `ADP016_FAIL_CLOSED_STATES` transcribed; `adp016_attempt_transition` raises typed `OwnerTransitionError` (H8: `PARENT_EVENT_HASH_MISMATCH`, `PRE_STATE_HASH_MISMATCH`) |
| forbidden `DELETE_MEMORY` | enforced (`test_H_delete_memory_forbidden`) |
| `UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION` | enforced (`test_H_rehydration_forbidden`) |
| `UNAUTHORIZED_RECALL_CUE` on causal trace | enforced (`test_D_K3_causal_trace_not_recallable`) |
| `actor_accessibility_boundary`: exports memory identity/kind/feature/retention/accessibility/uncertainty/provenance; **never** `actor_knows / actor_believes / may_claim_first_person` | `must_not_output` carried on every trace receipt; `first_person_origin_claimable: false` |

## 4. Target-owner effect dimensions — ADP-017 (blob `eece4f3f2f3f9288ab9bbc645dc81e20a99e1280`)

| Adopted interface | Candidate implementation |
|---|---|
| `ActorEpistemicEffect` 12 required fields; `stance_operation ∈ {ADD, WITHDRAW, SUPERSEDE_EXACT_RECORD, NO_CHANGE}` | `adp017_apply_epistemic_effect` validates all fields + enums |
| `knowledge_gate`: ALL 7 required; **objective truth necessary, NOT sufficient**; co-presence/system observability insufficient | `knowledge_gate_check` (K5 test: truth-supported claim without actor-facing basis → `DEFERRED_MISSING_EPISTEMIC_BASIS`) |
| `belief_gate`: no objective-status auto-belief | belief effects require actor-facing basis refs; `objective_status_auto_creates_or_edits_belief=false` honored |
| `epistemic_state_model.automatic_implications_forbidden` (8) | transcribed and asserted (`test_E_K5_no_automatic_implication_enumerated`) |
| `first_person_permission.mapping` | `first_person_permission()` transcribed exactly; K3 causal-trace override forces `DENY_FIRST_PERSON_CLAIM` (`causal_trace_memory_first_person_basis=false`) |
| `memory_interaction` noncollapse (4) + `sole_memory_basis_rule` | `adp017_sole_memory_basis_failclosed` (dead basis → deny, stance not erased) |
| `analyst_only_exclusions` (5 incl. `ANALYST_ONLY_CAUSAL_TRACE`) | enforced by the K3 firewall tests |
| `decision_states` (6) | transcribed; `no_transition_means_no_epistemic_state_change=true` honored |

## 5. Causal-order custody

The chain commits target-owner effects to a `ChainEventLedger` with hash-chained entries and **non-decreasing effective causal time** (H9). Reverse chronology is refused both at the ledger (`BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT`) and at the coupling gate for events carrying inverted causal parents.

## 6. The later-event read (situation dependence)

The later admitted event reads the previously committed `CAN008_CURRENT_RESPONSE_EFFECT` from the ledger and its typed response is **conditioned** on it (`BUFFER` → later `DEFLECT`); the control run lacking the prior effect yields `AMPLIFY`. The typed difference is asserted (`test_C_later_event_reads_stored_effect_and_differs_from_control`) — this is the "one later event reads it" requirement, demonstrated as a typed effect difference, not prose.

## 7. What remains owner jurisdiction (not created here)

1. The production positive-transition-authority registry entry (owner: CAN008/accepted-law issuer) — the guard awaits exactly this.
2. The concrete R2 rule inventory as **accepted** rules (the candidate rule is a worker candidate registered only in the fixture).
3. Any real V3 actor, ADP019 admission producer, or ADP020 stochastic binding.
4. The `CAND_R_CAN008_COUPLING_RESPONSE@1.0.0-candidate` → accepted-rule promotion decision.
