# 03 — Owner-release gate (T2)

**Status: `C9_NATIVE_POSITIVE_HELD`.** The gate independently checks seven surfaces. No surface is cleared. Seven finite owner HOLD forms are preserved. A fixture's `CURRENT_ACCEPTED`, a recomputed digest, an arbitrary rule hash or a locally granted owner never clears any hold.

## The seven surfaces checked

| Surface | Verified? | Evidence |
|---|---|---|
| CAN008 concrete RULE_A issuer | **No** | `CAN008_RULE_ISSUER_UNVERIFIED`. C9O located the jurisdictional owner (`V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE`) and verified R2 semantic adoption (`a6bc1555…` → `b80dd692…`), but no competent specifically empowered officer/forum with a signed/current concrete rule body and native registry action. |
| CAN011 RULE_T target grant | **No** | `CAN011_TARGET_UNISSUED`. CAN011 canon (`1ed04e62…`) owns `V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY@1.0.0` with `V3MS_MEDIATOR`, `V3MS_TENSION`, `V3MS_PRACTICE`. No independently adopted target update rule or conditional grant. |
| ADP019 event witness | **No** | `ADP019_ACTOR_EVENT_WITNESS_MISSING`. Real owner receipt required; `ADMITTED_SYNTHETIC_FIXTURE_ONLY` is not native. |
| ADP010 encounter witness | **No** | `ADP010_ENCOUNTER_WITNESS_MISSING`. No generated encounter/exposure receipt bound to a real actor identity. |
| PSEPF positive-transition registry | **No** | `POSITIVE_TRANSITION_REGISTRY_EMPTY`. `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES = {}` confirmed by test. A non-empty production registry requires a separate accepted authority binder/code change. |
| Performed-action owner | **No** | `PERFORMED_ACTION_OWNER_UNPROVED`. No actuator owner receipt with `actuator_ref`, `act`, `occurrence_ref`, `action_time`. |
| Later-action consumer | **No** | `LATER_ACTION_CONSUMER_UNBOUND`. No registered production later-action consumer of committed target state. |

## Finite owner HOLD forms

Each HOLD names the exact competent owner, the exact decision required and the evidence needed:

1. **`CAN008_RULE_ISSUER_UNVERIFIED`**
   - Owner: V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE competent concrete rule issuer
   - Decision: sign one exact RULE_A body/version/content-hash with allowed subjects, witnessed enacted history predicates, effective time and current source/use registry
   - Evidence: issuing office evidence, signed adoption record, rule body hash, registry entry

2. **`CAN011_TARGET_UNISSUED`**
   - Owner: V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY separate target-owner authority
   - Decision: adopt exact RULE_T body and a conditional V3MS_PRACTICE CREATE/NO_CHANGE/DENY grant with before/read/write sets, replay, rollback, expiry and revocation law
   - Evidence: separate target-rule adoption record, grant id/scope/expiry, registry snapshot hash

3. **`ADP019_ACTOR_EVENT_WITNESS_MISSING`**
   - Owner: External Admission Court (ADP019)
   - Decision: admit the exact precipitating occurrence with owner receipt and effective clock
   - Evidence: ADP019 admission receipt, immutable event id/hash/time, actor encounter receivability

4. **`ADP010_ENCOUNTER_WITNESS_MISSING`**
   - Owner: ADP010 generated encounter owner
   - Decision: admit the generated encounter/exposure basis for the actor
   - Evidence: ADP010 encounter receipt bound to the actor identity

5. **`POSITIVE_TRANSITION_REGISTRY_EMPTY`**
   - Owner: PSEPF production positive-transition registry binder
   - Decision: a separate accepted authority change registering the concrete positive transition authority outside any test caller
   - Evidence: accepted authority binder/code change with non-empty production registry

6. **`PERFORMED_ACTION_OWNER_UNPROVED`**
   - Owner: later performed-action actuator owner
   - Decision: admit one genuine performed action with independent occurrence receipt
   - Evidence: owner receipt with `actuator_ref`, `act`, `occurrence_ref`, `action_time`

7. **`LATER_ACTION_CONSUMER_UNBOUND`**
   - Owner: native later-action consumer owner
   - Decision: bind the exact downstream reader of committed target state
   - Evidence: registered consumer module/function with a verified committed-state read

## Gate behavior under fixture-supplied authority

`evaluate_release_gate(fixture_supplied_authority={...})` records that a fixture was supplied but **ignores it**. The gate stays `C9_NATIVE_POSITIVE_HELD`. This is tested by `test_fixture_supplied_authority_never_clears_gate`.

## What would clear the gate

All seven surfaces must be backed by independently authenticated competent issuers at the run's declared read cut. The gate then returns `C9_NATIVE_POSITIVE_AUTHORIZED`. This state has never been reached.
