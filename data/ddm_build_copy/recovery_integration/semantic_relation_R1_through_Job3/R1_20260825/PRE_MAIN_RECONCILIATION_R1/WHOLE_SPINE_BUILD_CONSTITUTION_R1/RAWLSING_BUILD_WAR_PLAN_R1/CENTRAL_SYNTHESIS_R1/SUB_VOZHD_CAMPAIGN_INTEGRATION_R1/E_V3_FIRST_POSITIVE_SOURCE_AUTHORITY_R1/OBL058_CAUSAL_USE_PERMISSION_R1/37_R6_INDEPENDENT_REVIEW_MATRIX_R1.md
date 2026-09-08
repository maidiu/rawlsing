# OBL058 — CAUSAL_USE_PERMISSION — R6 INDEPENDENT REVIEW MATRIX R1

## Status

`FROZEN_BEFORE_GOVERNED_REVIEW_EXECUTION`

This matrix is independently authored for the fresh R6 review. It does not modify the frozen candidate and does not prescribe a repair.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r6-independent-review-r1`
- exact review start: `2523e2a3bc2470a08a8c4ca78a7357007738c427`
- campaign authority: `4aac8ec1b9222ce19f3092cd6f1789b5d216af76`
- frozen target: `92418a9e13f55464a91c1c9f1deb96977bc294ef`

## Independent review families

1. `PROCESS_GENERATION` — parent-issued synthetic PERMIT and DENY observed from `fork()` children; repeated child validation/close; parent remains valid.
2. `OS_REQUESTER_IDENTITY` — peer PID/UID/process-start identity must be OS-observed; caller-supplied requester identity fields must not control acceptance.
3. `OBJECT_RECORD_LIFECYCLE` — ordinary weak-reference finalization, explicit close, duplicate close, close-after-finalization, and stale record retirement.
4. `FINALIZER_REACHABILITY` — determine whether ordinary runtime access to Python weak-reference finalizer state can suppress the only retirement path and leave an authoritative stale object-ID record. If suppression is possible, attempt later exact-type object-ID reuse with the saved body; allocator non-reproduction alone is not proof of correctness.
5. `DISTINCT_RECEIPTS` — equal semantic inputs must still produce distinct authority-instance identities; cross-receipt body reuse must fail.
6. `RECONSTRUCTION` — exact constructor, `object.__new__`, subclass, Mapping/proxy, JSON round-trip, copy/deepcopy and serialization cases.
7. `BROKER_BINDING` — genuine endpoint/PID/UID/start-time binding; unrelated endpoint replacement; broker death and one-shot authority-child death.
8. `REQUEST_ISOLATION` — repeated/concurrent same-process validation and request/response identity isolation between receipts.
9. `SCOPE_AND_BASIS` — exact five-field scope/basis binding; field-specific `NONCURRENT_SYNTHETIC` namespaces; exact current first-canary/project-current-shaped rejection; authority/schema/fixture/proof/authority-instance/content-integrity checks; surrogate inference denial.
10. `VALID_CONTROLS` — genuine synthetic PERMIT and DENY must remain functional; review may not pass by fail-all behavior.
11. `NO_CURRENT_EFFECT` — no project-current permission, OBL056 positive entry, OBL055 execution, ENCOUNTER, OEE realization or authority-index effect.

## Disposition law

Any reproducible acceptance by a later process/object generation that was not the generation originally issued is a blocking source-origin defect. Any such finding returns semantic FAIL without modifying the frozen candidate.

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`PROJECT_CURRENT_EFFECT_CREATED_BY_MATRIX = NO`
