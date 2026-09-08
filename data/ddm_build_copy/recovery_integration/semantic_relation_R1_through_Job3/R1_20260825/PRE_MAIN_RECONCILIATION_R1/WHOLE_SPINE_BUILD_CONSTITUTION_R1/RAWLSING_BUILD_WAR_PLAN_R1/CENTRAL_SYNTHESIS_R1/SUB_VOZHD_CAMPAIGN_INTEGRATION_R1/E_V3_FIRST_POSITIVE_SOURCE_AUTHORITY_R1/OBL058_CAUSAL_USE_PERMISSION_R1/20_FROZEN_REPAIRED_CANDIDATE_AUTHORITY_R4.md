# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R4

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R4 repairs only the source-origin capability-confinement defect returned by the exactly-one fresh R3 independent review. It preserves the R3 semantic controls already confirmed correct and does not perform independent review.

## Revised identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.3.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@4.0.0`
- executable: `causal_use_permission_candidate_r4.py`
- fixture class: `NONCURRENT_SYNTHETIC`

The immutable candidate freeze is the commit containing this authority document and the executable above; its exact SHA is recorded in the governed evidence and return packet.

## Exact decision grain

The candidate decides `CAUSAL_USE_PERMISSION` only for the exact tuple:

`(actor_id, world_id, subject_id, time_id, transition_id)`

A positive result remains possible only for the one frozen source-owned basis bound to the exact registered synthetic scope. All project-current-shaped scope identifiers remain forbidden.

## R4 source-origin boundary

R3 stored authoritative issuance state in parent-process Python closures. The fresh R3 review correctly showed that ordinary Python introspection could recover the minting helper and mutable ledger.

R4 removes that trust assumption.

Authoritative issuance state now exists only inside a separate repository-local authority subprocess. The imported parent module contains no alias to that subprocess-local issuance dictionary. The parent-facing transport exposes a deliberately narrow protocol:

1. `issue` accepts only object identity, exact scope, basis identity, and fixture class;
2. the authority subprocess independently validates those semantic inputs and constructs the complete authoritative receipt body itself;
3. `issue` rejects any extra caller-supplied receipt body/content field;
4. `validate` independently rechecks semantic content and then requires the exact object identity and exact authoritative body previously bound by the subprocess;
5. there is no append, replace, rebind, delete/reinsert, register-body, or generic mint operation.

The transport is not secret. Recovering its file-descriptor constants or invoking the protocol directly does not grant arbitrary receipt authority because the protocol never accepts caller-built authoritative content. A direct `issue` request still executes the same source-owned semantic decision inside the isolated authority process.

## No inspectable parent authority state

The generated parent request function has:

- no Python closure;
- no positional defaults;
- no keyword defaults;
- no captured ledger, registry, cache, receipt body, marker, token, or source decision object;
- only immutable pipe descriptor integers in its code constants.

The service process object is not retained as a module global after initialization. A private atexit callback retains it only for lifecycle cleanup, not for issuance or validation.

The receipt itself contains only a caller-visible JSON body slot. That slot is not authoritative. Rebinding it cannot alter subprocess authority state, and validation fails if it differs from the exact body previously bound to that object identity.

## Preservation controls

R4 preserves:

- exact five-field scope binding;
- field-specific `NONCURRENT_SYNTHETIC` namespaces;
- exact current first-canary subject rejection;
- project-current-shaped identity rejection;
- unregistered-basis `DENY`;
- no caller permission boolean;
- no caller basis-kind input;
- exact authority/schema/fixture/scope/basis proof/content-integrity checks;
- plain Mapping/proxy/reconstruction/subclass/exact-type fabrication rejection;
- copy/deep-copy/serialization rejection;
- cross-scope replay rejection;
- no public source-basis registration surface;
- no inference from classification, routing, occurrence/admission, ADP-010, proximity, co-location, or narrative plausibility.

## Non-authoritative lifetime pinning

The parent registers a no-op atexit callback holding each issued receipt so CPython cannot recycle an issued object identity while the authority subprocess remains alive. This pin is never consulted by issue or validate and cannot confer, alter, or transfer permission authority. Mutating or bypassing lifecycle cleanup can only reduce availability; it cannot create a positive receipt.

## Authority ceiling / no current effect

This candidate does not create or activate an actor, create positive applicability, admit an occurrence, prove witness independence, create ENCOUNTER, realize OEE, install current-positive OBL056 state, execute OBL055, update a project-current authority index, or claim SUB-VOZHD E/HQ adoption.

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R4_REPAIR_WORKER = NO`

## Required next gate

After the producer R4 governed bounded court is green, return this new frozen candidate to SUB-VOZHD E. SUB-VOZHD E alone may commission exactly one fresh distinct independent review of this R4 candidate.
