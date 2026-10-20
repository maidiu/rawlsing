# 01 — Source and juridical executable inventory (T0)

**Classification:** every seam is one of `ISSUED_RUNTIME`, `ACCEPTED_SEMANTICS_NO_RUNTIME`, `RESEARCH_FIXTURE`, `ABSENT` or `REQUIRES_COMPETENT_ISSUER`. Actual imported `__file__` and Git blob identities are asserted for every native module the candidate reaches.

## Native modules actually imported

| Module | `__file__` tail | Git blob SHA-1 | Seam class |
|---|---|---|---|
| `rawlsing_next.v3_psepf_zero_positive_guard` | `v3_psepf_zero_positive_guard.py` | `e0528d65215cb431196570c38bac4eae94217a1b` | `ISSUED_RUNTIME` |
| `rawlsing_next.wsc_gt0_protocol` | `wsc_gt0_protocol.py` | recorded in `evidence/source_hashes.json` | `ISSUED_RUNTIME` |
| `rawlsing_next.wsc_gt0_v3_runtime` | `wsc_gt0_v3_runtime.py` | recorded in `evidence/source_hashes.json` | `ISSUED_RUNTIME` |

Custody is enforced by `candidate/native_custody.py`; a blob mismatch raises `CustodyMismatch` (tested).

## Seam classification

| Seam | Authority source | Classification | Evidence |
|---|---|---|---|
| PSEPF zero-positive guard | `v3_psepf_zero_positive_guard.py` blob `e0528d65…` | `ISSUED_RUNTIME` | production registry confirmed empty; `evaluate_psepf_zero_positive_guard` denies zero effect for every guarded truth class |
| CAN008 R2 semantic coupling | HQ adoption `a6bc1555…` → body `b80dd692…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | adopted semantics expressly `NO_RUNTIME_IMPLEMENTATION` |
| CAN008 v1 response transaction grammar | `976c5908…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | governs `V3_ACTOR_RESPONSE_RULE_REGISTRY@1.0.0` transaction grammar; no native registry entry |
| CAN008 concrete RULE_A | none found | `REQUIRES_COMPETENT_ISSUER` | `CAN008_RULE_ISSUER_UNVERIFIED` |
| CAN011 target jurisdiction | `1ed04e62…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | `V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY@1.0.0`; three state kinds canonicalized |
| CAN011 concrete RULE_T | none found | `REQUIRES_COMPETENT_ISSUER` | `CAN011_TARGET_UNISSUED` |
| ADP007 actor creation + activation | `28813c57…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | jurisdiction established; no runnable native actor activation entrypoint bound here |
| ADP008 developmental active | `6428e26f…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | phase labels not default |
| ADP010 generated encounter | `gt34_adp010_input_authority_acceptance.py` | `RESEARCH_FIXTURE` | input-authority acceptance module; not a production encounter admission |
| ADP019 external occurrence admission | `5c38772e…` | `REQUIRES_COMPETENT_ISSUER` | real owner receipt required; `ADMITTED_SYNTHETIC_FIXTURE_ONLY` is not native |
| ADP015 relationship | `a4dab0a1…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | no relationship mutation from CAN011 alone |
| ADP016 memory | `0b7bbe29…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | no serial memory→belief conversion |
| ADP017 belief/claim access | `6b4162df…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | no actor belief from structural position |
| ADP020 causal RNG | `1911352f…` | `ACCEPTED_SEMANTICS_NO_RUNTIME` | no random choice without named-stream rule |
| ADP021 clock | W1 authority | `ACCEPTED_SEMANTICS_NO_RUNTIME` | no causal progress on scheduling alone |
| B3AS SQLite atomicity | `1a25b19dd…` | `RESEARCH_FIXTURE` | `ACCEPT_SCOPED` sourcefree logical SQLite; reusable as technical reference only |
| B1 coupled-development adapter | `c0f4588c…` blob `94ffc528…` | `RESEARCH_FIXTURE` | sourcefree test-only; `recognized_plan→joint_check` labels are not defensible psychology |
| S1 independent science court | `0d47fe86…` | `RESEARCH_FIXTURE` | `REVISE_BEFORE_NATIVE_INTEGRATION`; confirms local computation, denies psychology |
| LIFE1 world/relation/epochal court | `7ffc20dd…` | `RESEARCH_FIXTURE` | 30/30 tests, 156/156 native owner tests; 16/16 native positive `DEFER` remain |
| M6 actor-safe expression | `m6_actor_safe_expression.py` | `ISSUED_RUNTIME` | bounded V2 render; no actor-state write |
| GT0 end-to-end harness | `wsc_gt0_end_to_end.py` | `ISSUED_RUNTIME` | `TERMINAL = BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS` |
| Later-action consumer | none registered in production | `ABSENT` | typed `MISSING_CONSUMER` refusal implemented |
| Performed-action actuator owner | none registered | `REQUIRES_COMPETENT_ISSUER` | typed HOLD implemented |
| Native positive-transition registry | `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES` = `{}` | `ISSUED_RUNTIME` (empty) | confirmed by `test_guard_production_registry_is_empty` |

## Where zero-positive and read/write effects are controlled

The zero-positive guard (`v3_psepf_zero_positive_guard.py`) is the single fail-closed control point for truth-to-actor transitions. Its production registry is immutable and empty. A non-empty registry requires a separate accepted authority binder/code change. The guard never mutates actor state, causal history, RNG state or scheduler state. Every conditioning source in the candidate path is routed through this guard; the outcome `DENY_ZERO_EFFECT` is preserved and recorded.

Read/write effects at the candidate transport level are controlled by `candidate/transaction.py` (`BEGIN IMMEDIATE`, readset comparison, rollback integrity) following the B3AS technical pattern. Target CREATE/NO_CHANGE/DENY is controlled by `candidate/target_rules.py` with separate rule and permission jurisdictions.

## Scoped owner/read/action/middle-state APIs captured

| API surface | Module | Contract |
|---|---|---|
| `ingress_actor(record, as_of)` | `candidate/identity.py` | ADP007-style actor identity/activation/standing-state; fail-closed |
| `ingress_event(raw, as_of, last_time, prior_event_hashes)` | `candidate/events.py` | ADP010/019 event witness; typed missing witnesses |
| `bind_conditioning(subject, sources, as_of)` | `candidate/conditioning.py` | read-only person/world conditioning; no source→psyche conversion |
| `lookup_rule(registry, …)` | `candidate/response_rules.py` | CAN008 rule registry lookup; RULE_ABSENT / RULE_ISSUER_UNVERIFIED / FOUND |
| `evaluate_response(…)` | `candidate/response_rules.py` | bounded immediate response; never mints target permission |
| `evaluate_target(…)` | `candidate/target_rules.py` | CAN011 CREATE / NO_CHANGE / DENY branches |
| `CandidateStore.commit(…)` | `candidate/transaction.py` | atomic occurrence/effect/no-ghost + readset |
| `read_target_for_later_action(…)` | `candidate/later_action.py` | later E2 target READ by named consumer |
| `admit_performed_action(…)` | `candidate/action_admission.py` | genuine performed-action owner admission or typed HOLD |
| `evaluate_release_gate(…)` | `candidate/release_gate.py` | T2 owner-release gate |
| `run_candidate_path(…)` | `candidate/pipeline.py` | complete chain (a)–(h) |
