# OBL058 — CAUSAL_USE_PERMISSION — R2 INDEPENDENT REVIEW — GOVERNED COURT EVIDENCE R1

## Status

`GOVERNED_EXECUTION_GREEN__SEMANTIC_ADJUDICATION_SEPARATE`

This artifact records the fresh distinct independent robustness review court for frozen repaired candidate:

`f735c85393280557284b3a309cafc0847fb48aec`

A green execution means the independently authored assertions executed exactly as written. It does not by itself mean the candidate passes semantic review. Several assertions intentionally prove reproducible incorrect-positive acceptance paths.

## Independent review identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r2-independent-review-r1`
- exact starting HEAD: `292fba5789a78c85041a3ad02ed8be3358ce1c9c`
- frozen repaired semantic candidate: `f735c85393280557284b3a309cafc0847fb48aec`
- repaired authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.1.0`
- repaired receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@2.0.0`
- independent failure-mode matrix freeze: `e60470821f94c150e9f30aaf69e06aada3418645`
- independent primary-test commit: `28653ecb25fac9c98888216e48a393bc8749dba8`
- governed wrapper commit: `e73c7a0218327ab0f0c370ca554baee8f5886488`
- governed court binding / evidence execution: `7c71c646b2d33ee30668f2b4ee477c4488b17726`
- execution-only PR: `#279`, closed unmerged
- PR synthetic merge identity: `84edd3e6ac35bb5a99afdd4565abca9298e701de`

The failure-mode matrix was frozen before the producer's detailed R2 court was consumed. Producer-side tests were read only after that independent matrix freeze.

## Governed court

- workflow: `Rabochii Governed Bounded Court`
- run: `34193616253`
- job: `101956543670`
- Python: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.07s`
- court-spec validation: `PASS`
- independent review court: `18 passed, 10 subtests passed in 0.05s`
- receipt result: `PASS`
- receipt exit code: `0`
- semantic candidate: `f735c85393280557284b3a309cafc0847fb48aec`
- evidence execution: `7c71c646b2d33ee30668f2b4ee477c4488b17726`
- artifact ID: `10043065416`
- artifact ZIP SHA-256: `694b528502fb04d74b221f9cde6a24ca967f13534de0bc73682539c6c4421e65`

The execution-only PR was closed unmerged after evidence capture. The transient independent-review court-spec pointer was then restored to its starting producer-side value; that closure action did not modify the frozen candidate or the evidence execution.

## Independently reproduced blocking behavior

### I01 — module-level origin wrapper remains caller-accessible

The module stores `_wrap_source_issued_receipt` as a callable. A caller can assemble the exact positive body from public candidate constants, the registered basis identity, exact scope, and public digest rules, pass that body through the module-level wrapper, and obtain an object that `validate_receipt()` recognizes as source-issued and validates as `PERMIT`.

This directly defeats the R2 freeze claim that public callers cannot turn an arbitrary Mapping into a receipt recognized as emitted by the bounded source-authority instance.

### I02 — an issued receipt's internal data slot can be rebound

The mapping interface is read-only, but the returned receipt object exposes the `_data` slot and does not prohibit reassignment. The court obtains a genuine source-issued `DENY`, replaces its `_data` with a complete positive body, retains the original provenance marker, and the validator returns `PERMIT`.

Therefore mapping-surface immutability does not establish immutable source-origin semantics.

### I03 — the source-origin marker is recoverable and reusable

A legitimate issued receipt exposes `_marker`, and its concrete receipt class is recoverable with `type(receipt)`. The court uses the marker from a genuine `DENY` to construct a new receipt object carrying caller-assembled positive content. The validator recognizes that object as source-issued and returns `PERMIT`.

Thus the provenance token is transferable from one issued object to another rather than remaining authority-owned issuance state.

### I04 — the provenance predicate is subclass-overridable

The source-origin check uses `isinstance(receipt, IssuedReceipt)` followed by a dynamically dispatched `receipt._has_source_provenance()` call. A subclass can supply its own Mapping data and override that predicate to return `True`. The resulting caller-constructed object validates as `PERMIT` when its visible fields satisfy the otherwise-correct registry and digest checks.

Therefore the validator does not require the exact concrete source-issued object identity it claims to require.

## Controls that did hold

The same independent court confirmed the repaired candidate correctly enforces the following controls in ordinary paths:

- the registered positive basis validates for its exact synthetic scope;
- a plain Mapping copy of a genuine receipt is rejected;
- an unregistered basis yields `DENY`;
- the registered basis cannot be rebound across actor, world, subject, time, or transition;
- project-current-shaped namespaces are rejected for every scope field;
- the exact current first-canary subject is rejected;
- a `PROJECT_CURRENT` fixture label is rejected;
- wrong expected scope is rejected;
- nested scope post-construction mutation is detected;
- wrong authority and schema remain rejected;
- incorrect basis proof and basis-scope digest remain rejected;
- a denial conflicting with the registered positive basis remains rejected.

These controls show that R2 repaired the registry, exact-scope, namespace, and visible-content checks. They do not close the independently reproduced source-origin boundary defects I01-I04.

## Evidence holding

`INDEPENDENT_REVIEW_EXECUTION = GREEN`

`INDEPENDENT_REVIEW_SEMANTIC_HOLDING = FAIL`

The court's green result proves I01-I04 are reproducible against the frozen R2 candidate. The semantic FAIL is recorded in the separate independent-review return artifact.

## Non-action attestation

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`HQ_ADOPTION_CLAIMED = NO`

No central, PRE-MAIN, main, SUB-VOZHD integration, or sibling-lane branch was moved by this review worker.
