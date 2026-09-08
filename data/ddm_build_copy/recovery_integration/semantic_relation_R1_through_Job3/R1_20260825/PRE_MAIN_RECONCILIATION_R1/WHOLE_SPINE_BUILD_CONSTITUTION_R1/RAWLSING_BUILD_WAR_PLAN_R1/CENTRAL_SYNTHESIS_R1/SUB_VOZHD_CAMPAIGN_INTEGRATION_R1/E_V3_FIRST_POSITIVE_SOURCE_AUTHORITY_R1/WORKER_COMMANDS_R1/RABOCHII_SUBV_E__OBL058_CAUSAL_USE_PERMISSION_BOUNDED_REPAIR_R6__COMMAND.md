# RABOCHII SUB-VOZHD E — OBL058 CAUSAL_USE_PERMISSION — BOUNDED REPAIR R6 COMMAND R1

ROLE: `RABOCHII BOUNDED REPAIR IMPLEMENTER`

REPORTS TO: `SUB-VOZHD E`

LANE: `E1 / OBL058 — CAUSAL_USE_PERMISSION R6 REQUESTER/OBJECT-GENERATION BINDING REPAIR`

WORKER BRANCH:
`agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r6`

EXACT STARTING HEAD:
`c299ab4765d513b45815b19be131e4d5082b397a`

FAILED FROZEN R5 CANDIDATE:
`43474152150350c1b5c73374abd24ecebc627b99`

R5 REVIEW RECOMMENDATION:
`FAIL__OBL058_R5_INDEPENDENT_REVIEW__FORKED_PROCESS_RECEIPT_COPY_RETAINS_ACCEPTED_SOURCE_ORIGIN`

SMALLEST BLOCKER:
`BLOCKER__OBL058_R5_BROKER_OBJECT_ID_BINDING_OMITS_REQUESTER_PROCESS_GENERATION`

This is a repair-only continuation. Do not modify the frozen R5 candidate in place. Produce a new frozen R6 candidate.

## Read first

Read and obey the SUB-VOZHD E campaign charter, orchestration law, all OBL058 R1–R5 candidate/court/review/repair returns, the R5 independent review return at `c299ab4765d513b45815b19be131e4d5082b397a`, and the current SUB-VOZHD E adjudication from its immutable campaign ref supplied with this command.

## Exact repair objective

Close only the requester-process/object-generation source-origin defect while preserving the R5 broker/channel repair and all already-correct semantic boundaries.

The R5 broker correctly binds to the genuine broker process and one-shot authority child, but the authoritative record is still keyed by a bare integer `id(receipt)` without the requester process generation that owns the object. Under `fork()`, the child process receives a distinct process-local copy at the same virtual address and can present the same integer ID/body to the inherited broker.

R6 must ensure that validation accepts only the process generation and object generation for which the source-owned issuance decision was made.

At minimum:

1. a forked child-process copy of a genuine issued positive receipt must fail closed rather than validate `PERMIT` through the parent broker record;
2. a forked child-process copy of a genuine issued `DENY` must not gain or retain authority outside its original requester process generation;
3. broker validation must derive or verify requester process identity from source-owned/OS-observed state rather than trusting caller-supplied requester identity fields;
4. stale broker records must not authorize a later object generation after the original issued object is released;
5. same-process ordinary repeated/concurrent validation of a live issued receipt must continue to work;
6. the repair must not reintroduce caller-selectable broker/transport authority or rely on naming conventions or secrecy of inspectable Python objects.

The worker may choose the smallest sound implementation. A natural design may bind broker records to OS-observed requester PID/process-start generation plus exact object ID and use a close/finalization path to retire the record before object identity can be reused, but architecture selection remains with the worker.

## Preservation law

Preserve the R5 controls independently confirmed correct:

- genuine broker endpoint/PID/UID/start-time verification;
- unrelated same-user endpoint replacement rejection;
- broker-death and authority-child-death fail-closed behavior;
- source-owned one-shot child semantic decision;
- no caller-built body injection;
- exact actor/world/subject/time/transition binding;
- field-specific `NONCURRENT_SYNTHETIC` namespace enforcement;
- exact current first-canary and other project-current-shaped identity rejection;
- registered source basis, scope/proof and authority-instance integrity;
- authority/schema/fixture/content-integrity checks;
- constructor/`object.__new__`/subclass/mapping/proxy/JSON/copy/deepcopy/pickle rejection on ordinary paths;
- cross-scope replay rejection;
- stable repeated/concurrent validation without result mixing;
- multiple-module/broker-instance isolation;
- denial of classification/routing/occurrence/proximity/narrative-like surrogate permission;
- no public source-basis registration surface;
- no project-current effect.

Do not widen source-owner jurisdiction or enter OBL059/OBL060, comparator, PSEPF, OBL032, architecture/topology, sibling-campaign, or project-current semantics.

## Governed R6 court requirements

Freeze the new R6 candidate before governed evidence execution. The producer court must include direct regressions for the R5 review blocker and preserved controls, including at minimum:

- parent issued `PERMIT`, then `fork()`: child copy must fail closed;
- parent issued `DENY`, then `fork()`: child copy must fail closed;
- child attempts repeated validation of inherited receipt;
- parent remains able to validate the same live receipt after child rejection;
- requester PID/process-start binding checked from OS-observed peer state where applicable;
- direct caller-supplied requester identity fields ignored or rejected;
- released receipt causes broker record retirement before later object generation can be accepted;
- stale close/replay and duplicate close behavior is fail-closed/idempotent as appropriate;
- ordinary same-process repeated and concurrent validation remains stable;
- multiple receipts with equal bodies remain distinct;
- cross-receipt, cross-scope and cross-module reuse remain rejected;
- exact-type fabrication, copied/proxied/reconstructed/serialized receipts remain rejected;
- broker endpoint replacement, broker death and child death regressions remain green;
- valid synthetic `PERMIT` and `DENY` controls;
- all basis/scope/fixture/current-boundary regressions;
- no path to project-current permission, current-positive OBL056, OBL055 execution, ENCOUNTER, or OEE.

Record exact candidate, tests, governed evidence execution, run, job, artifact, ZIP SHA-256, and court terminal.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R6_REPAIR_WORKER = NO`

Do not commission, perform, or claim the fresh independent review of the R6 candidate. If the producer court is green, return to SUB-VOZHD E. SUB-VOZHD E alone will commission exactly one fresh distinct reviewer against the new frozen R6 candidate.

## Hard prohibitions

Do NOT create project-current positive causal-use permission, actor state, positive applicability, occurrence, witness independence, ENCOUNTER, OEE, current-positive OBL056 entries, or execute OBL055.

Do NOT claim SUB-VOZHD E adoption or HQ adoption.

## Required return

Return a durable repository packet containing the new frozen R6 candidate identity, exact repair description, governed court identities/results, regression coverage for requester/object-generation binding, no-self-review attestation, no-current-effect attestation, and recommendation to SUB-VOZHD E.

Terminal:

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_BOUNDED_REPAIR_R6__RETURN_TO_SUB_VOZHD_E`
