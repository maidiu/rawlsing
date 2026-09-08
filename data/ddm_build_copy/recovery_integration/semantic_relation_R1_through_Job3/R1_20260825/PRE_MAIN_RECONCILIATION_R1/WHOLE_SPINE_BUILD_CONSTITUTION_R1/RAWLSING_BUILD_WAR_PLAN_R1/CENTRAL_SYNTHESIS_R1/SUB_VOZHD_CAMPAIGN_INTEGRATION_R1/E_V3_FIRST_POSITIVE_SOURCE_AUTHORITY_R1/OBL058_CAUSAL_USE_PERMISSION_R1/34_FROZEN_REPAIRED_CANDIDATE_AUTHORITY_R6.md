# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R6

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R6 repairs only the requester-process/object-generation defect returned by the exactly-one fresh R5 independent review. It preserves the R5 broker/channel repair and the semantic controls already confirmed correct. This worker does not perform independent review.

## Revised identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- executable: `causal_use_permission_candidate_r6.py`
- producer court: `test_bounded_repair_r6.py`
- fixture class: `NONCURRENT_SYNTHETIC`

The immutable candidate freeze is the commit containing this authority document, executable, and producer court. Its exact SHA is recorded by the governed court and return packet.

## Exact R6 repair

R5 bound validation to the genuine broker process and one-shot authority child, but broker records were keyed by bare integer `id(receipt)` plus body/authority-instance state. A forked process inherits a distinct process-local copy at the same virtual address, so the copied receipt can present the same integer ID and body.

R6 adds the requester process generation to each broker record using operating-system-observed peer identity. On `issue`, the broker records the connecting process PID, UID, and `/proc/<pid>/stat` start-time generation together with the exact object ID, authoritative body, authority-instance ID, and one-shot child. On `validate` and `close`, the broker obtains peer credentials from the live Unix-domain connection and recomputes the peer process start-time. The record is accepted only when PID, UID, and process-start generation exactly match the issuer process generation.

Caller-supplied requester identity fields are not part of the protocol and are rejected by exact request-shape validation.

Therefore a fork-child copy of a parent-issued receipt presents the same process-local integer object address but a different OS process generation and is rejected before the one-shot authority child is consulted.

## Object-generation retirement

`IssuedReceipt` is weak-referenceable and carries only its public body slot. Normal issuance registers a weak-reference finalizer that asks the source-owned broker to retire the exact object-ID record when the issued object is released. The broker permits `close` only from the original requester process generation. Duplicate close is idempotent.

This prevents a normal later same-process object generation from inheriting a stale authoritative record merely because CPython later reuses an address after the original issued object has been destroyed.

The finalizer/close path is not consulted to create positive authority; it can only retire an existing record.

## Preserved R5 controls

R6 preserves:

- genuine broker endpoint/PID/UID/start-time verification;
- rejection of unrelated same-user broker replacement;
- broker-death and authority-child-death fail-closed behavior;
- one-shot child initialization and source-owned scope/basis/fixture decision;
- no caller-built authoritative-body injection;
- exact actor/world/subject/time/transition binding;
- field-specific `NONCURRENT_SYNTHETIC` namespaces;
- exact current first-canary and other project-current-shaped identity rejection;
- one frozen source-owned positive basis;
- unregistered-basis `DENY`;
- exact basis proof, scope digest, authority, schema, fixture, authority-instance and content-integrity checks;
- plain mapping/proxy/reconstruction/subclass/exact-type fabrication rejection;
- copy/deepcopy/serialization rejection;
- cross-scope replay rejection;
- stable repeated and concurrent same-process validation;
- multiple-receipt authority-instance separation;
- denial of classification/routing/occurrence/proximity/narrative-like surrogate permission;
- no public source-basis registration surface;
- no project-current effect.

## Producer verification before freeze

Local producer verification of the exact candidate/test pair completed green:

`30 passed, 21 subtests passed`

The governed repository court remains the required producer evidence of record and must bind to this frozen candidate SHA.

## Authority ceiling / no current effect

This candidate does not create or activate an actor, create positive applicability, admit an occurrence, prove contact-witness independence, create ENCOUNTER, realize OEE, install current-positive OBL056 state, execute OBL055, update project-current authority state, or claim SUB-VOZHD E/HQ adoption.

`INDEPENDENT_REVIEW_PERFORMED_BY_R6_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

## Required next gate

Run the governed R6 producer court against this exact frozen candidate. If green, return it to SUB-VOZHD E for exactly one fresh distinct independent review. Do not self-review.
