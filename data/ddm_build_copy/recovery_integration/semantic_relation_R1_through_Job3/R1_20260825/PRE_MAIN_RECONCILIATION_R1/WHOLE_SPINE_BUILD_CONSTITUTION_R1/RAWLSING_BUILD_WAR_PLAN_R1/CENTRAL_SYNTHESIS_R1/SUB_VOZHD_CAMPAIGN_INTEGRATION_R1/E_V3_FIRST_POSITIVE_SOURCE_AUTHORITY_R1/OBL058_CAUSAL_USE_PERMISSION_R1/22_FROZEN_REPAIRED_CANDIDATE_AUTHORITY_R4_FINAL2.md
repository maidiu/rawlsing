# OBL058 — CAUSAL_USE_PERMISSION — FINAL R4 CANDIDATE FREEZE R2

## Status

`FROZEN_R4_CANDIDATE__READY_FOR_PRODUCER_GOVERNED_COURT__NO_INDEPENDENT_REVIEW`

The earlier pre-court R4 freezes `ff8be5eb12fafa40b1479355581cccff0a67debd` and `1cf7087c41a5d8ac3a16aff329e4704a56325645` received no governed evidence execution and are superseded before court.

This final pre-court repair removes the long-lived mutable issuance ledger entirely. Each issued receipt receives one dedicated one-shot authority subprocess. That child performs the source-owned semantic decision exactly once, fixes one exact `(object identity, authoritative body)` pair for its own lifetime, and thereafter accepts validation requests only. It exposes no second initialize, append, replace, rebind, delete/reinsert, register-body, or generic mint operation.

## Final R4 identities

- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.3.1`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@4.1.0`
- executable: `causal_use_permission_candidate_r4.py`
- fixture class: `NONCURRENT_SYNTHETIC`

## Source-origin boundary

Correctness does not depend on secrecy of parent-process Python closures, leading-underscore naming, or a caller-inaccessible mutable parent ledger. The issuer, validator, transport helper, and receipt-authority launcher have no authority-bearing closure state. Recovering the transport or launcher does not permit caller-built receipt content to become authoritative because initialization accepts only the exact semantic scope/basis/fixture inputs and constructs the body inside the child authority process.

A receipt's parent-visible body and process handles are not authoritative. Rebinding a DENY body to a PERMIT body, copying all parent-visible receipt state, recovering the exact receipt type, constructing an object with `object.__new__`, proxying, subclassing, copying, deep-copying, or serializing cannot satisfy the child process's fixed object-identity/body pair.

## Preserved controls

R4 preserves the exact five-field actor/world/subject/time/transition scope binding, field-specific `NONCURRENT_SYNTHETIC` namespaces, exact first-canary and project-current-shaped identity rejection, one frozen source-owned positive basis, unregistered-basis denial, absence of caller permission/basis-kind inputs, exact authority/schema/fixture/scope/basis-proof/content-integrity checks, cross-scope replay rejection, inference-like surrogate denial, no public source-basis registration surface, and all no-current-effect prohibitions.

## Evidence boundary

This commit is the semantic candidate SHA for the R4 governed bounded-repair court. No independent review has been performed by the R4 repair worker.

`INDEPENDENT_REVIEW_PERFORMED_BY_R4_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`
