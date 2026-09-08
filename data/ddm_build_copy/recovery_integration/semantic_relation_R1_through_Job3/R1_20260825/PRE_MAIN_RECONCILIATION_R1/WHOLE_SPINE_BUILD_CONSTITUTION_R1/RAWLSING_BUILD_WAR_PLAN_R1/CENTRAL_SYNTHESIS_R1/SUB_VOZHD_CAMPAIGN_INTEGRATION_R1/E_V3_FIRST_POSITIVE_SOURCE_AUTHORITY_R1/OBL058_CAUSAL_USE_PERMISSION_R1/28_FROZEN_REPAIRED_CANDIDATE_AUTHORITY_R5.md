# OBL058 — CAUSAL_USE_PERMISSION — FROZEN REPAIRED CANDIDATE AUTHORITY R5

## Status

`FROZEN_REPAIRED_CANDIDATE__NOT_PROJECT_CURRENT__NOT_HQ_ADOPTED`

R5 repairs only the parent transport/response binding defect returned by the exactly-one fresh R4 independent review. It preserves the one-shot child semantic decision and the already-correct scope, basis, fixture, integrity, and no-current-effect controls. This repair worker does not perform independent review.

## Revised identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.4.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@5.0.0`
- executable: `causal_use_permission_candidate_r5.py`
- producer court: `test_bounded_repair_r5.py`
- fixture class: `NONCURRENT_SYNTHETIC`

The immutable commit containing this document, executable, and producer court is the R5 semantic candidate SHA recorded by the governed evidence.

## Exact decision grain

The candidate decides `CAUSAL_USE_PERMISSION` only for:

`(actor_id, world_id, subject_id, time_id, transition_id)`

A `PERMIT` remains possible only for the one frozen source-owned positive basis bound to the exact registered noncurrent-synthetic scope.

## R5 source-owned channel binding

R4 correctly moved the source-owned semantic decision into a one-shot child authority, but the parent receipt still carried mutable process and transport fields. Validation trusted those caller-rebindable fields, so a different responder could stand in for the source-owned child.

R5 removes parent receipt transport/process authority state.

Each issued receipt has only one caller-visible content slot, `_body_json`. It carries no read descriptor, write descriptor, process handle, broker handle, socket object, marker, token, or decision capability.

Authoritative channel ownership is split into two process-local layers:

1. one dedicated one-shot receipt-authority child performs the exact scope/basis/fixture decision and fixes one exact object-identity/body/authority-instance tuple;
2. one separate broker process owns the mapping from parent object identity to that exact one-shot authority child and its authoritative body.

The parent process never receives a child `Popen`, child read/write descriptor, or child channel. Those remain in the broker process.

## Exact broker-instance binding

Validation does not trust a process or transport field supplied by the receipt.

The validator is generated once at module initialization with immutable code constants naming:

- the broker Unix-domain socket path;
- the original broker PID;
- the original broker `/proc/<pid>/stat` start-time identity;
- the expected broker user identity.

On every validation it reconnects to that socket and verifies Linux `SO_PEERCRED` against the exact broker PID and verifies the original process start time before sending the request.

Therefore:

- replacing receipt fields cannot redirect validation because those fields do not exist;
- replacing the socket endpoint with another process fails peer-identity validation;
- PID reuse or broker replacement fails start-time validation;
- an unrelated live process cannot satisfy the broker identity check;
- parent helper replacement does not affect the bound validator because validation contains its own broker identity constants and channel checks.

This is an operating-system process identity boundary, not a Python naming or secrecy convention.

## Response/receipt binding

Every parent-to-broker validation uses a fresh request identity and requires the exact response identity.

The broker then validates only through the original one-shot child associated with the exact parent object identity. The child independently checks:

- exact receipt object identity;
- exact authoritative body;
- exact authority-instance identity;
- expected scope;
- authority/schema/fixture;
- scope and basis binding;
- source-basis proof;
- receipt content integrity.

Each broker request uses a fresh connection, so concurrent or repeated validations cannot consume another request's stream response. Cross-receipt body reuse is rejected by the exact child identity/body binding.

## Preservation controls

R5 preserves:

- one-shot child initialization;
- no caller-built body injection during initialization;
- exact five-field scope binding;
- field-specific `NONCURRENT_SYNTHETIC` namespaces;
- exact current first-canary subject rejection;
- other project-current-shaped identity rejection;
- one frozen source-owned positive basis;
- unregistered basis denial;
- no caller permission boolean or basis-kind input;
- exact authority/schema/fixture/scope/basis-proof/content-integrity checks;
- plain mapping/proxy/reconstruction/subclass/exact-type fabrication rejection;
- copy/deep-copy/serialization rejection;
- cross-scope replay rejection;
- denial of classification/routing/occurrence/proximity/narrative surrogate bases;
- valid synthetic `PERMIT` and `DENY`;
- no public source-basis registration API.

## Authority ceiling / no current effect

This candidate does not create or activate an actor, create positive applicability, admit an occurrence, prove contact-witness independence, create ENCOUNTER, realize OEE, install current-positive OBL056 state, execute OBL055, update a project-current authority index, or claim SUB-VOZHD E/HQ adoption.

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R5_REPAIR_WORKER = NO`

## Required next gate

After a green producer R5 governed bounded court, return this frozen candidate to SUB-VOZHD E.

SUB-VOZHD E alone may commission exactly one fresh distinct independent review of the R5 candidate.
